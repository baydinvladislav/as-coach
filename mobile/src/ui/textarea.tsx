import React from 'react';

import { normVert } from '@theme';

import { Input } from './input';

export const Textarea = () => (
  <Input
    isTextarea={true}
    height={normVert(120)}
    placeholder={'Type your complaint here...'}
    multiline={true}
    numberOfLines={4}
  />
);
