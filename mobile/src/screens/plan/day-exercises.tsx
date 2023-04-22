import React from 'react';
import { StyleSheet, View } from 'react-native';

import { observer } from 'mobx-react';

import { AddIcon } from '@assets';
import { CheckboxGroup, SearchInput } from '@components';
import { useStore } from '@hooks';
import { t } from '@i18n';
import { colors, normHor, normVert } from '@theme';
import { Button, Text, ViewWithButtons } from '@ui';

import { ButtonType, FontSize, TPlan } from '~types';

import { PlanScreens } from './plan';

type TProps = {
  handleNavigate: (
    nextScreen: PlanScreens,
    params?: Record<string, any>,
  ) => void;
  values: TPlan;
  handleChange: (e: string | React.ChangeEvent<any>) => () => void;
  setValues: React.Dispatch<React.SetStateAction<TPlan>>;
  params: Record<string, any>;
};

export const DayExercisesScreen = observer(
  ({ handleNavigate, values, setValues, params }: TProps) => {
    const { loading, customer } = useStore();

    const isLoading = loading.isLoading;

    const [data, keys] = [
      Object.values(customer.exercises),
      Object.keys(customer.exercises),
    ];

    const dayName = values.trainings[params.dayNumber].name;

    return (
      <>
        <Text style={styles.title} color={colors.white} fontSize={FontSize.S24}>
          {t('newDay.exercisesTitle', {
            day: params.dayNumber + 1,
            exercises: dayName,
          })}
        </Text>
        <View style={styles.searchInput}>
          <SearchInput />
        </View>
        <Button
          style={styles.addExercisesButton}
          type={ButtonType.TEXT}
          onPress={() => handleNavigate(PlanScreens.CREATE_EXERCISES_SCREEN)}
          leftIcon={<AddIcon fill={colors.green} />}
        >
          {t('buttons.createExercises')}
        </Button>
        <ViewWithButtons
          style={{ justifyContent: 'space-between' }}
          onCancel={() => handleNavigate(PlanScreens.CREATE_DAY_SCREEN, params)}
          onConfirm={() => handleNavigate(PlanScreens.CREATE_PLAN_SCREEN)}
          confirmText={t('buttons.next')}
          isLoading={isLoading}
          isScroll={true}
        >
          {data.map((item: any, index) => (
            <CheckboxGroup
              style={styles.checkboxGroup}
              key={params.dayNumber + keys[index]}
              data={item}
              title={keys[index]}
              setValues={setValues}
              dayName={dayName}
              values={values}
              dayNumber={params.dayNumber}
            />
          ))}
        </ViewWithButtons>
      </>
    );
  },
);

const styles = StyleSheet.create({
  checkboxGroup: {
    marginTop: normVert(20),
  },
  title: {
    marginTop: normVert(14),
    marginBottom: normVert(16),
    marginLeft: normHor(16),
  },
  addExercisesButton: {
    marginRight: 'auto',
    marginLeft: normHor(16),
    marginBottom: normVert(20),
  },
  searchInput: {
    marginBottom: normVert(20),
    marginHorizontal: normHor(16),
  },
});
