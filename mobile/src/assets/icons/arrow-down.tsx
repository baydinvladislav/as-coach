import React from 'react';

import Svg, { Path, SvgProps } from 'react-native-svg';

export const ArrowDownIcon = (props: SvgProps) => (
  <Svg width="20" height="20" viewBox="0 0 20 20" fill="none" {...props}>
    <Path
      d="M16.6 7.4585L11.1667 12.8918C10.525 13.5335 9.47502 13.5335 8.83336 12.8918L3.40002 7.4585"
      stroke="white"
      strokeOpacity="0.7"
      strokeWidth="1.5"
      strokeMiterlimit="10"
      strokeLinecap="round"
      strokeLinejoin="round"
    />
  </Svg>
);
