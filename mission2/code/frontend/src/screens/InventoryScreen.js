import React, { useState, useEffect, useCallback } from 'react';
import { useFocusEffect } from '@react-navigation/native';
import { View, Text, FlatList, StyleSheet, RefreshControl, TouchableOpacity, ActivityIndicator } from 'react-native';
import axios from 'axios';
import { SafeAreaView } from 'react-native-safe-area-context';
import { Package, Clock, Tag, ArrowLeft } from 'lucide-react-native';
import { MotiView } from 'moti';

// const API_URL = 'http://10.0.2.2:8000'; // Android Emulator
// const API_URL = 'http://localhost:8000'; // iOS
const API_URL = process.env.EXPO_PUBLIC_API_URL

export default function InventoryScreen({ navigation }) {
    const [items, setItems] = useState([]);
    const [refreshing, setRefreshing] = useState(false);
    const [loading, setLoading] = useState(true);

    const FAKE_DATA = [
        { name: 'Red Apple', qty: 1, timestamp: '06/12/25 10:30 AM' },
        { name: 'Banana', qty: 5, timestamp: '06/12/25 10:32 AM' },
        { name: 'Carrot', qty: 2, timestamp: '06/12/25 10:35 AM' },
        { name: 'Milk', qty: 12, timestamp: '06/12/25 10:40 AM' },
        { name: 'Cereal', qty: 7, timestamp: '06/12/25 10:45 AM' },
    ];

    useFocusEffect(
        useCallback(() => {
            fetchInventory();
        }, [])
    );

    const fetchInventory = async () => {
        try {
            const response = await axios.get(`${API_URL}/inventory`);
            setItems(response.data);
        } catch (error) {
            console.log('Error fetching inventory:', error);
        } finally {
            setLoading(false);
        }
    };

    const onRefresh = useCallback(async () => {
        setRefreshing(true);
        await fetchInventory();
        setRefreshing(false);
    }, []);

    const renderItem = ({ item, index }) => (
        <MotiView
            from={{ opacity: 0, translateY: 20 }}
            animate={{ opacity: 1, translateY: 0 }}
            transition={{
                type: 'timing',
                duration: 500,
                delay: index * 100,
            }}
            style={styles.itemCard}
        >
            <View style={styles.iconContainer}>
                <Package color="#6B4E3D" size={24} />
            </View>
            <View style={styles.itemDetails}>
                <Text style={styles.itemName}>{item.name}</Text>
                <View style={styles.metaRow}>
                    <Tag color="#8FBC8F" size={14} />
                    <Text style={styles.qty}>Qty: {item.qty}</Text>
                </View>
                <View style={styles.metaRow}>
                    <Clock color="#8FBC8F" size={14} />
                    <Text style={styles.itemTime}>{item.timestamp}</Text>
                </View>
            </View>

        </MotiView>
    );

    return (
        <SafeAreaView style={styles.container}>
            <View style={styles.header}>
                <TouchableOpacity onPress={() => navigation.goBack()} style={styles.backButton}>
                    <ArrowLeft color="#6B4E3D" size={28} />
                </TouchableOpacity>
                <Text style={styles.headerTitle}>Inventory</Text>
            </View>

            {loading ? (
                <View style={styles.loadingContainer}>
                    <ActivityIndicator size="large" color="#6B8E23" />
                    <Text style={styles.loadingText}>Loading inventory...</Text>
                </View>
            ) : (
                <FlatList
                    data={items}
                    renderItem={renderItem}
                    keyExtractor={(item, index) => index.toString()}
                    contentContainerStyle={styles.list}
                    refreshControl={
                        <RefreshControl refreshing={refreshing} onRefresh={onRefresh} tintColor="#6B8E23" />
                    }
                    ListEmptyComponent={
                        <Text style={styles.emptyText}>No items logged yet.</Text>
                    }
                />
            )}
        </SafeAreaView>
    );
}

const styles = StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: '#F9F8F2', // COLORS.background
        padding: 20,
    },
    header: {
        flexDirection: 'row',
        alignItems: 'center',
        marginBottom: 20,
        gap: 15,
    },
    backButton: {
        padding: 5,
    },
    headerTitle: {
        fontSize: 28,
        fontWeight: 'bold',
        color: '#6B4E3D', // COLORS.text
        fontFamily: 'System',
    },
    list: {
        gap: 15,
        paddingBottom: 20,
    },
    itemCard: {
        backgroundColor: '#FFFFFF', // COLORS.cardBackground
        borderRadius: 16, // Soft geometry
        padding: 15,
        flexDirection: 'row',
        alignItems: 'center',
        shadowColor: '#000',
        shadowOffset: { width: 0, height: 2 },
        shadowOpacity: 0.05,
        shadowRadius: 5,
        elevation: 2,
        borderWidth: 1,
        borderColor: '#E0E0E0',
    },
    iconContainer: {
        backgroundColor: '#F0F4C3', // Light yellowish green for icon background
        padding: 12,
        borderRadius: 12,
        marginRight: 15,
    },
    itemDetails: {
        flex: 1,
        gap: 4,
    },
    itemName: {
        color: '#6B4E3D', // COLORS.text
        fontSize: 16,
        fontWeight: 'bold',
    },
    metaRow: {
        flexDirection: 'row',
        alignItems: 'center',
        gap: 5,
    },
    qty: {
        color: '#6B4E3D', // COLORS.text
        fontSize: 12,
        opacity: 0.7,
    },
    itemTime: {
        color: '#8FBC8F', // COLORS.primaryGradientStart
        fontSize: 12,
    },
    statusBadge: {
        color: '#6B8E23', // COLORS.primary
        fontWeight: 'bold',
        fontSize: 12,
        backgroundColor: '#F0F4C3',
        paddingHorizontal: 8,
        paddingVertical: 4,
        borderRadius: 8,
        overflow: 'hidden',
    },
    emptyText: {
        color: '#A0A0A0', // COLORS.inactive
        textAlign: 'center',
        marginTop: 50,
        fontSize: 16,
    },
    loadingContainer: {
        flex: 1,
        justifyContent: 'center',
        alignItems: 'center',
    },
    loadingText: {
        marginTop: 10,
        color: '#6B4E3D',
        fontSize: 16,
        fontFamily: 'System',
    },
});
