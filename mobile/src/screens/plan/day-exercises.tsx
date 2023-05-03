import React, { useCallback, useEffect, useState } from 'react';
import { StyleSheet, View } from 'react-native';

import { debounce, isEmpty } from 'lodash';
import { observer } from 'mobx-react';

import { AddIcon } from '@assets';
import { CheckboxGroup, NotFound, SearchInput } from '@components';
import { useStore } from '@hooks';
import { t } from '@i18n';
import { colors, normHor, normVert } from '@theme';
import { Button, Text, ViewWithButtons } from '@ui';

import { ButtonType, FontSize, TExercises, TPlan } from '~types';

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

export const DayExercisesScreen = observer(
  ({ handleNavigate, values, setValues, params, errors }: TProps) => {
    const [searchValue, setSearchValue] = useState<string | undefined>();

    const { loading, customer } = useStore();

    const isLoading = loading.isLoading;

    const [data, keys] = [
      Object.values(
        isEmpty(customer.searchExercises)
          ? customer.exercises
          : customer.searchExercises,
      ),
      Object.keys(
        isEmpty(customer.searchExercises)
          ? customer.exercises
          : customer.searchExercises,
      ),
    ];

    const dayName = values?.trainings?.[params.dayNumber]?.name;

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
          {t('newDay.exercisesTitle', {
            day: params.dayNumber + 1,
            exercises: dayName,
          })}
        </Text>
        <View style={styles.searchInput}>
          <SearchInput value={searchValue} onChangeText={setSearchValue} />
        </View>
        <Button
          style={styles.addExercisesButton}
          type={ButtonType.TEXT}
          onPress={() => handleNavigate(PlanScreens.CREATE_EXERCISE_SCREEN)}
          leftIcon={<AddIcon fill={colors.green} />}
        >
          {t('buttons.createExercises')}
        </Button>
        <ViewWithButtons
          style={{ justifyContent: 'space-between' }}
          onCancel={handleCancel}
          onConfirm={() =>
            handleNavigate(PlanScreens.CREATE_PLAN_SCREEN, undefined, true)
          }
          confirmText={t('buttons.next')}
          isLoading={isLoading}
          isScroll={true}
        >
          {!searchValue && data.length ? (
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
