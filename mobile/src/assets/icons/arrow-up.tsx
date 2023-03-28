import React from 'react';

import Svg, { Path, SvgProps } from 'react-native-svg';

export const ArrowUpIcon = (props: SvgProps) => (
  <Svg width="20" height="20" viewBox="0 0 20 20" fill="none" {...props}>
    <Path
      d="M15.0583 7.97484L9.99998 2.9165L4.94165 7.97484"
      stroke="white"
      strokeOpacity="0.7"
      strokeWidth="1.5"
      strokeMiterlimit="10"
      strokeLinecap="round"
      strokeLinejoin="round"
    />
    <Path
      d="M10 17.0831V3.05811"
      stroke="white"
      strokeOpacity="0.7"
      strokeWidth="1.5"
      strokeMiterlimit="10"
      strokeLinecap="round"
      strokeLinejoin="round"
    />
  </Svg>
);
