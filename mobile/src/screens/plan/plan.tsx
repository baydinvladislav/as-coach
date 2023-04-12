import React, { useState } from 'react';
import { View } from 'react-native';

import { CreatePlanScreen } from './create-plan';
import { NewPlanScreen } from './new-plan';

export const PlanScreen = () => {
  const [current, setCurrent] = useState(0);

  const handleNext = () => {
    setCurrent(current => current + 1);
  };

  const handlePrev = () => {
    setCurrent(current => current - 1);
  };

  return (
    <>
      {current === 0 && (
        <NewPlanScreen onNext={handleNext} onPrev={handlePrev} />
      )}
      {current === 1 && (
        <CreatePlanScreen onNext={handleNext} onPrev={handlePrev} />
      )}
    </>
  );
};
