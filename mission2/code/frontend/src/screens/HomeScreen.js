import React, { useState, useEffect } from 'react';
import { View, Text, TouchableOpacity, StyleSheet, Image, Alert } from 'react-native';
import axios from 'axios';
import { SafeAreaView } from 'react-native-safe-area-context';
import { MotiView, MotiImage } from 'moti';

const API_URL = 'http://10.0.2.2:8000'; // Android Emulator localhost
// const API_URL = 'http://localhost:8000'; // iOS Simulator
// const API_URL = 'http://<YOUR_LAN_IP>:8000'; // Physical Device

export default function HomeScreen({ navigation }) {
    const [status, setStatus] = useState(null);
    const [loading, setLoading] = useState(true);

    const fetchStatus = async () => {
        try {
            const response = await axios.get(`${API_URL}/status`);
            setStatus(response.data);
        } catch (error) {
            console.log('Error fetching status:', error);
        } finally {
            setLoading(false);
        }
    };

    const sendCommand = async (command) => {
        try {
            await axios.post(`${API_URL}/${command}`);
            Alert.alert('Success', `Robot ${command}ed`);
            fetchStatus();
        } catch (error) {
            Alert.alert('Error', `Failed to ${command} robot`);
        }
    };

    useEffect(() => {
        fetchStatus();
        const interval = setInterval(fetchStatus, 2000);
        return () => clearInterval(interval);
    }, []);

    return (
        <SafeAreaView style={styles.container}>
            <View style={styles.contentContainer}>
                <MotiView
                    style={styles.logoContainer}
                    from={{ opacity: 0, scale: 0.5 }}
                    animate={{ opacity: 1, scale: 1 }}
                    transition={{
                        type: 'spring',
                        duration: 1000,
                        damping: 15,
                    }}
                >
                    <View style={styles.logoBackground}>
                        <Image source={require('../../assets/logo.png')} style={styles.logo} resizeMode="contain" />
                    </View>
                </MotiView>

                <View style={styles.controls}>
                    <MotiView
                        from={{ opacity: 0, translateY: 50 }}
                        animate={{ opacity: 1, translateY: 0 }}
                        transition={{
                            type: 'timing',
                            duration: 500,
                            delay: 500,
                        }}
                    >
                        <TouchableOpacity
                            activeOpacity={0.8}
                            onPress={() => navigation.navigate('Inventory')}
                        >
                            <MotiView
                                style={[styles.button, styles.startButton]}
                                from={{ scale: 1 }}
                                animate={({ pressed }) => ({
                                    scale: pressed ? 0.95 : 1,
                                })}
                                transition={{
                                    type: 'spring',
                                    damping: 10,
                                    stiffness: 200,
                                }}
                            >
                                <Text style={styles.buttonText}>Inventory</Text>
                            </MotiView>
                        </TouchableOpacity>
                    </MotiView>
                </View>
            </View>
        </SafeAreaView>
    );
}

const styles = StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: '#F9F8F2', // COLORS.background
    },
    contentContainer: {
        flex: 1,
        padding: 50,
        paddingTop: 0,
        paddingBottom: 200, // Push content up
        alignItems: 'center',
        justifyContent: 'center',
    },
    logoContainer: {
        marginBottom: -50,
        alignItems: 'center',
        width: '100%',
    },
    logoBackground: {
        width: '100%',
        alignItems: 'center',
        justifyContent: 'center',
    },
    logo: {
        width: 600,
        height: 600,
    },
    // headerTextContainer removed
    statusCard: {
        width: '100%',
        backgroundColor: '#FFFFFF',
        borderRadius: 20,
        padding: 20,
        marginBottom: 30,
        shadowColor: '#000',
        shadowOffset: { width: 0, height: 2 },
        shadowOpacity: 0.05,
        shadowRadius: 10,
        elevation: 3,
        borderWidth: 1,
        borderColor: '#E0E0E0',
    },
    cardTitle: {
        fontSize: 18,
        color: '#6B8E23', // COLORS.primary
        marginBottom: 15,
        fontWeight: '600',
    },
    statusInfo: {
        gap: 10,
    },
    row: {
        flexDirection: 'row',
        justifyContent: 'space-between',
    },
    label: {
        color: '#6B4E3D', // COLORS.text
        fontSize: 16,
        opacity: 0.8,
    },
    value: {
        color: '#6B4E3D', // COLORS.text
        fontSize: 16,
        fontWeight: 'bold',
    },
    offlineText: {
        color: '#BF616A',
        fontStyle: 'italic',
        textAlign: 'center',
    },
    controls: {
        width: '100%',
        gap: 15,
    },
    button: {
        flexDirection: 'row',
        alignItems: 'center',
        justifyContent: 'center',
        paddingVertical: 18,
        borderRadius: 30, // Pill shape
        gap: 10,
        shadowColor: '#000',
        shadowOffset: { width: 0, height: 4 },
        shadowOpacity: 0.1,
        shadowRadius: 8,
        elevation: 5,
    },
    startButton: {
        backgroundColor: '#6B8E23', // COLORS.primary
    },
    stopButton: {
        backgroundColor: '#BF616A', // Keep red for stop, but maybe softer?
        opacity: 0.9,
    },
    buttonText: {
        color: '#FFF',
        fontSize: 22,
        fontWeight: '600',
    },
});
