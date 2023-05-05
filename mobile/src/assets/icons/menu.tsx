import React from 'react';

import Svg, { Path, SvgProps } from 'react-native-svg';

export const MenuIcon = (props: SvgProps) => (
  <Svg width="24" height="24" viewBox="0 0 24 24" {...props}>
    <Path
      d="M3 7H21"
      stroke="#B8FF5F"
      stroke-width="1.5"
      stroke-linecap="round"
    />
    <Path
      d="M3 12H21"
      stroke="#B8FF5F"
      stroke-width="1.5"
      stroke-linecap="round"
    />
    <Path
      d="M3 17H21"
      stroke="#B8FF5F"
      stroke-width="1.5"
      stroke-linecap="round"
    />
  </Svg>
);
