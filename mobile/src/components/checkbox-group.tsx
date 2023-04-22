import React from 'react';
import { StyleProp, StyleSheet, View, ViewStyle } from 'react-native';

import { Sets } from '@components';
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
  values: TPlan;
  dayNumber: number;
};

export const CheckboxGroup = ({
  style,
  data,
  title,
  setValues,
  dayName,
  values,
  dayNumber,
}: TProps) => {
  const handlePress = (id: string) => {
    setValues(values => addExerciseToPlan(values, dayName, id));
  };
  const handleChangeSets = (id: string, e: React.ChangeEvent<any>) => {
    setValues(values => addExerciseToPlan(values, dayName, id, e.target.value));
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
      {data.length
        ? data.map((item, key) => {
            const exercise = values.trainings[dayNumber].exercises?.find(
              exercise => exercise.id === item.id,
            );
            return (
              <React.Fragment key={dayNumber + item.id}>
                <Checkbox
                  style={[styles.checkbox, key !== 0 && styles.border]}
                  onChangeCheckbox={() => handlePress(item.id)}
                  placeholder={item.name}
                  value={Boolean(exercise)}
                />
                {exercise && (
                  <Sets
                    val={exercise?.sets}
                    onChangeText={e => handleChangeSets(item.id, e)}
                  />
                )}
              </React.Fragment>
            );
          })
        : null}
    </View>
  );
};

const styles = StyleSheet.create({
  checkbox: {
    paddingVertical: normVert(16),
  },
  border: {
    borderTopColor: colors.black3,
    borderTopWidth: 1,
  },
});
