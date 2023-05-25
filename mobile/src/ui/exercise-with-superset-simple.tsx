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

  return (
    <>
      {exercises.map((exercise, key, arr) => {
        const { name } = customer.getExerciseById(exercise.id);
        const lastIndexSuperset = exercise.supersets?.length || 0;
        const lastIndexExercises = arr.length + lastIndexSuperset + 1;
        const index =
          arr.slice(0, key).length +
          arr
            .slice(0, key)
            .reduce((acc, item) => (acc += item.supersets?.length || 0), 0);
        return (
          <React.Fragment key={key}>
            <ExerciseInfo
              type={ExerciseCardType.SIMPLE}
              name={name}
              index={index}
              isLast={
                Boolean(exercise?.supersets?.length) ||
                key === exercises.length - 1
              }
              exercises={exercise}
            />
            {exercise.supersets?.map?.((superset, i) => {
              const { name } = customer.getExerciseById(superset);

              return (
                <View key={i}>
                  <Line />
                  <ExerciseInfo
                    type={ExerciseCardType.SIMPLE}
                    name={name}
                    key={i}
                    index={i + index + 1}
                    isLast={
                      index !== lastIndexExercises &&
                      i + 2 === lastIndexSuperset
                    }
                    exercises={exercise}
                  />
                </View>
              );
            })}
          </React.Fragment>
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
