import { useNavigation as useNativeNavigation } from '@react-navigation/native';
import type { ParamListBase } from '@react-navigation/native';
import { NativeStackNavigationProp } from '@react-navigation/native-stack';

export enum Screens {
  WelcomeScreen = 'WelcomeScreen',
  RegistrationScreen = 'RegistrationScreen',
  LoginScreen = 'LoginScreen',
}

type Routes = Screens;

export const useNavigation = () =>
  useNativeNavigation<NativeStackNavigationProp<ParamListBase, Routes>>();
