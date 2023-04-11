import React from 'react';

import Svg, { Path, SvgProps } from 'react-native-svg';

export const MinusIcon = (props: SvgProps) => (
  <Svg width="21" height="21" viewBox="0 0 21 21" fill="none" {...props}>
    <Path
      d="M5.25 10.5H15.75"
      stroke={props.stroke}
      strokeOpacity="0.7"
      strokeWidth="1.5"
      strokeLinecap="round"
      strokeLinejoin="round"
    />
  </Svg>
);
