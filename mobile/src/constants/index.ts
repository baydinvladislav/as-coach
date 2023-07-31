import Config from 'react-native-config';

import { normVert } from '@theme';

export * from './mask';
export * from './regexp';
export * from './date';

export const API_URL_IOS = Config.API_URL;
export const API_URL_ANDROID = Config.API_URL;

export const URL_IOS = Config.API_URL;
export const URL_ANDROID = Config.API_URL;

export const ENCRYPTION_KEY = 'development';
export const TOKEN = 'token';

export const TOP_PADDING = normVert(60);
