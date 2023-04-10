import React from 'react';

import CustomerStore from './CustomerStore';
import { LoadingStore } from './LoadingStore';
import UserStore from './UserStore';

export class RootStore {
  user: UserStore;
  loading: LoadingStore;
  customer: CustomerStore;
  constructor() {
    this.user = new UserStore(this);
    this.loading = new LoadingStore();
    this.customer = new CustomerStore(this);
  }
}

export const StoresContext = React.createContext(new RootStore());
