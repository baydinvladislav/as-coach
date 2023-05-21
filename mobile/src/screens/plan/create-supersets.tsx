import React from 'react';
import { StyleSheet, View } from 'react-native';

import { observer } from 'mobx-react';
import styled from 'styled-components';

import { Edit2Icon } from '@assets';
import { useStore } from '@hooks';
import { t } from '@i18n';
import { colors, normHor, normVert } from '@theme';
import { Button, ExerciseWithSuperset, Text, ViewWithButtons } from '@ui';

import { ButtonType, FontSize, TPlan } from '~types';

import { PlanScreens } from './plan';

type TProps = {
  handleNavigate: (
    nextScreen: PlanScreens,
    params?: Record<string, any>,
    withValidate?: boolean,
  ) => void;
  values: TPlan;
  handleChange: (e: string | React.ChangeEvent<any>) => () => void;
  setValues: React.Dispatch<React.SetStateAction<TPlan>>;
  params: Record<string, any>;
  errors: Record<string, any>;
};

export const CreateSupersetsScreen = observer(
  ({ handleNavigate, values, setValues, params, errors }: TProps) => {
    const { customer } = useStore();

    const handleCancel = () => {
      handleNavigate(PlanScreens.CREATE_DAY_EXERCISES_SCREEN, params);
    };

    const handleEdit = () => {
      handleNavigate(PlanScreens.EDIT_EXERCISES_SCREEN, params);
    };

    const exercises = values?.trainings?.[params.dayNumber]?.exercises;
    const dayName = values?.trainings?.[params.dayNumber]?.name;

    const quantity =
      exercises.length +
      exercises.reduce((acc, item) => (acc += item.supersets?.length || 0), 0);

    return (
      <>
        <View style={styles.row}>
          <Text
            style={styles.title}
            color={colors.white}
            fontSize={FontSize.S24}
          >
            {t('supersets.title', {
              quantity,
            })}
          </Text>
          <Button
            type={ButtonType.TEXT}
            onPress={handleEdit}
            leftIcon={<Edit2Icon fill={colors.green} />}
          >
            {t('buttons.edit')}
          </Button>
        </View>
        <Text
          style={styles.exercisesText}
          color={colors.black4}
          fontSize={FontSize.S10}
        >
          {t('supersets.dayTitle', {
            day: params.dayNumber + 1,
            name: dayName,
          })}
        </Text>
        <ViewWithButtons
          style={{ justifyContent: 'space-between' }}
          onCancel={handleCancel}
          onConfirm={() =>
            handleNavigate(PlanScreens.CREATE_PLAN_SCREEN, params, true)
          }
          confirmText={t('buttons.addExercises')}
          cancelText={t('buttons.moreExercises')}
          isScroll={true}
        >
          <ExerciseWithSuperset exercises={exercises} />
        </ViewWithButtons>
      </>
    );
  },
);

const styles = StyleSheet.create({
  row: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginLeft: normHor(16),
    marginRight: normHor(16),
  },
  exercisesText: {
    textTransform: 'uppercase',
    marginBottom: normVert(40),
    marginLeft: normHor(16),
  },
  title: {
    marginTop: normVert(14),
    marginBottom: normVert(16),
  },
});

const Line = styled(View)`
  background-color: ${colors.green};
  width: 1px;
  height: ${normVert(28)}px;
  position: absolute;
  bottom: ${normVert(78)}px;
  left: ${normHor(10)}px;
`;