import React from 'react';

import Svg, { Path, SvgProps } from 'react-native-svg';

export const CheckIcon = (props: SvgProps) => (
  <Svg width="14" height="10" viewBox="0 0 14 10" fill="none" {...props}>
    <Path
      d="M1 5L4.99529 9L13 1"
      stroke="#292D32"
      stroke-width="1.5"
      stroke-linecap="round"
      stroke-linejoin="round"
    />
  </Svg>
);
