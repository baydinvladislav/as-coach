import React, { useState } from 'react';

import { useFormik } from 'formik';
import { observer } from 'mobx-react';

import { createPlan } from '@api';
import { useStateCallback } from '@hooks';
import { RoutesProps, Screens, useNavigation } from '@navigation';
import { CustomerProps } from '@store';
import { ModalLayout } from '@ui';
import { createPlanValidationSchema } from '@utils';

import { TPlan } from '~types';

import { CreateExerciseScreen } from './create-exercise';
import { CreatePlanScreen } from './create-plan';
import { CreateSupersetsScreen } from './create-supersets';
import { DayExercisesScreen } from './day-exercises';
import { EditExercisesScreen } from './edit-exercises';
import { NewDayScreen } from './new-day';
import { NewPlanScreen } from './new-plan';

export enum PlanScreens {
  CREATE_DATE_SCREEN = 'CreateDateScreen',
  CREATE_PLAN_SCREEN = 'CreatePlanScreen',
  CREATE_DAY_SCREEN = 'CreateDayScreen',
  CREATE_DAY_EXERCISES_SCREEN = 'CreateDayExercisesScreen',
  CREATE_EXERCISE_SCREEN = 'CreateExerciseScreen',
  CREATE_SUPERSETS_SCREEN = 'CreateSupersetsScreen',
  EDIT_EXERCISES_SCREEN = 'EditExercisesScreen',
}

export const PlanScreen = observer(({ route }: RoutesProps) => {
  const { navigate } = useNavigation();
  const [currentScreen, setCurrentScreen] = useState(
    PlanScreens.CREATE_DATE_SCREEN,
  );

  const [isLoading, setIsLoading] = useStateCallback(false);

  const [params, setParams] = useState({});

  const customer = route.params as CustomerProps;

  const onSubmit = (values: TPlan) => {
    createPlan(customer.id, {
      ...values,
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
      set_rest: '120',
      exercise_rest: '180',

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
    if (withValidate) {
      setIsLoading(true, () => validate(nextScreen, params));
    } else {
      clearErrors();
      setCurrentScreen(nextScreen);
      setParams(params || {});
    }
  };

  const validate = (nextScreen: PlanScreens, params?: Record<string, any>) => {
    validateForm()
      .then(data => {
        if (currentScreen === PlanScreens.CREATE_DATE_SCREEN) {
          if (
            !Object.keys(data).includes('start_date') &&
            !Object.keys(data).includes('end_date')
          ) {
            clearErrors();
            setCurrentScreen(nextScreen);
            setParams(params || {});
          }
        } else if (currentScreen === PlanScreens.CREATE_DAY_SCREEN) {
          if (!Object.keys(data).includes('trainings')) {
            clearErrors();
            setCurrentScreen(nextScreen);
            setParams(params || {});
          }
        } else if (currentScreen === PlanScreens.CREATE_DAY_EXERCISES_SCREEN) {
          if (!Object.keys(data).includes('trainings')) {
            clearErrors();
            setCurrentScreen(nextScreen);
            setParams(params || {});
          }
        } else {
          clearErrors();
          setCurrentScreen(nextScreen);
          setParams(params || {});
        }
      })
      .finally(() => {
        setIsLoading(false);
      });
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
    isLoading,
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

      case PlanScreens.CREATE_EXERCISE_SCREEN:
        return <CreateExerciseScreen {...formProps} />;

      case PlanScreens.CREATE_SUPERSETS_SCREEN:
        return <CreateSupersetsScreen {...formProps} />;

      case PlanScreens.EDIT_EXERCISES_SCREEN:
        return <EditExercisesScreen {...formProps} />;
    }
  };

  return (
    <ModalLayout
      isScroll={currentScreen === PlanScreens.CREATE_DATE_SCREEN ? false : true}
    >
      {renderScreen()}
    </ModalLayout>
  );
});
