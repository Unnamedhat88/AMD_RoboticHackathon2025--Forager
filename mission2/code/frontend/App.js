import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { Home, List } from 'lucide-react-native';
import HomeScreen from './src/screens/HomeScreen';
import InventoryScreen from './src/screens/InventoryScreen';
import LiveViewScreen from './src/screens/LiveViewScreen';

const Tab = createBottomTabNavigator();

export default function App() {
  return (
    <NavigationContainer>
      <Tab.Navigator
        screenOptions={{
          headerShown: false,
          tabBarStyle: {
            display: 'none', // Hide the nav bar as requested, navigation via Home Screen buttons
            backgroundColor: '#F9F8F2', // COLORS.background
            borderTopColor: '#E0E0E0', // COLORS.border
            elevation: 0, // Remove shadow on Android for cleaner look
            shadowOpacity: 0, // Remove shadow on iOS
            height: 60,
            paddingBottom: 10,
          },
          tabBarActiveTintColor: '#6B8E23',
          tabBarInactiveTintColor: '#A0A0A0',
        }}
      >
        <Tab.Screen
          name="Home"
          component={HomeScreen}
          options={{
            tabBarIcon: ({ color, size }) => <Home color={color} size={size} />,
          }}
        />
        <Tab.Screen
          name="Inventory"
          component={InventoryScreen}
          options={{
            tabBarIcon: ({ color, size }) => <List color={color} size={size} />,
          }}
        />
        <Tab.Screen
          name="LiveView" // Internal name for navigation
          component={LiveViewScreen}
          options={{
            headerShown: false, // Hide native header, using custom one in screen
            tabBarButton: () => null, // Hide from tab bar
            tabBarStyle: { display: 'none' } // Hide tab bar when on this screen
          }}
        />
      </Tab.Navigator>
    </NavigationContainer>
  );
}
