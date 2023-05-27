import React from 'react';
import { StyleSheet, View } from 'react-native';

import { colors, normVert } from '@theme';
import { Text } from '@ui';

import { FontSize, FontWeight } from '~types';

type TProps = {
  children: React.ReactNode;
  title: string;
};

export const CreatePlanItem = ({ children, title }: TProps) => (
  <View>
    <Text
      color={colors.white}
      weight={FontWeight.Bold}
      style={styles.title}
      fontSize={FontSize.S20}
    >
      {title}
    </Text>
    {children}
  </View>
);

const styles = StyleSheet.create({
  title: {
    marginTop: normVert(40),
    marginBottom: normVert(20),
  },
});
