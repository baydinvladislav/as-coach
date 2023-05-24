import React, { useEffect } from 'react';
import { StyleSheet } from 'react-native';

import { observer } from 'mobx-react';

import { useStore } from '@hooks';
import { t } from '@i18n';
import { colors, normVert } from '@theme';
import { Input, Text, ViewWithButtons } from '@ui';

import { FontSize, TFormProps } from '~types';

import { PlanScreens } from './plan';

export const NewDayScreen = observer(
  ({
    handleNavigate,
    values,
    handleChange,
    params,
    setValues,
    errors,
  }: TFormProps) => {
    useEffect(() => {
      if (!params.isExists) {
        setValues(values => ({
          ...values,
          trainings: [...values.trainings, { name: '', exercises: [] }],
        }));
      }
      // eslint-disable-next-line react-hooks/exhaustive-deps
    }, []);

    const { loading } = useStore();

    const isLoading = loading.isLoading;

    const handleCancel = () => {
      if (!params.isExists) {
        setValues(values => ({
          ...values,
          trainings: values.trainings.filter(
            (_, key) => key !== params.dayNumber,
          ),
        }));
      } else {
        setValues(values => ({
          ...values,
          trainings: params.oldValue,
        }));
      }

      handleNavigate(PlanScreens.CREATE_PLAN_SCREEN);
    };

    return (
      <>
        <Text style={styles.title} color={colors.white} fontSize={FontSize.S24}>
          {t('newDay.title', { day: params.dayNumber + 1 })}
        </Text>
        <ViewWithButtons
          style={{ justifyContent: 'space-between' }}
          onCancel={handleCancel}
          onConfirm={() => {
            handleNavigate(
              PlanScreens.CREATE_DAY_EXERCISES_SCREEN,
              params,
              true,
            );
          }}
          confirmText={t('buttons.next')}
          isLoading={isLoading}
        >
          <Input
            placeholder="Название тренировки"
            value={values.trainings?.[params.dayNumber]?.name}
            onChangeText={handleChange(`trainings[${params.dayNumber}].name`)}
            error={errors.trainings?.[params.dayNumber]?.name}
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
