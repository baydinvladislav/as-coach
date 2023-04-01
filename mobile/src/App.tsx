/**
 * Sample React Native App
 * https://github.com/facebook/react-native
 *
 * @format
 * @flow strict-local
 */
import React from 'react';
import { StatusBar } from 'react-native';

import 'react-native-gesture-handler';

import { StackNavigator } from '@navigation';
import { DefaultTheme, NavigationContainer } from '@react-navigation/native';
import { colors } from '@theme';

const MyTheme = {
  ...DefaultTheme,
  colors: {
    ...DefaultTheme.colors,
    background: colors.black,
  },
};

const App = () => (
  <NavigationContainer theme={MyTheme}>
    <StatusBar barStyle="light-content" />
    <StackNavigator />
  </NavigationContainer>
);

export default App;
