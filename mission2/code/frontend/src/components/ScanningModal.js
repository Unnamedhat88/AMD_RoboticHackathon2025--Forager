import React from 'react';
import { View, Text, StyleSheet, Modal } from 'react-native';
import { MotiView } from 'moti';
import { Leaf } from 'lucide-react-native';

export default function ScanningModal({ visible }) {
    return (
        <Modal transparent visible={visible} animationType="fade">
            <View style={styles.container}>
                <View style={styles.content}>
                    <MotiView
                        from={{ scale: 1, opacity: 0.8 }}
                        animate={{ scale: 1.4, opacity: 1 }}
                        transition={{
                            type: 'timing',
                            duration: 1000,
                            loop: true,
                            repeatReverse: true,
                        }}
                        style={styles.iconContainer}
                    >
                        <Leaf color="#9FBF8A" size={80} fill="#9FBF8A" />
                    </MotiView>
                    <Text style={styles.text}>Scanning...</Text>
                </View>
            </View>
        </Modal>
    );
}

const styles = StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: 'rgba(245, 235, 220, 0.85)', // Cream with opacity
        justifyContent: 'center',
        alignItems: 'center',
    },
    content: {
        alignItems: 'center',
        gap: 20,
    },
    iconContainer: {
        marginBottom: 20,
    },
    text: {
        fontSize: 28,
        fontWeight: 'bold',
        color: '#4B3D2A', // Dark Soil Brown
        fontFamily: 'System',
    },
});
