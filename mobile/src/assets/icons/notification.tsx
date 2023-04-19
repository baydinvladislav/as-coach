import React from 'react';

import Svg, { Path, SvgProps } from 'react-native-svg';

export const NotificationIcon = ({ ...props }: SvgProps) => (
  <Svg width="20" height="20" viewBox="0 0 20 20" fill="none" {...props}>
    <Path
      d="M10 5.3667V8.1417"
      strokeMiterlimit="10"
      strokeOpacity="0.7"
      strokeWidth="1.5"
      strokeLinecap="round"
    />
    <Path
      d="M10.0167 1.6665C6.95004 1.6665 4.4667 4.14984 4.4667 7.2165V8.9665C4.4667 9.53317 4.23337 10.3832 3.9417 10.8665L2.88337 12.6332C2.23337 13.7248 2.68337 14.9415 3.88337 15.3415C7.8667 16.6665 12.175 16.6665 16.1584 15.3415C17.2834 14.9665 17.7667 13.6498 17.1584 12.6332L16.1 10.8665C15.8084 10.3832 15.575 9.52484 15.575 8.9665V7.2165C15.5667 4.1665 13.0667 1.6665 10.0167 1.6665Z"
      strokeMiterlimit="10"
      strokeOpacity="0.7"
      strokeWidth="1.5"
      strokeLinecap="round"
    />
    <Path
      d="M12.775 15.6831C12.775 17.2081 11.525 18.4581 9.99998 18.4581C9.24164 18.4581 8.54164 18.1414 8.04164 17.6414C7.54164 17.1414 7.22498 16.4414 7.22498 15.6831"
      strokeMiterlimit="10"
      strokeOpacity="0.7"
      strokeWidth="1.5"
    />
  </Svg>
);
