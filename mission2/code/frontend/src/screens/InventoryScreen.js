import React, { useState, useEffect, useCallback } from 'react';
import { View, Text, FlatList, StyleSheet, RefreshControl } from 'react-native';
import axios from 'axios';
import { SafeAreaView } from 'react-native-safe-area-context';
import { Package, Clock, Tag } from 'lucide-react-native';

const API_URL = 'http://10.0.2.2:8000'; // Android Emulator
// const API_URL = 'http://localhost:8000'; // iOS

export default function InventoryScreen() {
    const [items, setItems] = useState([]);
    const [refreshing, setRefreshing] = useState(false);

    const fetchInventory = async () => {
        try {
            const response = await axios.get(`${API_URL}/inventory`);
            setItems(response.data);
        } catch (error) {
            console.log('Error fetching inventory:', error);
        }
    };

    const onRefresh = useCallback(async () => {
        setRefreshing(true);
        await fetchInventory();
        setRefreshing(false);
    }, []);

    useEffect(() => {
        fetchInventory();
    }, []);

    const renderItem = ({ item }) => (
        <View style={styles.itemCard}>
            <View style={styles.iconContainer}>
                <Package color="#6B4E3D" size={24} />
            </View>
            <View style={styles.itemDetails}>
                <Text style={styles.itemName}>{item.item_name}</Text>
                <View style={styles.metaRow}>
                    <Tag color="#8FBC8F" size={14} />
                    <Text style={styles.itemCategory}>{item.category}</Text>
                </View>
                <View style={styles.metaRow}>
                    <Clock color="#8FBC8F" size={14} />
                    <Text style={styles.itemTime}>{item.timestamp}</Text>
                </View>
            </View>
            <Text style={styles.statusBadge}>{item.status}</Text>
        </View>
    );

    return (
        <SafeAreaView style={styles.container}>
            <Text style={styles.headerTitle}>Inventory</Text>
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
        </SafeAreaView>
    );
}

const styles = StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: '#F9F8F2', // COLORS.background
        padding: 20,
    },
    headerTitle: {
        fontSize: 28,
        fontWeight: 'bold',
        color: '#6B4E3D', // COLORS.text
        marginBottom: 20,
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
    itemCategory: {
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
});
