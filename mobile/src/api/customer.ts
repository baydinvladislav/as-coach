import { axiosBase } from '@api';
import { CustomerProps } from '@store';

import { TExercises, TPlanType } from '~types';

export const createCustomer = (values: Partial<CustomerProps>) =>
  axiosBase.post('/customers', values);

export const getCustomers = () => axiosBase.get('/customers');

export const createPlan = (id: string, values: any) =>
  axiosBase.post(`/customers/${id}/training_plans`, values);

export const getExercises = () => axiosBase.get<TExercises[]>('/exercises');

export const getCustomerPlan = (id: string) =>
  axiosBase.get<TPlanType[]>(`/customers/${id}/training_plans`);

export const getCustomerPlanDetail = (id: string, planId: string) =>
  axiosBase.get<TPlanType[]>(`/customers/${id}/training_plans/${planId}`);
