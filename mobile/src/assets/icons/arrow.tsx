import React from 'react';

import Svg, { Path, SvgProps } from 'react-native-svg';

export const ArrowIcon = (props: SvgProps) => (
  <Svg width="20" height="20" viewBox="0 0 20 20" fill="none" {...props}>
    <Path
      d="M8.7083 5.59998L5.60828 2.5L2.5083 5.59998"
      stroke="white"
      strokeOpacity="0.7"
      strokeWidth="1.5"
      strokeLinecap="round"
      strokeLinejoin="round"
    />
    <Path
      d="M5.60828 17.5V2.5"
      stroke="white"
      strokeOpacity="0.7"
      strokeWidth="1.5"
      strokeLinecap="round"
      strokeLinejoin="round"
    />
    <Path
      d="M11.2916 14.3999L14.3917 17.4999L17.4916 14.3999"
      stroke="white"
      strokeOpacity="0.7"
      strokeWidth="1.5"
      strokeLinecap="round"
      strokeLinejoin="round"
    />
    <Path
      d="M14.3916 2.5V17.5"
      stroke="white"
      strokeOpacity="0.7"
      strokeWidth="1.5"
      strokeLinecap="round"
      strokeLinejoin="round"
    />
  </Svg>
);
