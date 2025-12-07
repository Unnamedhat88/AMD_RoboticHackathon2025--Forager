import React, { useState, useEffect, useCallback } from 'react';
import { View, Text, StyleSheet, Image, Dimensions, TouchableOpacity, Alert, Vibration } from 'react-native';
import axios from 'axios';
import { useFocusEffect } from '@react-navigation/native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { MotiView } from 'moti';
import { WebView } from 'react-native-webview';
import { Camera, Plus, ArrowLeft } from 'lucide-react-native';

const API_URL = process.env.EXPO_PUBLIC_API_URL;
const { width, height } = Dimensions.get('window');

// Mock camera aspect ratio (4:3)
const CAM_WIDTH = width;
const CAM_HEIGHT = width * (4 / 3);

export default function LiveViewScreen({ navigation }) {
    const [objects, setObjects] = useState([]);
    const [connected, setConnected] = useState(false);

    const [imageUri, setImageUri] = useState(`${API_URL}/camera/latest?t=${Date.now()}`);

    // Refs for stability and auto-logging
    const failureCount = React.useRef(0);
    const isLogging = React.useRef(false);
    const [isScanning, setIsScanning] = useState(false);

    const handleScanTrigger = async () => {
        setIsScanning(true);
        Vibration.vibrate(100);
        try {
            const res = await axios.post(`${API_URL}/robot/scan`);
            if (res.data.success) {
                Alert.alert("Robot Started", "Arm is picking up the item...");
            } else {
                Alert.alert("Busy", res.data.message || "Robot is busy");
                setIsScanning(false);
            }
        } catch (e) {
            Alert.alert("Error", "Could not trigger robot.");
            setIsScanning(false);
        }

        // Reset scanning state after a while or poll for status? 
        // For now, reset after 15s (approx cycle time)
        setTimeout(() => setIsScanning(false), 15000);
    };

    useFocusEffect(
        useCallback(() => {
            const interval = setInterval(fetchObjects, 200);
            return () => clearInterval(interval);
        }, [])
    );

    const fetchObjects = async () => {
        try {
            const response = await axios.get(`${API_URL}/objects`, { timeout: 1000 });
            setObjects(response.data);

            // Jitter Fix: Only update connection status on success
            failureCount.current = 0;
            if (!connected) setConnected(true);

            // Auto-Logging Logic
            if (!isLogging.current) {
                const unloggedItem = response.data.find(obj => !obj.logged);
                if (unloggedItem) {
                    isLogging.current = true;
                    await handleLogItem(unloggedItem.id, unloggedItem.name);
                    isLogging.current = false;
                }
            }
        } catch (error) {
            failureCount.current += 1;
            // Only go offline after 3 consecutive failures
            if (failureCount.current >= 3) {
                setConnected(false);
            }
        }
    };

    const handleLogItem = async (trackId, name) => {
        try {
            const response = await axios.post(`${API_URL}/log/${trackId}`);
            if (response.data.success) {
                Vibration.vibrate(50);
                // We don't need to alert anymore, the checkmark UI update is enough feedback
                // and the backend updates the 'logged' state in the next poll cycle.
            } else {
                // Silent fail or console warn
            }
        } catch (error) {
            // Ignore temporary failures
        }
    };

    const renderBoundingBox = (obj) => {
        // Backend currently returns [xmin, ymin, xmax, ymax] in "box" field if we updated tracker_state to store it.
        // Wait, tracker_state stores 'box' but GET /objects currently implementation in tracker_state.py sends:
        // {'id': tid, 'name': obj['label'], 'confidence': obj['score'], 'logged': obj.get('logged', False)}
        // it DOES NOT send 'box'. I need to update tracker_state.py to include 'box'.

        // Let's assume for now I will fix the backend to send 'box'.
        // coordinate system: backend is 640x480. Frontend is CAM_WIDTH x CAM_HEIGHT.

        if (!obj.box) return null;

        const [xmin, ymin, xmax, ymax] = obj.box;

        const scaleX = CAM_WIDTH / 640;
        const scaleY = CAM_HEIGHT / 480;

        const left = xmin * scaleX;
        const top = ymin * scaleY;
        const boxW = (xmax - xmin) * scaleX;
        const boxH = (ymax - ymin) * scaleY;

        return (
            <View key={obj.id} style={[styles.bbox, { left, top, width: boxW, height: boxH, borderColor: obj.logged ? '#A0A0A0' : '#6B8E23' }]}>
                {obj.logged ? (
                    <View style={[styles.labelTag, { backgroundColor: '#A0A0A0' }]}>
                        <Text style={styles.labelText}>✔ {obj.name} (Logged)</Text>
                    </View>
                ) : (
                    <View style={styles.labelTag}>
                        <Text style={styles.labelText}>{obj.name} {Math.round(obj.confidence * 100)}%</Text>
                    </View>
                )}


            </View>
        );
    };

    return (
        <SafeAreaView style={styles.container}>
            <View style={styles.header}>
                <TouchableOpacity onPress={() => navigation.navigate('Home')} style={{ paddingRight: 10 }}>
                    <ArrowLeft color="#6B4E3D" size={28} />
                </TouchableOpacity>
                <Text style={styles.title}>Live Perception</Text>
                <View style={[styles.statusBadge, { backgroundColor: connected ? '#6B8E23' : '#BF616A' }]}>
                    <Text style={styles.statusText}>{connected ? 'ONLINE' : 'OFFLINE'}</Text>
                </View>
            </View>

            <View style={styles.cameraContainer}>
                {/* Live Video Feed (WebView) */}
                <WebView
                    source={{
                        html: `
                        <html>
                          <body style="margin:0; padding:0; background:black; display:flex; justify-content:center; align-items:center;">
                            <img src="${API_URL}/video_feed" style="width:100%; height:100%; object-fit: fill;" />
                          </body>
                        </html>
                        `
                    }}
                    style={styles.cameraPreview}
                    scrollEnabled={false}
                    javaScriptEnabled={true}
                    domStorageEnabled={true}
                    scalesPageToFit={false} // Disable to let CSS handle scaling
                />

                {/* Overlay Layer */}
                <View style={styles.overlay}>
                    {objects.map(renderBoundingBox)}
                </View>

                {!connected && (
                    <View style={styles.centerMessage}>
                        <Text style={styles.messageText}>Connecting to Robot...</Text>
                    </View>
                )}
            </View>

            <View style={styles.footer}>
                <TouchableOpacity
                    style={[styles.scanButton, isScanning && styles.disabledButton]}
                    onPress={handleScanTrigger}
                    disabled={isScanning}
                >
                    <Text style={styles.scanButtonText}>{isScanning ? 'Robot Moving...' : 'Start Scan Cycle'}</Text>
                </TouchableOpacity>
                <Text style={styles.hintText}>Place item in pink area & press Start</Text>
            </View>
        </SafeAreaView>
    );
}

const styles = StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: '#F9F8F2',
    },
    header: {
        padding: 20,
        flexDirection: 'row',
        justifyContent: 'space-between',
        alignItems: 'center',
    },
    title: {
        fontSize: 24,
        fontWeight: 'bold',
        color: '#6B4E3D',
    },
    statusBadge: {
        paddingHorizontal: 10,
        paddingVertical: 4,
        borderRadius: 12,
    },
    statusText: {
        color: '#FFF',
        fontSize: 12,
        fontWeight: 'bold',
    },
    cameraContainer: {
        width: CAM_WIDTH,
        height: CAM_HEIGHT,
        backgroundColor: '#000',
        overflow: 'hidden',
        position: 'relative',
    },
    cameraPreview: {
        width: '100%',
        height: '100%',
        // opacity: 0.5, // Commented out to fix dark feed
    },
    overlay: {
        ...StyleSheet.absoluteFillObject,
    },
    centerMessage: {
        ...StyleSheet.absoluteFillObject,
        justifyContent: 'center',
        alignItems: 'center',
    },
    messageText: {
        color: '#FFF',
        fontSize: 18,
    },
    bbox: {
        position: 'absolute',
        borderWidth: 2,
        borderRadius: 4,
        // borderColor set dynamically
    },
    labelTag: {
        position: 'absolute',
        top: -20,
        left: 0,
        backgroundColor: 'rgba(0,0,0,0.7)',
        paddingHorizontal: 6,
        paddingVertical: 2,
        borderRadius: 4,
    },
    labelText: {
        color: '#FFF',
        fontSize: 10,
        fontWeight: 'bold',
    },
    logButton: {
        position: 'absolute',
        top: '50%',
        left: '50%',
        transform: [{ translateX: -30 }, { translateY: -15 }],
        backgroundColor: '#6B8E23',
        flexDirection: 'row',
        alignItems: 'center',
        paddingHorizontal: 12,
        paddingVertical: 8,
        borderRadius: 20,
        zIndex: 10,
        minWidth: 80, // Prevent squishing
        justifyContent: 'center',
    },
    logButtonText: {
        color: '#FFF',
        fontSize: 12,
        fontWeight: 'bold',
    },
    footer: {
        flex: 1,
        alignItems: 'center',
        justifyContent: 'center',
    },
    hintText: {
        color: '#6B4E3D',
        opacity: 0.6,
        marginTop: 10,
    },
    scanButton: {
        backgroundColor: '#6B4E3D',
        paddingHorizontal: 40,
        paddingVertical: 15,
        borderRadius: 30,
        elevation: 5,
    },
    disabledButton: {
        backgroundColor: '#A0A0A0',
    },
    scanButtonText: {
        color: '#FFF',
        fontSize: 18,
        fontWeight: 'bold',
    }
});
