import React from 'react';

import Svg, { Path, SvgProps } from 'react-native-svg';

export const LockIcon = ({ stroke = 'white', ...props }: SvgProps) => (
  <Svg width="20" height="20" viewBox="0 0 20 20" fill="none" {...props}>
    <Path
      d="M5 8.33317V6.6665C5 3.90817 5.83333 1.6665 10 1.6665C14.1667 1.6665 15 3.90817 15 6.6665V8.33317"
      stroke={stroke}
      strokeOpacity="0.7"
      strokeWidth="1.5"
      strokeLinecap="round"
      strokeLinejoin="round"
    />
    <Path
      d="M9.99996 15.4167C11.1506 15.4167 12.0833 14.4839 12.0833 13.3333C12.0833 12.1827 11.1506 11.25 9.99996 11.25C8.84937 11.25 7.91663 12.1827 7.91663 13.3333C7.91663 14.4839 8.84937 15.4167 9.99996 15.4167Z"
      stroke={stroke}
      strokeOpacity="0.7"
      strokeWidth="1.5"
      strokeLinecap="round"
      strokeLinejoin="round"
    />
    <Path
      d="M14.1666 18.3335H5.83329C2.49996 18.3335 1.66663 17.5002 1.66663 14.1668V12.5002C1.66663 9.16683 2.49996 8.3335 5.83329 8.3335H14.1666C17.5 8.3335 18.3333 9.16683 18.3333 12.5002V14.1668C18.3333 17.5002 17.5 18.3335 14.1666 18.3335Z"
      stroke={stroke}
      strokeOpacity="0.7"
      strokeWidth="1.5"
      strokeLinecap="round"
      strokeLinejoin="round"
    />
  </Svg>
);
