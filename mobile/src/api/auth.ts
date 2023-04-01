import { axiosBase } from '@api';

export const login = (username: string, password: string) =>
  axiosBase.post('/login', {
    username,
    password,
    isJson: false,
  });

export const registration = (username: string, password: string) =>
  axiosBase.post(
    '/signup',
    JSON.stringify({
      password,
      username,
    }),
  );

export const me = () => axiosBase.get('/me');
