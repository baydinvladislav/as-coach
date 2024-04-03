import * as yup from 'yup';

import {
  BIRTHDAY_REGEXP,
  EMAIL_REGEXP,
  OTP_LENGTH,
  PASSWORD_MIN,
  PHONE_REGEXP,
  TELEGRAM_USERNAME_REGEXP,
} from '@constants';
import { t } from '@i18n';

export const confirmPasswordSchema = () =>
  yup.object().shape({
    password: yup
      .string()
      .min(PASSWORD_MIN, t('errors.minPassword'))
      .required(t('errors.required')),
  });

export const changePasswordSchema = () =>
  yup.object().shape({
    password: yup
      .string()
      .oneOf([yup.ref('newPassword')], t('errors.passwordNotMatch'))
      .min(PASSWORD_MIN, t('errors.minPassword'))
      .required(t('errors.required')),
    newPassword: yup
      .string()
      .min(PASSWORD_MIN, t('errors.minPassword'))
      .oneOf([yup.ref('password')], t('errors.passwordNotMatch'))
      .required(t('errors.required')),
  });

export const loginValidationSchema = () =>
  yup.object().shape({
    username: yup
      .string()
      .matches(PHONE_REGEXP, t('errors.phoneError'))
      .required(t('errors.required')),
    password: yup
      .string()
      .min(OTP_LENGTH, t('errors.minPassword'))
      .required(t('errors.required')),
  });

export const registrationValidationSchema = () =>
  yup.object().shape({
    first_name: yup.string().required(t('errors.required')),
    username: yup
      .string()
      .matches(PHONE_REGEXP, t('errors.phoneError'))
      .required(t('errors.required')),
    password: yup
      .string()
      .min(PASSWORD_MIN, t('errors.minPassword'))
      .required(t('errors.required')),
  });

export const profileEditValidationSchema = () =>
  yup.object().shape({
    first_name: yup.string().required(t('errors.required')),
    last_name: yup.string().nullable().default(null),
    username: yup
      .string()
      .matches(PHONE_REGEXP, t('errors.phoneError'))
      .required(t('errors.required')),
    gender: yup.string().nullable().default(null),
    birthday: yup
      .string()
      .nullable()
      .default(null)
      .matches(BIRTHDAY_REGEXP, t('errors.birthdayError')),
    email: yup
      .string()
      .nullable()
      .default(null)
      .matches(EMAIL_REGEXP, t('errors.emailError')),
  });

export const addClientValidationSchema = () =>
  yup.object().shape({
    first_name: yup.string().required(t('errors.required')),
    last_name: yup.string().required(t('errors.required')),
    phone_number: yup
      .string()
      .matches(TELEGRAM_USERNAME_REGEXP, t('errors.tgUsernameError'))
      .required(t('errors.required')),
  });

export const createPlanValidationSchema = () =>
  yup.object().shape({
    start_date: yup.string().required(t('errors.required')),
    end_date: yup.string().required(t('errors.required')),
    diets: yup.array().of(
      yup.object().shape({
        proteins: yup.string().required(t('errors.required')),
        fats: yup.string().required(t('errors.required')),
        carbs: yup.string().required(t('errors.required')),
      }),
    ),
    trainings: yup.array().of(
      yup.object().shape({
        name: yup.string().required(t('errors.required')),
        exercises: yup.array().of(
          yup.object().shape({
            id: yup.string().required(t('errors.required')),
            name: yup.string().required(t('errors.required')),
            sets: yup.array().of(yup.string().required(t('errors.required'))),
          }),
        ),
      }),
    ),
  });

export const createExerciseSchema = () =>
  yup.object().shape({
    name: yup.string().required(t('errors.required')),
    muscle_group_id: yup.string().required(t('errors.specifyMuscleGroup')),
  });
