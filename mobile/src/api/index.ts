import axios, { AxiosRequestHeaders } from 'axios';
import { isEmpty } from 'lodash';

import { API_URL, TOKEN } from '@constants';
import { storage } from '@utils';

export * from './auth';

export const axiosBase = axios.create({
  headers: {
    'Content-Type': 'application/json',
  },
});

axiosBase.defaults.baseURL = API_URL;

axiosBase.defaults.transformRequest = function (data = {}, headers) {
  const { isJson = true, ...body } = data;

  if (isEmpty(body)) return;

  if (!isJson) {
    (headers as AxiosRequestHeaders)['Content-Type'] =
      'application/x-www-form-urlencoded';
    const str = [];
    for (const key in body) {
      str.push(encodeURIComponent(key) + '=' + encodeURIComponent(body[key]));
    }

    return str.join('&');
  }

  return JSON.stringify(body);
};

axiosBase.interceptors.request.use(config => {
  const getToken = storage.getItem(TOKEN);

  getToken.then((token?: string) => {
    const auth = token ? `Bearer ${token}` : '';
    config.headers = {
      ...config.headers,
      Authorization: auth,
    };
  });

  return config;
});
