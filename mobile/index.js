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
import { isIOS } from 'src/utils';

import App from './src/App';

ScrollView.defaultProps = ScrollView.defaultProps || {};
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
