import React, { PropsWithChildren, useState } from 'react';

export const ExerciseCardContext = React.createContext({});

export const ExerciseCardProvider = ({ children }: PropsWithChildren<null>) => {
  const [cards, setCards] = useState([{}]);

  return (
    <ExerciseCardContext.Provider value={{ cards, setCards }}>
      {children}
    </ExerciseCardContext.Provider>
  );
};
