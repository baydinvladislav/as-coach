/**
 * @format
 */
import React from 'react';
import {
  AppRegistry,
  ScrollView,
  StatusBar,
  Text,
  TextInput,
} from 'react-native';

import { name as appName } from 'app.json';
import 'react-native-gesture-handler';
import overrideColorScheme from 'react-native-override-color-scheme';
import { isIOS } from 'src/utils';

import App from './src/App';

const ignoreWarns = [
  'VirtualizedLists should never be nested inside plain ScrollViews',
];

const errorWarn = global.console.error;
global.console.error = (...arg) => {
  for (const error of ignoreWarns) {
    if (arg[0].startsWith(error)) {
      return;
    }
  }
  errorWarn(...arg);
};

overrideColorScheme.setScheme('dark');

TextInput.defaultProps = TextInput.defaultProps || {};
Text.defaultProps = Text.defaultProps || {};
ScrollView.defaultProps = ScrollView.defaultProps || {};
Text.defaultProps.allowFontScaling = false;
TextInput.defaultProps.allowFontScaling = false;
ScrollView.defaultProps.bounces = false;
ScrollView.defaultProps.showsVerticalScrollIndicator = false;
ScrollView.defaultProps.showsHorizontalScrollIndicator = false;
ScrollView.defaultProps.overScrollMode = 'never';

if (isIOS) {
  StatusBar.setBarStyle('light-content');
} else {
  StatusBar.setTranslucent(true);
  StatusBar.setBackgroundColor('transparent');
}

const headlessCheck = ({ isHeadless }) => (isHeadless ? null : <App />);

AppRegistry.registerComponent(appName, () => (isIOS ? headlessCheck : App));
