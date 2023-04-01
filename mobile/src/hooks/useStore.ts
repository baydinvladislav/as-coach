import React from 'react';

import { StoresContext } from '../store/RootStore';

export const useStore = () => {
  const store = React.useContext(StoresContext);
  if (!store) {
    throw new Error('useStore must be used within a StoreProvider.');
  }
  return store;
};
