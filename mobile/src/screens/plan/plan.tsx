import React, { useState } from 'react';

import { useFormik } from 'formik';
import moment from 'moment';

import { createPlan } from '@api';
import { RoutesProps, Screens, useNavigation } from '@navigation';
import { CustomerProps } from '@store';
import { ModalLayout } from '@ui';
import { createPlanValidationSchema } from '@utils';

import { TPlan } from '~types';

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
  CREATE_EXERCISES_SCREEN = 'CreateExercisesScreen',
  CREATE_SUPERSETS_SCREEN = 'CreateSupersetsScreen',
  EDIT_EXERCISES_SCREEN = 'EditExercisesScreen',
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
      start_date: '05.05.2023',
      end_date: '05.05.2023',
      trainings: [
        {
          name: 'test',
          exercises: [
            {
              id: '4283c861-eb38-4be6-ad5a-0d48f54e9415',
              sets: ['12', '12', '12'],
            },
            {
              id: '7860b296-fe24-4541-84d8-576e4698b7c5',
              sets: ['12', '12', '12'],
              supersets: [
                '33ecc6de-dfc1-4dfb-a07b-637f769e9095',
                '5414ead9-5d9c-4cee-b4c4-48eebad6f0a5',
              ],
            },
            {
              id: '7ea243a7-356a-443e-ac44-697320be8f08',
              sets: ['12', '12', '12'],
            },
            {
              id: '9b811d46-3efc-4ad2-8393-f2633014fa5d',
              sets: ['12', '12', '12'],
              supersets: ['844aa04d-d264-4799-a12a-43de7ea03b43'],
            },
            {
              id: '8832fd62-ed9a-4c2a-83f5-ae02bac14f3a',
              sets: ['12', '12', '12'],
            },
          ],
        },
      ],
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
};
