import React, { useState } from 'react';

import { useFormik } from 'formik';

import { CreatePlanScreen } from './create-plan';
import { DayExercisesScreen } from './day-exercises';
import { Layout } from './layout';
import { NewDayScreen } from './new-day';
import { NewPlanScreen } from './new-plan';

export const PlanScreen = () => {
  const [current, setCurrent] = useState(0);

  const handleNext = () => {
    setCurrent(current => current + 1);
  };

  const handlePrev = () => {
    setCurrent(current => current - 1);
  };

  const onSubmit = (values: any) => {
    console.log('submit', values);
    if (current === 0) {
      handleNext();
    } else if (current === 1) {
      handleNext();
    } else if (current === 2) {
      handleNext();
    } else if (current === 3) {
      console.log('end');
    }
  };

  const { handleChange, handleSubmit, values } = useFormik({
    initialValues: {
      start_date: '',
      end_date: '',
      different_time: false,
      squirrels1: '',
      fats1: '',
      carbohydrates1: '',
      squirrels2: '',
      fats2: '',
      carbohydrates2: '',
      days: [{ rest1: '0', rest2: '0' }],
      notes: '',
    },
    onSubmit,
    validateOnChange: false,
    validateOnBlur: false,
  });

  const formProps = {
    values,
    handleSubmit,
    handleChange: handleChange as (
      e: string | React.ChangeEvent<any>,
    ) => () => void,
  };

  return (
    <Layout>
      {current === 0 && <NewPlanScreen {...formProps} />}
      {current === 1 && <CreatePlanScreen {...formProps} onPrev={handlePrev} />}
      {current === 2 && <NewDayScreen {...formProps} onPrev={handlePrev} />}
      {current === 3 && (
        <DayExercisesScreen {...formProps} onPrev={handlePrev} />
      )}
    </Layout>
  );
};
