import * as yup from 'yup';

import { t } from '@i18n';

export const loginValidationSchema = () =>
  yup.object().shape({
    username: yup
      .string()
      .length(18, t('errors.phoneError'))
      .required(t('errors.required')),
    password: yup.string().required(t('errors.required')),
  });

export const registrationValidationSchema = () =>
  yup.object().shape({
    first_name: yup.string().required(t('errors.required')),
    username: yup
      .string()
      .length(18, t('errors.phoneError'))
      .required(t('errors.required')),
    password: yup.string().required(t('errors.required')),
  });

export const profileEditValidationSchema = () =>
  yup.object().shape({
    first_name: yup.string().required(t('errors.required')),
    last_name: yup.string().nullable().default(null),
    username: yup.string().required(t('errors.required')),
    gender: yup.string().nullable().default(null),
    birthday: yup.string().nullable().default(null),
    email: yup.string().nullable().default(null),
  });

export const addClientValidationSchema = () =>
  yup.object().shape({
    first_name: yup.string().required(t('errors.required')),
    last_name: yup.string().required(t('errors.required')),
    phone_number: yup
      .string()
      .length(18, t('errors.phoneError'))
      .required(t('errors.required')),
  });
