/**
 * Sample React Native App
 * https://github.com/facebook/react-native
 *
 * @format
 * @flow strict-local
 */
import React, { useRef, useState } from 'react';
import { StatusBar } from 'react-native';

import 'react-native-gesture-handler';

import { Screens, StackNavigator } from '@navigation';
import {
  DefaultTheme,
  NavigationContainer,
  NavigationContainerRef,
  useNavigationContainerRef,
} from '@react-navigation/native';
import { colors } from '@theme';
import { Layout } from '@ui';

const MyTheme = {
  ...DefaultTheme,
  colors: {
    ...DefaultTheme.colors,
    background: colors.transparent,
  },
};

const App = () => {
  const navigationRef = useNavigationContainerRef();
  const [currentScreen, setCurrentScreen] = useState<string>(
    Screens.WelcomeScreen,
  );
  const routeNameRef = useRef();

  return (
    <Layout {...ATTR(currentScreen)}>
      <NavigationContainer
        theme={MyTheme}
        ref={navigationRef}
        onReady={() => {
          routeNameRef.current = navigationRef.getCurrentRoute().name;
        }}
        onStateChange={async () => {
          const previousRouteName = routeNameRef.current;
          const currentRouteName = navigationRef.getCurrentRoute().name;

          if (previousRouteName !== currentRouteName) {
            setCurrentScreen(currentRouteName);
          }
        }}
      >
        <StatusBar barStyle="light-content" />
        <StackNavigator />
      </NavigationContainer>
    </Layout>
  );
};

const ATTR = (screen: string) => {
  switch (screen) {
    case Screens.WelcomeScreen:
      return {};

    case Screens.ProfileEditScreen:
      return { backgroundBlurRadius: 10, backgroundOpacity: 0.3, topOffset: 0 };

    default:
      return { backgroundBlurRadius: 10, backgroundOpacity: 0.3 };
  }
};

export default App;
