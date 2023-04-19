import React from 'react';
import { StyleSheet } from 'react-native';

import { observer } from 'mobx-react';

import { useStore } from '@hooks';
import { t } from '@i18n';
import { colors, normVert } from '@theme';
import { Input, Text, ViewWithButtons } from '@ui';

import { FontSize, TPlan } from '~types';

import { PlanScreens } from './plan';

type TProps = {
  values: TPlan;
  handleChange: (e: string | React.ChangeEvent<any>) => () => void;
  handleNavigate: (
    nextScreen: PlanScreens,
    params?: Record<string, any>,
  ) => void;
  params: Record<string, any>;
};

export const NewDayScreen = observer(
  ({ handleNavigate, values, handleChange, params }: TProps) => {
    const { loading } = useStore();

    const isLoading = loading.isLoading;

    return (
      <>
        <Text style={styles.title} color={colors.white} fontSize={FontSize.S24}>
          {t('newDay.title', { day: params.dayNumber + 1 })}
        </Text>
        <ViewWithButtons
          style={{ justifyContent: 'space-between' }}
          onCancel={() => handleNavigate(PlanScreens.CREATE_PLAN_SCREEN)}
          onConfirm={() => {
            handleNavigate(PlanScreens.CREATE_DAY_EXERCISES_SCREEN, params);
          }}
          confirmText={t('buttons.next')}
          isLoading={isLoading}
        >
          <Input
            placeholder="Название тренировки"
            value={values.trainings?.[params.dayNumber]?.name}
            onChangeText={handleChange(`trainings[${params.dayNumber}].name`)}
          />
        </ViewWithButtons>
      </>
    );
  },
);

const styles = StyleSheet.create({
  title: {
    marginTop: normVert(14),
    marginBottom: normVert(20),
    marginLeft: normVert(16),
  },
});
