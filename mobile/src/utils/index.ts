import { isString } from 'lodash';

export * from './constants';

interface INestedMessages {
  [key: string]: string | INestedMessages;
}

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