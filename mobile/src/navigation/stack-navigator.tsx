import React from 'react';

import { createStackNavigator } from '@react-navigation/stack';
import { WelcomeScreen } from '@screens';

const Stack = createStackNavigator();

export const StackNavigator = () => (
  <Stack.Navigator screenOptions={{ headerShown: false }}>
    <Stack.Screen name="WelcomeScreen" component={WelcomeScreen} />
  </Stack.Navigator>
);
