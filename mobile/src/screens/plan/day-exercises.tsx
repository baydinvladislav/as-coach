import React, { useState } from 'react';
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
  handleNavigate: (nextScreen: PlanScreens) => void;
  values: TPlan;
  handleChange: (e: string | React.ChangeEvent<any>) => () => void;
  setValues: React.Dispatch<React.SetStateAction<TPlan>>;
};

export const DayExercisesScreen = observer(
  ({ handleNavigate, values, setValues }: TProps) => {
    const [dayNumber] = useState(values.trainings.length);
    const { loading, customer } = useStore();

    const isLoading = loading.isLoading;

    const [data, keys] = [
      Object.values(customer.exercises),
      Object.keys(customer.exercises),
    ];

    const dayName = values.trainings[dayNumber - 1].name;

    return (
      <>
        <Text style={styles.title} color={colors.white} fontSize={FontSize.S24}>
          {t('newDay.exercisesTitle', {
            day: dayNumber,
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
          leftIcon={<AddIcon stroke={colors.green} />}
        >
          {t('buttons.createExercises')}
        </Button>
        <ViewWithButtons
          style={{ justifyContent: 'space-between' }}
          onCancel={() => handleNavigate(PlanScreens.CREATE_DAY_SCREEN)}
          onConfirm={() => handleNavigate(PlanScreens.CREATE_PLAN_SCREEN)}
          confirmText={t('buttons.next')}
          isLoading={isLoading}
          isScroll={true}
        >
          {data.map((item: any, index) => (
            <CheckboxGroup
              style={styles.checkboxGroup}
              key={keys[index]}
              data={item}
              title={keys[index]}
              setValues={setValues}
              dayName={dayName}
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
