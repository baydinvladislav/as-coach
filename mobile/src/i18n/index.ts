import { createIntl, createIntlCache } from 'react-intl';

import { flattenMessages } from '@utils';

import { ru } from './locales/ru';

const cache = createIntlCache();

const locale = 'ru';

const i18nMsg: { [key: string]: Record<string, string> } = {
  ru: flattenMessages(ru),
};

export const intl = createIntl(
  {
    locale,
    messages: i18nMsg[locale],
  },
  cache,
);

export const t = (id: string, values = {}): string =>
  intl.formatMessage({ id }, values);
