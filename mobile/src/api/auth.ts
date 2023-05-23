import { axiosBase } from '@api';
import { UserProps } from '@store';
import { removeNulls } from '@utils';

import { TResponseConfirmPassword } from '~types';

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

export const changePassword = ({ password }: Pick<UserProps, 'password'>) =>
  axiosBase.patch('/change_password', { password });

export const confirmPassword = ({ password }: Pick<UserProps, 'password'>) =>
  axiosBase.post<TResponseConfirmPassword>('/confirm_password', {
    current_password: password,
    isJson: false,
  });
