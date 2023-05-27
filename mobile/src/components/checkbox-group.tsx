import React from 'react';
import { StyleProp, View, ViewStyle } from 'react-native';

import { CheckboxWithSets } from '@components';
import { colors } from '@theme';
import { Text } from '@ui';
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
  errors: Record<string, any>;
};

export const CheckboxGroup = ({
  style,
  data,
  title,
  setValues,
  dayName,
  values,
  dayNumber,
  errors,
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
            const exercise = values.trainings[dayNumber]?.exercises?.find(
              exercise => exercise.id === item.id,
            );
            return (
              <CheckboxWithSets
                key={item.id}
                placeholder={item.name}
                isFirst={key === 0}
                handlePress={() => handlePress(item.id)}
                exercise={exercise}
                errors={errors}
                handleChangeSets={e => handleChangeSets(item.id, e)}
                index={key}
              />
            );
          })
        : null}
    </View>
  );
};
