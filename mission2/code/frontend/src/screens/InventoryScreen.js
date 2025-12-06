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
                <Package color="#D8DEE9" size={24} />
            </View>
            <View style={styles.itemDetails}>
                <Text style={styles.itemName}>{item.item_name}</Text>
                <View style={styles.metaRow}>
                    <Tag color="#81A1C1" size={14} />
                    <Text style={styles.itemCategory}>{item.category}</Text>
                </View>
                <View style={styles.metaRow}>
                    <Clock color="#81A1C1" size={14} />
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
                    <RefreshControl refreshing={refreshing} onRefresh={onRefresh} tintColor="#D8DEE9" />
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
        backgroundColor: '#1E1E2E',
        padding: 20,
    },
    headerTitle: {
        fontSize: 28,
        fontWeight: 'bold',
        color: '#D8DEE9',
        marginBottom: 20,
    },
    list: {
        gap: 15,
    },
    itemCard: {
        backgroundColor: '#2E3440',
        borderRadius: 12,
        padding: 15,
        flexDirection: 'row',
        alignItems: 'center',
    },
    iconContainer: {
        backgroundColor: '#3B4252',
        padding: 10,
        borderRadius: 10,
        marginRight: 15,
    },
    itemDetails: {
        flex: 1,
        gap: 4,
    },
    itemName: {
        color: '#ECEFF4',
        fontSize: 16,
        fontWeight: 'bold',
    },
    metaRow: {
        flexDirection: 'row',
        alignItems: 'center',
        gap: 5,
    },
    itemCategory: {
        color: '#D8DEE9',
        fontSize: 12,
    },
    itemTime: {
        color: '#81A1C1',
        fontSize: 12,
    },
    statusBadge: {
        color: '#A3BE8C',
        fontWeight: 'bold',
        fontSize: 12,
    },
    emptyText: {
        color: '#4C566A',
        textAlign: 'center',
        marginTop: 50,
    },
});
