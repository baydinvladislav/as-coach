import React from 'react';

import { Screens } from '@navigation';
import { createStackNavigator } from '@react-navigation/stack';
import { LoginScreen, RegistrationScreen, WelcomeScreen } from '@screens';

const Stack = createStackNavigator();

export const StackNavigator = () => (
  <Stack.Navigator
    initialRouteName={Screens.LoginScreen}
    screenOptions={{ headerShown: false, animationEnabled: false }}
  >
    <Stack.Screen name={Screens.WelcomeScreen} component={WelcomeScreen} />
    <Stack.Screen
      name={Screens.RegistrationScreen}
      component={RegistrationScreen}
    />
    <Stack.Screen name={Screens.LoginScreen} component={LoginScreen} />
  </Stack.Navigator>
);
