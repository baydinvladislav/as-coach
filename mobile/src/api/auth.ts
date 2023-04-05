import { axiosBase } from '@api';
import { removeNulls } from '@utils';

export const login = (values: { username: string; password: string }) =>
  axiosBase.post('/login', {
    ...values,
    isJson: false,
  });

export const registration = (values: {
  first_name: string;
  username: string;
  password: string;
}) => axiosBase.post('/signup', values);

export const profileEdit = (values: {
  first_name?: string;
  last_name?: string;
  username?: string;
  password?: string;
  gender?: string;
  birthday?: string;
  email?: string;
}) => axiosBase.post('/profiles', { ...removeNulls(values), isJson: false });

export const me = () => axiosBase.get('/profiles');
