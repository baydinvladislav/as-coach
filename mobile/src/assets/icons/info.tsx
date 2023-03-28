import React from 'react';

import Svg, { Path, SvgProps } from 'react-native-svg';

export const InfoIcon = (props: SvgProps) => (
  <Svg width="20" height="20" viewBox="0 0 20 20" fill="none" {...props}>
    <Path
      d="M9.99996 18.3332C14.5833 18.3332 18.3333 14.5832 18.3333 9.99984C18.3333 5.4165 14.5833 1.6665 9.99996 1.6665C5.41663 1.6665 1.66663 5.4165 1.66663 9.99984C1.66663 14.5832 5.41663 18.3332 9.99996 18.3332Z"
      stroke="white"
      strokeOpacity="0.7"
      strokeWidth="1.5"
      strokeLinecap="round"
      strokeLinejoin="round"
    />
    <Path
      d="M10 6.6665V10.8332"
      stroke="white"
      strokeOpacity="0.7"
      strokeWidth="1.5"
      strokeLinecap="round"
      strokeLinejoin="round"
    />
    <Path
      d="M9.99536 13.3335H10.0028"
      stroke="white"
      strokeOpacity="0.7"
      strokeWidth="1.5"
      strokeLinecap="round"
      strokeLinejoin="round"
    />
  </Svg>
);
