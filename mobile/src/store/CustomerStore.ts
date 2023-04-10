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
  @observable searchCustomers: CustomerProps[] = [];

  @action
  setCustomer(data: CustomerProps[]) {
    this.customers = [...this.customers, ...data];
  }

  @action
  setSearchCustomer(data: CustomerProps[]) {
    this.searchCustomers = [...data];
  }

  @action
  searchCustomerByName(searchValue?: string) {
    this.setSearchCustomer(
      searchValue
        ? this.customers.filter(
            customer =>
              customer.first_name.includes(searchValue) ||
              customer.last_name.includes(searchValue),
          )
        : this.customers,
    );
  }

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
      this.setCustomer(data);
      this.setSearchCustomer(data);
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
      this.setCustomer([data]);
    } catch (e) {
      console.warn(e);
      throw e;
    }
  }
}
