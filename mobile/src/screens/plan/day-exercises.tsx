import React, { useCallback, useEffect, useState } from 'react';
import { StyleSheet, TouchableOpacity, View } from 'react-native';

import { debounce, isEmpty } from 'lodash';
import { observer } from 'mobx-react';
import styled from 'styled-components';

import { AddIcon } from '@assets';
import { CheckboxGroup, NotFound, SearchInput } from '@components';
import { useStore } from '@hooks';
import { t } from '@i18n';
import { useFocusEffect } from '@react-navigation/native';
import { colors, normHor, normVert } from '@theme';
import { Button, Text, ViewWithButtons } from '@ui';

import {
  ButtonType,
  FontSize,
  FontWeight,
  TExercises,
  TFormProps,
} from '~types';

import { PlanScreens } from './plan';

export const DayExercisesScreen = observer(
  ({ handleNavigate, values, setValues, params, errors }: TFormProps) => {
    const [searchInputKey, setSearchInputKey] = useState(0);

    const [searchValue, setSearchValue] = useState<string | undefined>();

    const { loading, customer } = useStore();

    const isLoading = loading.isLoading;

    const isEmptySearchExercises = isEmpty(customer.searchExercises);

    const clearSearch = () => {
      setSearchInputKey(key => key + 1);
      setSearchValue(undefined);
      customer.searchExercisesByName('');
    };

    const [data, keys] = [
      Object.values(
        isEmptySearchExercises ? customer.exercises : customer.searchExercises,
      ),
      Object.keys(
        isEmptySearchExercises ? customer.exercises : customer.searchExercises,
      ),
    ];

    const dayName = values?.trainings?.[params.dayNumber]?.name;
    const exercises = values?.trainings?.[params.dayNumber]?.exercises;

    // eslint-disable-next-line react-hooks/exhaustive-deps
    const search = useCallback(
      debounce(() => {
        customer.searchExercisesByName(searchValue);
      }, 200),
      [searchValue],
    );

    useEffect(() => {
      search();
    }, [search, searchValue]);

    // eslint-disable-next-line react-hooks/exhaustive-deps
    useFocusEffect(useCallback(() => () => clearSearch(), []));

    useEffect(() => {
      customer.getExercises();
      // eslint-disable-next-line react-hooks/exhaustive-deps
    }, []);

    const handleCancel = () => {
      clearSearch();
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

    const handleConfirm = () => {
      clearSearch();
      handleNavigate(PlanScreens.CREATE_SUPERSETS_SCREEN, params, true);
    };

    const isNotEmptyExercises =
      (data.length && !searchValue) || !isEmptySearchExercises;

    return (
      <>
        <Text
          style={styles.title}
          color={colors.white}
          fontSize={FontSize.S24}
          weight={FontWeight.Bold}
        >
          {t('newDay.exercisesTitle', {
            day: params.dayNumber + 1,
            exercises: dayName,
          })}
        </Text>
        <Text
          style={styles.exercisesText}
          color={colors.black4}
          fontSize={FontSize.S10}
          weight={FontWeight.Bold}
        >
          {t('createPlan.exercises')}
        </Text>
        <View style={styles.searchInput}>
          <SearchInput
            key={searchInputKey}
            value={searchValue}
            onChangeText={setSearchValue}
          />
        </View>
        <Button
          style={styles.addExercisesButton}
          type={ButtonType.TEXT}
          onPress={() =>
            handleNavigate(PlanScreens.CREATE_EXERCISE_SCREEN, params, true)
          }
          leftIcon={<AddIcon fill={colors.green} />}
        >
          {t('buttons.createExercises')}
        </Button>
        <ViewWithButtons
          style={{ justifyContent: 'space-between' }}
          containerStyle={isNotEmptyExercises ? {} : { flex: 1 }}
          onCancel={handleCancel}
          onConfirm={handleConfirm}
          confirmText={t('buttons.next')}
          isLoading={isLoading}
          isScroll={true}
          circles={
            exercises?.length ? (
              <Circle onPress={handleConfirm}>
                <Text>{exercises.length}</Text>
              </Circle>
            ) : null
          }
        >
          {isNotEmptyExercises ? (
            data.map((item: TExercises[], index) => (
              <CheckboxGroup
                style={styles.checkboxGroup}
                key={params.dayNumber + keys[index]}
                data={item}
                title={keys[index]}
                setValues={setValues}
                dayName={dayName}
                values={values}
                dayNumber={params.dayNumber}
                errors={errors?.trainings?.[params.dayNumber]}
              />
            ))
          ) : (
            <NotFound text={t('notFound.exercise')} />
          )}
        </ViewWithButtons>
      </>
    );
  },
);

const styles = StyleSheet.create({
  checkboxGroup: {
    marginTop: normVert(20),
  },
  exercisesText: {
    textTransform: 'uppercase',
    marginBottom: normVert(40),
    marginLeft: normHor(16),
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

const Circle = styled(TouchableOpacity)`
  position: absolute;
  z-index: 1;
  background-color: ${colors.green};
  right: ${normHor(22)}px;
  bottom: ${normVert(174)}px;
  border-radius: 100px;
  width: ${normHor(48)}px;
  height: ${normVert(48)}px;
  justify-content: center;
  align-items: center;
`;
