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

Text.defaultProps = Text.defaultProps || {};
Text.defaultProps.maxFontSizeMultiplier = 1.2;
TextInput.defaultProps = TextInput.defaultProps || {};
TextInput.defaultProps.maxFontSizeMultiplier = 1.2;
ScrollView.defaultProps = ScrollView.defaultProps || {};
ScrollView.defaultProps.bounces = false;
ScrollView.defaultProps.showsVerticalScrollIndicator = false;
ScrollView.defaultProps.showsHorizontalScrollIndicator = false;
ScrollView.defaultProps.overScrollMode = 'never';
ScrollView.defaultProps.keyboardShouldPersistTaps = 'handled';

if (!isIOS) {
  StatusBar.setTranslucent(true);
  StatusBar.setBackgroundColor('transparent');
}
const headlessCheck = ({ isHeadless }) => (isHeadless ? null : <App />);

AppRegistry.registerComponent(appName, () => (isIOS ? headlessCheck : App));
