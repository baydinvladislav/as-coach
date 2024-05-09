import React from 'react';
import { View } from 'react-native';

import styled from 'styled-components';

import { ExerciseInfo } from '@components';
import { useStore } from '@hooks';
import { colors, normHor, normVert } from '@theme';

import { ExerciseCardType, TPropsExercises } from '~types';

type TProps = {
  exercises: TPropsExercises[];
};

export const ExerciseWithSupersetSimple = ({ exercises }: TProps) => {
  const CheckFirstInSuperset = (
    current: TPropsExercises,
    previous?: TPropsExercises,
  ): boolean => {
    if (current.superset_id === undefined || current.superset_id === 'None') {
      return false;
    }

    return !!(
      previous &&
      previous.superset_id != undefined &&
      current.superset_id == previous.superset_id
    );
  };

  return (
    <>
      {exercises.map((exercise, key) => {
        const name = exercise.name;
        const supersets = exercise.supersets;

        const isHasLine = CheckFirstInSuperset(exercise, exercises[key - 1]);
        return (
          <View key={key}>
            {isHasLine && <Line />}
            <ExerciseInfo
              type={ExerciseCardType.SIMPLE}
              name={name}
              index={key}
              isLast={
                Boolean(supersets?.length) || key === exercises.length - 1
              }
              exercises={exercise}
            />
          </View>
        );
      })}
    </>
  );
};

const Line = styled(View)`
  background-color: ${colors.black4};
  width: 1px;
  height: ${normVert(24)}px;
  position: absolute;
  bottom: ${normVert(68)}px;
  left: ${normHor(10)}px;
  border-radius: 100px;
`;
