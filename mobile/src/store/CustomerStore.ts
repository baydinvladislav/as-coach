import { action, computed, makeObservable, observable } from 'mobx';
import { createCustomer, getCustomers } from 'src/api/customer';

import { RootStore } from './RootStore';
import { actionLoading } from './action-loading';

export type CustomerProps = {
  id: string;
  first_name: string;
  last_name: string;
  phone_number: string;
};

export default class CustomerStore {
  rootStore: RootStore;

  constructor(root: RootStore) {
    this.rootStore = root;
    makeObservable(this);
  }

  @observable customers: CustomerProps[] = [];

  @action
  getCustomerById(id: string) {
    return this.customers.filter(customer => customer.id === id)[0];
  }

  @action
  @actionLoading()
  async getCustomers() {
    try {
      if (this.customers.length) {
        return;
      }
      const { data } = await getCustomers();
      this.customers = data;
    } catch (e) {
      console.warn(e);
      throw e;
    }
  }

  @action
  @actionLoading()
  async createCustomer(values: Partial<CustomerProps>) {
    try {
      const { data } = await createCustomer(values);
      this.customers = [...this.customers, data];
    } catch (e) {
      console.warn(e);
      throw e;
    }
  }
}
