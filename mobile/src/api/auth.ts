import { axiosBase } from '@api';
import { UserProps } from '@store';
import { removeNulls } from '@utils';

export const login = (values: Partial<UserProps>) =>
  axiosBase.post('/login', {
    ...values,
    isJson: false,
  });

export const registration = (values: Partial<UserProps>) =>
  axiosBase.post('/signup', values);

export const profileEdit = (values: Partial<UserProps>) =>
  axiosBase.post('/profiles', { ...removeNulls(values), isJson: false });

export const me = () => axiosBase.get('/profiles');
