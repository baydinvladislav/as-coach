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
  const { customer } = useStore();
  const isFromServer = exercises[0].superset_id !== undefined;
  return (
    <>
      {exercises.map((exercise, key, arr) => {
        const { name } = customer.getExerciseById(exercise.id);
        const supersets = exercise.supersets;

        const isFirstInSuperset =
          (exercise.supersets && supersets?.[0] !== exercise.id) ||
          (arr[key - 1] && exercise.superset_id === arr[key - 1]?.superset_id);

        const isHasLine = isFromServer
          ? isFirstInSuperset
          : exercise?.supersets?.length &&
            exercise.supersets[0] !== exercise.id;
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
