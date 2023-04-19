import React, { useState } from 'react';
import { StyleSheet, TouchableOpacity, View } from 'react-native';

import styled from 'styled-components';

import { ArrowDownIcon, ArrowUp2Icon, EditIcon } from '@assets';
import { useStore } from '@hooks';
import { t } from '@i18n';
import { colors, normHor, normVert } from '@theme';
import { Text } from '@ui';

import { FontSize, TPropsExercise } from '~types';

type TProps = {
  exercises: TPropsExercise;
  onEdit: () => void;
};

export const ExercisesCard = ({ exercises, onEdit }: TProps) => {
  const [isOpen, setIsOpen] = useState(false);

  const { customer } = useStore();

  return (
    <Container>
      <View style={[isOpen && styles.topContainer, styles.row]}>
        <View>
          <View style={[styles.row, { justifyContent: 'flex-start' }]}>
            <Text color={colors.white} fontSize={FontSize.S17}>
              {exercises.name}
            </Text>
            <Icon onPress={onEdit}>
              <EditIcon fill={colors.green} />
            </Icon>
          </View>
          <Text
            style={styles.exercisesText}
            color={colors.black4}
            fontSize={FontSize.S12}
          >
            {exercises.exercises.length} {t('createPlan.exercises')}
          </Text>
        </View>
        <Icon onPress={() => setIsOpen(isOpen => !isOpen)}>
          {isOpen ? <ArrowUp2Icon /> : <ArrowDownIcon />}
        </Icon>
      </View>
      {isOpen &&
        exercises.exercises?.map((exercise, key) => {
          const data = customer.getExerciseById(exercise.id);
          return (
            <View key={data.id} style={[styles.exercise, styles.row]}>
              <Text fontSize={FontSize.S12} color={colors.white}>
                {key + 1}. {data.name}
              </Text>
              <View style={styles.row}>
                {exercise.sets.map((set, key) => (
                  <React.Fragment key={key}>
                    <Text fontSize={FontSize.S12} color={colors.white}>
                      {set}
                    </Text>
                    {key !== exercise.sets.length - 1 && (
                      <Text fontSize={FontSize.S12} color={colors.green}>
                        ,{' '}
                      </Text>
                    )}
                  </React.Fragment>
                ))}
              </View>
            </View>
          );
        })}
    </Container>
  );
};

const styles = StyleSheet.create({
  exercisesText: {
    marginTop: normVert(10),
  },
  topContainer: {
    borderBottomColor: colors.grey7,
    borderBottomWidth: 1,
    paddingBottom: normVert(16),
    marginBottom: normVert(4),
  },
  exercise: {
    marginTop: normVert(12),
  },
  row: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
});

const Container = styled(View)`
  background-color: ${colors.black3};
  border-radius: 12px;
  width: 100%;
  padding-vertical: ${normVert(16)}px;
  padding-horizontal: ${normHor(16)}px;
  margin-bottom: ${normVert(19)}px;
`;

const Icon = styled(TouchableOpacity)`
  margin-left: ${normHor(13)}px;
`;
