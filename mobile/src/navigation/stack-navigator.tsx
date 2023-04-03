import React from 'react';

import { SmsScreen } from 'src/screens/auth/sms';

import { Screens } from '@navigation';
import { createStackNavigator } from '@react-navigation/stack';
import {
  ChangePasswordScreen,
  LkScreen,
  LoginScreen,
  NewChangePasswordScreen,
  ProfileEditScreen,
  ProfileScreen,
  RegistrationScreen,
  WelcomeScreen,
} from '@screens';

const Stack = createStackNavigator();

export const StackNavigator = () => (
  <Stack.Navigator
    initialRouteName={Screens.ProfileScreen}
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
    <Stack.Screen name={Screens.ProfileScreen} component={ProfileScreen} />
    <Stack.Screen
      name={Screens.ProfileEditScreen}
      component={ProfileEditScreen}
    />
    <Stack.Screen
      name={Screens.ChangePasswordScreen}
      component={ChangePasswordScreen}
    />
    <Stack.Screen
      name={Screens.NewChangePasswordScreen}
      component={NewChangePasswordScreen}
    />
  </Stack.Navigator>
);
