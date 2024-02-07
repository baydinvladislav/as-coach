import { action, makeObservable, observable } from 'mobx';

import {
  createCustomer,
  getCustomerPlan,
  getCustomers,
  getExercises,
} from '@api';

import { TExercisesEdited, TPlanType } from '~types';

import { RootStore } from './RootStore';
import { actionLoading } from './action-loading';

export type CustomerProps = {
  id: string;
  first_name: string;
  last_name: string;
  phone_number: string;
  plans: TPlanType[];
  last_plan_end_date: string;
};

export default class CustomerStore {
  rootStore: RootStore;

  constructor(root: RootStore) {
    this.rootStore = root;
    makeObservable(this);
  }

  @observable exercises: TExercisesEdited = {};
  @observable searchExercises: TExercisesEdited = {};
  @observable customers: CustomerProps[] = [];
  @observable searchCustomers: CustomerProps[] = [];

  @action
  setInitialCustomers() {
    this.setCustomer([]);
    this.setSearchCustomer([]);
  }

  @action
  setCustomer(data: CustomerProps[]) {
    this.customers = data;
  }

  @action
  setExercises(data: TExercisesEdited) {
    this.exercises = data;
  }

  @action
  getExerciseById(id: string) {
    return Object.values(this.exercises)
      .flat(1)
      .filter(exercise => exercise.id === id)[0];
  }

  @action
  setSearchExercises(data: TExercisesEdited) {
    this.searchExercises = data;
  }

  @action
  searchExercisesByName(searchValue?: string) {
    if (searchValue) {
      const result: Record<string, any> = {};
      for (const key in this.exercises) {
        for (const i in this.exercises[key]) {
          if (this.exercises[key][i].name.includes(searchValue)) {
            result[key] = [this.exercises[key][i]];
          }
        }
      }
      this.setSearchExercises(result);
    } else {
      this.setSearchExercises({});
    }
  }

  @action
  setSearchCustomer(data: CustomerProps[]) {
    this.searchCustomers = data;
  }

  @action
  searchCustomerByName(searchValue?: string) {
    if (searchValue) {
      this.setSearchCustomer(
        this.customers.filter(
          customer =>
            customer.first_name.includes(searchValue) ||
            customer.last_name.includes(searchValue),
        ),
      );
    } else {
      this.setSearchCustomer([]);
    }
  }

  @action
  getCustomerById(id: string) {
    return this.customers.filter(customer => customer.id === id)[0];
  }

  @action
  @actionLoading()
  async getCustomerPlanById(id: string) {
    try {
      const { data } = await getCustomerPlan(id);
      return data;
    } catch (e) {
      console.warn(e);
    }
  }

  @action
  @actionLoading()
  async getCustomers() {
    try {
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
      this.setCustomer([data, ...this.customers]);
      this.setSearchCustomer(this.customers);
    } catch (e) {
      console.warn(e);
      throw e;
    }
  }

  @action
  async getExercises() {
    try {
      const { data } = await getExercises();

      const obj: TExercisesEdited = {};

      data.forEach(item => {
        if (obj[item?.muscle_group] === undefined) {
          obj[item?.muscle_group] = [];
        }
        obj[item?.muscle_group].push(item);
      });

      this.setExercises(obj);
    } catch (e) {
      console.warn(e);
      throw e;
    }
  }
}
