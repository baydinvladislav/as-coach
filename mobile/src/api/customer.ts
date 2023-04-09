import { axiosBase } from '@api';
import { CustomerProps } from '@store';

export const createCustomer = (values: Partial<CustomerProps>) =>
  axiosBase.post('/customers', {
    ...values,
  });

export const getCustomers = () => axiosBase.get('/customers');
