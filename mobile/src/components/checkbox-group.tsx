import React from 'react';
import { StyleProp, StyleSheet, View, ViewStyle } from 'react-native';

import { colors, normVert } from '@theme';
import { Checkbox, Text } from '@ui';
import { addExerciseToPlan } from '@utils';

import { FontSize, TExercises, TPlan } from '~types';

type TProps = {
  title: string;
  style?: StyleProp<ViewStyle>;
  data: TExercises[];
  setValues: React.Dispatch<React.SetStateAction<TPlan>>;
  dayName: string;
};

export const CheckboxGroup = ({
  style,
  data,
  title,
  setValues,
  dayName,
}: TProps) => {
  const handlePress = (id: string) => {
    setValues(values => addExerciseToPlan(values, dayName, id));
  };

  return (
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
          value={false}
          onChangeCheckbox={() => handlePress(item.id)}
          placeholder={item.name}
        />
      ))}
    </View>
  );
};

const styles = StyleSheet.create({
  checkbox: {
    paddingVertical: normVert(16),
  },
});
