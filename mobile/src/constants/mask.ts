export const PHONE_MASK = [
  '+',
  '7',
  ' ',
  '(',
  /\d/,
  /\d/,
  /\d/,
  ')',
  ' ',
  /\d/,
  /\d/,
  /\d/,
  '-',
  /\d/,
  /\d/,
  '-',
  /\d/,
  /\d/,
];

export const RANGE_MASK = [/\d/, /\d/, /\d/, /\d/];

export const DATE_MASK = [
  /\d/,
  /\d/,
  '.',
  /\d/,
  /\d/,
  '.',
  /\d/,
  /\d/,
  /\d/,
  /\d/,
];

export const TELEGRAM_USERNAME_MASK = ['@', ...Array(32).fill(/[a-zA-Z0-9_]/)];
