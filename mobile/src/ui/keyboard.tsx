import React from 'react';
import { ScrollView, StyleProp, ViewStyle } from 'react-native';

import { AvoidSoftInput } from 'react-native-avoid-softinput';

import { useFocusEffect } from '@react-navigation/native';
import { normVert } from '@theme';
import { isIOS } from '@utils';

type TProps = {
  children: React.ReactNode;
  style?: StyleProp<ViewStyle>;
};

export const Keyboard = ({ children, style }: TProps) => {
  const onFocusEffect = React.useCallback(() => {
    AvoidSoftInput.setEasing('easeIn');
    AvoidSoftInput.setEnabled(true);
    if (isIOS) AvoidSoftInput.setAvoidOffset(normVert(-30));
    AvoidSoftInput.setShouldMimicIOSBehavior(true);

    return () => {
      AvoidSoftInput.setEasing('easeOut');
      AvoidSoftInput.setEnabled(false);
      if (isIOS) AvoidSoftInput.setAvoidOffset(0);
      AvoidSoftInput.setShouldMimicIOSBehavior(false);
    };
  }, []);

  useFocusEffect(onFocusEffect);
  return <ScrollView contentContainerStyle={style}>{children}</ScrollView>;
};
