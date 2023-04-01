import React from 'react';

import { LoadingStore } from './LoadingStore';
import UserStore from './UserStore';

export class RootStore {
  user: UserStore;
  loading: LoadingStore;
  constructor() {
    this.user = new UserStore(this);
    this.loading = new LoadingStore();
  }
}

export const StoresContext = React.createContext(new RootStore());
