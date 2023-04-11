import React from 'react';
import { StyleSheet, View } from 'react-native';

import { colors, normVert } from '@theme';
import { Text } from '@ui';

import { FontSize } from '~types';

type TProps = {
  children: React.ReactNode;
  title: string;
};

export const CreatePlanItem = ({ children, title }: TProps) => (
  <View>
    <Text color={colors.white} style={styles.title} fontSize={FontSize.S24}>
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
