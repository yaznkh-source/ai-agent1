import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { Text } from 'react-native';
import DashboardScreen from './screens/DashboardScreen';
import ChatScreen from './screens/ChatScreen';
import AgentsScreen from './screens/AgentsScreen';
import ProjectsScreen from './screens/ProjectsScreen';
import ClientPortalScreen from './screens/ClientPortalScreen';
import SettingsScreen from './screens/SettingsScreen';

// Mock icons - in real app use react-native-vector-icons
const TabIcon = ({ name, focused }: { name: string; focused: boolean }) => (
  <Text style={{ fontSize: 20, color: focused ? '#8b5cf6' : '#71717a' }}>{name}</Text>
);

const Tab = createBottomTabNavigator();

export default function App() {
  return (
    <NavigationContainer>
      <Tab.Navigator
        screenOptions={{
          tabBarActiveTintColor: '#8b5cf6',
          tabBarInactiveTintColor: '#71717a',
          headerStyle: { backgroundColor: '#8b5cf6' },
          headerTintColor: 'white',
          headerTitleStyle: { fontWeight: 'bold' }
        }}
      >
        <Tab.Screen
          name="Dashboard"
          component={DashboardScreen}
          options={{
            title: 'لوحة التحكم - 68 وكيل 292 مهارة',
            tabBarIcon: ({ focused }) => <TabIcon name="📊" focused={focused} />,
            tabBarLabel: 'Dashboard'
          }}
        />
        <Tab.Screen
          name="Chat"
          component={ChatScreen}
          options={{
            title: 'محادثات - Chat with 68 agents',
            tabBarIcon: ({ focused }) => <TabIcon name="💬" focused={focused} />,
            tabBarLabel: 'Chat'
          }}
        />
        <Tab.Screen
          name="Agents"
          component={AgentsScreen}
          options={{
            title: 'الوكلاء - 68 Agents',
            tabBarIcon: ({ focused }) => <TabIcon name="🤖" focused={focused} />,
            tabBarLabel: 'Agents'
          }}
        />
        <Tab.Screen
          name="Projects"
          component={ProjectsScreen}
          options={{
            title: 'المشاريع - Projects',
            tabBarIcon: ({ focused }) => <TabIcon name="📁" focused={focused} />,
            tabBarLabel: 'Projects'
          }}
        />
        <Tab.Screen
          name="ClientPortal"
          component={ClientPortalScreen}
          options={{
            title: 'بوابة العميل - Client Portal',
            tabBarIcon: ({ focused }) => <TabIcon name="👤" focused={focused} />,
            tabBarLabel: 'Clients'
          }}
        />
        <Tab.Screen
          name="Settings"
          component={SettingsScreen}
          options={{
            title: 'الإعدادات - Settings',
            tabBarIcon: ({ focused }) => <TabIcon name="⚙️" focused={focused} />,
            tabBarLabel: 'Settings'
          }}
        />
      </Tab.Navigator>
    </NavigationContainer>
  );
}
