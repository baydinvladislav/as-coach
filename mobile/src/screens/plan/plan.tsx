import React, { useState } from 'react';

import { useFormik } from 'formik';
import moment from 'moment';

import { createPlan } from '@api';
import { RoutesProps, Screens, useNavigation } from '@navigation';
import { CustomerProps } from '@store';
import { createPlanValidationSchema } from '@utils';

import { TPlan } from '~types';

import { CreateExerciseScreen } from './create-exercise';
import { CreatePlanScreen } from './create-plan';
import { DayExercisesScreen } from './day-exercises';
import { Layout } from './layout';
import { NewDayScreen } from './new-day';
import { NewPlanScreen } from './new-plan';

export enum PlanScreens {
  CREATE_DATE_SCREEN = 'CreateDateScreen',
  CREATE_PLAN_SCREEN = 'CreatePlanScreen',
  CREATE_DAY_SCREEN = 'CreateDayScreen',
  CREATE_DAY_EXERCISES_SCREEN = 'CreateDayExercisesScreen',
  CREATE_EXERCISES_SCREEN = 'CreateExercisesScreen',
}

export const PlanScreen = ({ route }: RoutesProps) => {
  const { navigate } = useNavigation();
  const [currentScreen, setCurrentScreen] = useState(
    PlanScreens.CREATE_DATE_SCREEN,
  );

  const [params, setParams] = useState({});

  const customer = route.params as CustomerProps;

  const onSubmit = (values: TPlan) => {
    createPlan(customer.id, {
      ...values,
      start_date: moment(values.start_date, 'DD mmm ddd'),
      end_date: moment(values.end_date, 'DD mmm ddd'),
      diets: values.diets
        .map((diet, index) => {
          if (index !== 0 && !values.different_time) {
            return undefined;
          }
          return {
            carbs: Number(diet.carbs),
            fats: Number(diet.fats),
            proteins: Number(diet.proteins),
          };
        })
        .filter(item => item),
    }).then(() => navigate(Screens.DetailClient, { id: customer.id }));
  };

  const {
    handleChange,
    handleSubmit,
    errors,
    values,
    setValues,
    validateForm,
    setErrors,
  } = useFormik({
    initialValues: {
      // Server values
      diets: [{ proteins: '', fats: '', carbs: '' }],
      start_date: '',
      end_date: '',
      trainings: [],
      notes: '',
      set_rest: '0',
      exercise_rest: '0',

      // Locally values
      different_time: false,
    },
    onSubmit,
    validationSchema: createPlanValidationSchema,
    validateOnChange: false,
    validateOnBlur: false,
  });

  const clearErrors = () => {
    setErrors({});
  };

  const handleNavigate = (
    nextScreen: PlanScreens,
    params?: Record<string, any>,
    withValidate = false,
  ) => {
    if (!withValidate) {
      clearErrors();
      setCurrentScreen(nextScreen);
      setParams(params || {});
    }
    if (withValidate) {
      if (currentScreen === PlanScreens.CREATE_DATE_SCREEN) {
        validateForm().then(data => {
          if (
            !Object.keys(data).includes('start_date') &&
            !Object.keys(data).includes('end_date')
          ) {
            clearErrors();
            setCurrentScreen(nextScreen);
            setParams(params || {});
          }
        });
      } else if (currentScreen === PlanScreens.CREATE_DAY_SCREEN) {
        validateForm().then(data => {
          if (!Object.keys(data).includes('trainings')) {
            clearErrors();
            setCurrentScreen(nextScreen);
            setParams(params || {});
          }
        });
      } else if (currentScreen === PlanScreens.CREATE_DAY_EXERCISES_SCREEN) {
        validateForm().then(data => {
          if (!Object.keys(data).includes('trainings')) {
            clearErrors();
            setCurrentScreen(nextScreen);
            setParams(params || {});
          }
        });
      } else if (currentScreen === PlanScreens.CREATE_EXERCISES_SCREEN) {
        validateForm().then(data => {
          if (!Object.keys(data).includes('trainings')) {
            clearErrors();
            setCurrentScreen(nextScreen);
            setParams(params || {});
          }
        });
      } else {
        clearErrors();
        setCurrentScreen(nextScreen);
        setParams(params || {});
      }
    }
  };

  const formProps = {
    params,
    customer,
    values: values as unknown as TPlan,
    errors: errors as Record<string, any>,
    handleSubmit,
    handleNavigate,
    setValues: setValues as unknown as React.Dispatch<
      React.SetStateAction<TPlan>
    >,
    handleChange: handleChange as (
      e: string | React.ChangeEvent<any>,
    ) => () => void,
    clearErrors,
  };

  const renderScreen = () => {
    switch (currentScreen) {
      case PlanScreens.CREATE_DATE_SCREEN:
        return <NewPlanScreen {...formProps} />;

      case PlanScreens.CREATE_PLAN_SCREEN:
        return <CreatePlanScreen {...formProps} />;

      case PlanScreens.CREATE_DAY_SCREEN:
        return <NewDayScreen {...formProps} />;

      case PlanScreens.CREATE_DAY_EXERCISES_SCREEN:
        return <DayExercisesScreen {...formProps} />;

      case PlanScreens.CREATE_EXERCISES_SCREEN:
        return <CreateExerciseScreen {...formProps} />;
    }
  };

  return (
    <Layout
      isScroll={currentScreen === PlanScreens.CREATE_DATE_SCREEN ? false : true}
    >
      {renderScreen()}
    </Layout>
  );
};
