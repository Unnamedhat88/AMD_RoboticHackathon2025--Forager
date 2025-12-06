import React, { useState, useEffect } from 'react';
import { View, Text, TouchableOpacity, StyleSheet, Image, Alert } from 'react-native';
import axios from 'axios';
import { SafeAreaView } from 'react-native-safe-area-context';
import { Play, Square, Activity } from 'lucide-react-native';

const API_URL = 'http://10.0.2.2:8000'; // Android Emulator localhost
// const API_URL = 'http://localhost:8000'; // iOS Simulator
// const API_URL = 'http://<YOUR_LAN_IP>:8000'; // Physical Device

export default function HomeScreen() {
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
            <View style={styles.header}>
                <Text style={styles.headerTitle}>GroceryBot</Text>
                <Activity color="#A3BE8C" size={24} />
            </View>

            <View style={styles.statusCard}>
                <Text style={styles.cardTitle}>System Status</Text>
                {status ? (
                    <View style={styles.statusInfo}>
                        <View style={styles.row}>
                            <Text style={styles.label}>State:</Text>
                            <Text style={styles.value}>{status.state}</Text>
                        </View>
                        <View style={styles.row}>
                            <Text style={styles.label}>Running:</Text>
                            <Text style={[styles.value, { color: status.running ? '#A3BE8C' : '#BF616A' }]}>
                                {status.running ? 'Active' : 'Stopped'}
                            </Text>
                        </View>
                        <View style={styles.row}>
                            <Text style={styles.label}>Current Item:</Text>
                            <Text style={styles.value}>{status.current_item || 'None'}</Text>
                        </View>
                    </View>
                ) : (
                    <Text style={styles.offlineText}>Connecting to robot...</Text>
                )}
            </View>

            <View style={styles.controls}>
                <TouchableOpacity style={[styles.button, styles.startButton]} onPress={() => sendCommand('start')}>
                    <Play color="#FFF" fill="#FFF" />
                    <Text style={styles.buttonText}>Start</Text>
                </TouchableOpacity>

                <TouchableOpacity style={[styles.button, styles.stopButton]} onPress={() => sendCommand('stop')}>
                    <Square color="#FFF" fill="#FFF" />
                    <Text style={styles.buttonText}>Stop</Text>
                </TouchableOpacity>
            </View>
        </SafeAreaView>
    );
}

const styles = StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: '#1E1E2E', // Dark background
        padding: 20,
    },
    header: {
        flexDirection: 'row',
        justifyContent: 'space-between',
        alignItems: 'center',
        marginBottom: 30,
    },
    headerTitle: {
        fontSize: 28,
        fontWeight: 'bold',
        color: '#D8DEE9',
    },
    statusCard: {
        backgroundColor: '#2E3440',
        borderRadius: 16,
        padding: 20,
        marginBottom: 30,
        shadowColor: '#000',
        shadowOffset: { width: 0, height: 4 },
        shadowOpacity: 0.3,
        shadowRadius: 4.65,
        elevation: 8,
    },
    cardTitle: {
        fontSize: 18,
        color: '#88C0D0',
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
        color: '#D8DEE9',
        fontSize: 16,
    },
    value: {
        color: '#ECEFF4',
        fontSize: 16,
        fontWeight: 'bold',
    },
    offlineText: {
        color: '#BF616A',
        fontStyle: 'italic',
    },
    controls: {
        flexDirection: 'row',
        justifyContent: 'space-around',
    },
    button: {
        flexDirection: 'row',
        alignItems: 'center',
        paddingVertical: 15,
        paddingHorizontal: 30,
        borderRadius: 12,
        gap: 10,
    },
    startButton: {
        backgroundColor: '#A3BE8C',
    },
    stopButton: {
        backgroundColor: '#BF616A',
    },
    buttonText: {
        color: '#FFF',
        fontSize: 18,
        fontWeight: 'bold',
    },
});
