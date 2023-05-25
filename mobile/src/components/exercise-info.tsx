import React from 'react';
import { ScrollView, StyleSheet, View } from 'react-native';

import styled from 'styled-components';

import { colors, normHor, normVert } from '@theme';
import { Text } from '@ui';

import {
  ExerciseCardType,
  FontSize,
  FontWeight,
  TPropsExercises,
} from '~types';

type TProps = {
  name: string;
  exercises: TPropsExercises;
  index: number;
  isLast: boolean;
  type: ExerciseCardType;
};

export const ExerciseInfo = ({
  exercises,
  index,
  name,
  isLast,
  type,
}: TProps) => (
  <View style={[styles.row, styles.exercise]}>
    <Number type={type}>
      <Text fontSize={FontSize.S16} color={colors.white}>
        {index + 1}
      </Text>
    </Number>
    <Column isLast={isLast}>
      <Text
        fontSize={FontSize.S16}
        weight={
          type === ExerciseCardType.FULL
            ? FontWeight.Regular
            : FontWeight.Medium
        }
        color={colors.white}
      >
        {name}
      </Text>
      <ScrollView
        horizontal={true}
        contentContainerStyle={[styles.row, styles.sets]}
      >
        {exercises.sets.map((set, index) => (
          <React.Fragment key={index}>
            <Text
              fontSize={
                type === ExerciseCardType.FULL ? FontSize.S17 : FontSize.S16
              }
              color={colors.black5}
            >
              {set}
            </Text>
            {index !== exercises.sets.length - 1 && (
              <Text
                fontSize={
                  type === ExerciseCardType.FULL ? FontSize.S17 : FontSize.S16
                }
                color={
                  type === ExerciseCardType.FULL ? colors.green : colors.white
                }
              >
                ,{' '}
              </Text>
            )}
          </React.Fragment>
        ))}
      </ScrollView>
    </Column>
  </View>
);

const styles = StyleSheet.create({
  exercise: {
    marginTop: normVert(12),
    justifyContent: 'flex-start',
    alignItems: 'flex-start',
  },
  row: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  sets: {
    marginTop: normVert(7),
  },
});

const Number = styled(View)<{ type: ExerciseCardType }>`
  border: ${({ type }) =>
    type === ExerciseCardType.FULL ? `1px solid ${colors.black4}` : 'none'};
  border-radius: 100px;
  width: ${normHor(22)}px;
  height: ${normVert(22)}px;
  align-items: center;
  justify-content: center;
  margin-right: ${normHor(12)}px;
  margin-top: ${({ type }) =>
    type === ExerciseCardType.FULL ? 0 : normVert(14)}px;
`;

const Column = styled(View)<{ isLast: boolean }>`
  margin-top: ${normVert(4)}px;
  align-items: flex-start;
  border-bottom-color: ${colors.black3};
  border-bottom-width: ${({ isLast }) => (isLast ? 0 : 1)}px;
  padding-bottom: ${normVert(18)}px;
  width: ${normHor(247)}px;
`;
