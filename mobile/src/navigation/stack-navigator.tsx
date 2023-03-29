import React from 'react';

import { SmsScreen } from 'src/screens/sms';

import { Screens } from '@navigation';
import { createStackNavigator } from '@react-navigation/stack';
import {
  LkScreen,
  LoginScreen,
  RegistrationScreen,
  WelcomeScreen,
} from '@screens';

const Stack = createStackNavigator();

export const StackNavigator = () => (
  <Stack.Navigator
    initialRouteName={Screens.WelcomeScreen}
    screenOptions={{ headerShown: false, animationEnabled: false }}
  >
    <Stack.Screen name={Screens.WelcomeScreen} component={WelcomeScreen} />
    <Stack.Screen
      name={Screens.RegistrationScreen}
      component={RegistrationScreen}
    />
    <Stack.Screen name={Screens.LoginScreen} component={LoginScreen} />
    <Stack.Screen name={Screens.SmsScreen} component={SmsScreen} />
    <Stack.Screen name={Screens.LkScreen} component={LkScreen} />
  </Stack.Navigator>
);
