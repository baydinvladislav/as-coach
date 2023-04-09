import React from 'react';

import { observer } from 'mobx-react-lite';
import { SmsScreen } from 'src/screens/auth/sms';

import { useStore } from '@hooks';
import { Screens } from '@navigation';
import { createStackNavigator } from '@react-navigation/stack';
import {
  AddClientScreen,
  ChangePasswordScreen,
  LkScreen,
  LoginScreen,
  NewChangePasswordScreen,
  ProfileEditScreen,
  ProfileScreen,
  RegistrationScreen,
  WelcomeScreen,
} from '@screens';

const GuestStack = createStackNavigator();
const UserStack = createStackNavigator();

export const StackNavigator = observer(() => {
  const { user } = useStore();

  const isGuest = !!user.hasAccess; // меняем !user.hasAccess на !!!user.hasAccess для разработки. Чтобы открывался сразу лк

  return isGuest ? (
    <GuestStack.Navigator
      initialRouteName={Screens.WelcomeScreen}
      screenOptions={{
        headerShown: false,
        animationEnabled: false,
      }}
    >
      <GuestStack.Screen
        name={Screens.WelcomeScreen}
        component={WelcomeScreen}
      />
      <GuestStack.Screen
        name={Screens.RegistrationScreen}
        component={RegistrationScreen}
      />
      <GuestStack.Screen name={Screens.LoginScreen} component={LoginScreen} />
      <GuestStack.Screen name={Screens.SmsScreen} component={SmsScreen} />
    </GuestStack.Navigator>
  ) : (
    <UserStack.Navigator
      initialRouteName={Screens.LkScreen}
      screenOptions={{ headerShown: false, animationEnabled: false }}
    >
      <UserStack.Screen name={Screens.LkScreen} component={LkScreen} />
      <UserStack.Screen
        options={{
          presentation: 'modal',
          animationEnabled: true,
        }}
        name={Screens.AddClientScreen}
        component={AddClientScreen}
      />
      <UserStack.Screen name={Screens.SmsScreen} component={SmsScreen} />
      <UserStack.Screen
        name={Screens.ProfileScreen}
        component={ProfileScreen}
      />
      <UserStack.Screen
        name={Screens.ProfileEditScreen}
        component={ProfileEditScreen}
      />
      <UserStack.Screen
        name={Screens.ChangePasswordScreen}
        component={ChangePasswordScreen}
      />
      <UserStack.Screen
        name={Screens.NewChangePasswordScreen}
        component={NewChangePasswordScreen}
      />
    </UserStack.Navigator>
  );
});
