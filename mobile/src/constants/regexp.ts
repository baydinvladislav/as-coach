/* eslint-disable no-useless-escape */
export const PHONE_REGEXP =
  /^(\+7|7|8)?[\s\-]?\(?[489][0-9]{2}\)?[\s\-]?[0-9]{3}[\s\-]?[0-9]{2}[\s\-]?[0-9]{2}$/;

export const BIRTHDAY_REGEXP =
  /^\s*(3[01]|[12][0-9]|0?[1-9])\.(1[012]|0?[1-9])\.((?:19|20)\d{2})\s*$/;

export const EMAIL_REGEXP = /([a-zA-Z0-9._-]+@[a-zA-Z0-9._-]+\.[a-zA-Z0-9_-]+)/;

export const TELEGRAM_USERNAME_REGEXP = /^@[a-zA-Z][a-zA-Z\d_]{4,31}$/;
