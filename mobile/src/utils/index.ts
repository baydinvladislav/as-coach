import { Dimensions } from 'react-native';

import { isNil, isString, omitBy } from 'lodash';

export * from './constants';
export * from './storage';
export * from './schema';

interface INestedMessages {
  [key: string]: string | INestedMessages;
}

export const removeNulls = (obj: any) => omitBy(obj, isNil);

export const transformPhone = (phone: string) =>
  phone ? '+' + phone.replace(/[^0-9]/g, '') : '';

export const flattenMessages = (nestedMessages: INestedMessages, prefix = '') =>
  Object.keys(nestedMessages).reduce(
    (acc: Record<string, string>, key: string): Record<string, string> => {
      const value = nestedMessages[`${key}`];
      const prefixedKey = prefix ? `${prefix}.${key}` : key;

      if (isString(value)) {
        acc[`${prefixedKey}`] = value;
      } else {
        Object.assign(acc, flattenMessages(value, prefixedKey));
      }

      return acc;
    },
    {},
  );

export const windowWidth = Dimensions.get('window').width;
export const windowHeight = Dimensions.get('window').height;
