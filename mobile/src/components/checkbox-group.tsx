import React from 'react';
import { StyleProp, StyleSheet, View, ViewStyle } from 'react-native';

import { colors, normVert } from '@theme';
import { Checkbox, Text } from '@ui';

import { FontSize } from '~types';

type TProps = {
  title: string;
  style?: StyleProp<ViewStyle>;
  data: {
    id: number;
    value: boolean;
    placeholder: string;
  }[];
};

export const CheckboxGroup = ({ style, data, title }: TProps) => (
  <View style={style}>
    <Text
      style={{ textTransform: 'uppercase' }}
      fontSize={FontSize.S10}
      color={colors.grey4}
    >
      {title}
    </Text>
    {data.map(item => (
      <Checkbox
        style={styles.checkbox}
        key={item.id}
        value={item.value}
        onChangeCheckbox={() => console.log(123)}
        placeholder={item.placeholder}
      />
    ))}
  </View>
);

const styles = StyleSheet.create({
  checkbox: {
    paddingVertical: normVert(16),
  },
});
