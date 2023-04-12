import React from 'react';

import Svg, { Circle, Path, SvgProps } from 'react-native-svg';

export const NotFoundIcon = (props: SvgProps) => (
  <Svg width="150" height="122" viewBox="0 0 150 122" fill="none" {...props}>
    <Path
      opacity="0.06"
      d="M51.8497 104.628C31.9075 96.6519 0.997109 96.1534 0 64.2484C8.47543 32.3436 49.5665 48.9648 72.5 37.0004C95.4335 25.036 121.647 -11.527 142.088 4.42549C162.529 20.378 138.313 50.8491 126.134 68.7957C113.955 86.7423 126.134 111.086 107.189 119.085C84.7543 128.556 71.7918 112.604 51.8497 104.628Z"
      fill="white"
    />
    <Circle
      cx="74.5314"
      cy="55.0214"
      r="31.1805"
      stroke="white"
      strokeOpacity="0.4"
      strokeWidth="3"
    />
    <Path
      d="M102 82L108 88"
      stroke="white"
      strokeOpacity="0.4"
      strokeWidth="3"
      strokeLinecap="round"
    />
  </Svg>
);
