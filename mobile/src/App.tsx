/**
 * Sample React Native App
 * https://github.com/facebook/react-native
 *
 * @format
 * @flow strict-local
 */
import React, { useRef, useState } from 'react';

import 'moment/locale/ru';
import 'react-native-gesture-handler';
import { Edge, SafeAreaProvider } from 'react-native-safe-area-context';

import { Screens, StackNavigator } from '@navigation';
import {
  DefaultTheme,
  NavigationContainer,
  useNavigationContainerRef,
} from '@react-navigation/native';
import { colors } from '@theme';
import { Layout } from '@ui';

const App = () => {
  const navigationRef = useNavigationContainerRef();
  const [currentScreen, setCurrentScreen] = useState<string>(
    Screens.WelcomeScreen,
  );
  const routeNameRef = useRef();

  const MyTheme = {
    ...DefaultTheme,
    colors: {
      ...DefaultTheme.colors,
      background: colors.transparent,
    },
  };

  return (
    <SafeAreaProvider>
      <Layout {...ATTR(currentScreen)}>
        <NavigationContainer
          theme={MyTheme}
          ref={navigationRef}
          onReady={() => {
            routeNameRef.current = navigationRef.getCurrentRoute().name;
          }}
          onStateChange={async () => {
            const currentRouteName = navigationRef.getCurrentRoute().name;
            setCurrentScreen(currentRouteName);
          }}
        >
          <StackNavigator />
        </NavigationContainer>
      </Layout>
    </SafeAreaProvider>
  );
};

const ATTR = (screen: string) => {
  switch (screen) {
    case Screens.WelcomeScreen:
      return { edges: ['right', 'left', 'top', 'bottom'] as Edge[] };

    case Screens.ProfileEditScreen:
      return {
        backgroundBlurRadius: 10,
        backgroundOpacity: 0.3,
        edges: ['right', 'left'] as Edge[],
        style: { paddingHorizontal: 0 },
      };

    case Screens.LkScreen:
    case Screens.AddClientScreen:
    case Screens.PlanScreen:
    case Screens.DetailClient:
      return {
        backgroundBlurRadius: 10,
        backgroundOpacity: 0.3,
        edges: ['right', 'left'] as Edge[],
        style: { paddingHorizontal: 0 },
      };

    default:
      return {
        backgroundBlurRadius: 10,
        backgroundOpacity: 0.3,
        edges: ['right', 'left', 'top', 'bottom'] as Edge[],
      };
  }
};

export default App;
