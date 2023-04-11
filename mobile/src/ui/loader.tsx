import React from 'react';

import Lottie from 'lottie-react-native';

import { LoaderJSON } from '@assets';
import { normHor, normVert } from '@theme';

export const Loader = () => (
  <Lottie
    source={LoaderJSON}
    style={{
      marginLeft: 'auto',
      marginRight: 'auto',
      width: normHor(100),
      height: normVert(100),
    }}
    autoPlay={true}
    loop={true}
  />
);
