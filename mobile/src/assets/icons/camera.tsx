import React from 'react';

import Svg, { Path, SvgProps } from 'react-native-svg';

export const CameraIcon = (props: SvgProps) => (
  <Svg width="20" height="20" viewBox="0 0 20 20" fill="none" {...props}>
    <Path
      d="M5.63339 18.3332H14.3667C16.6667 18.3332 17.5834 16.9248 17.6917 15.2082L18.1251 8.32484C18.2417 6.52484 16.8084 4.99984 15.0001 4.99984C14.4917 4.99984 14.0251 4.70817 13.7917 4.25817L13.1917 3.04984C12.8084 2.2915 11.8084 1.6665 10.9584 1.6665H9.05006C8.19173 1.6665 7.19173 2.2915 6.80839 3.04984L6.20839 4.25817C5.97506 4.70817 5.50839 4.99984 5.00006 4.99984C3.19172 4.99984 1.75839 6.52484 1.87506 8.32484L2.30839 15.2082C2.40839 16.9248 3.33339 18.3332 5.63339 18.3332Z"
      stroke="white"
      strokeOpacity="0.7"
      strokeWidth="1.5"
      strokeLinecap="round"
      strokeLinejoin="round"
    />
    <Path
      d="M8.75 6.6665H11.25"
      stroke="white"
      strokeOpacity="0.7"
      strokeWidth="1.5"
      strokeLinecap="round"
      strokeLinejoin="round"
    />
    <Path
      d="M9.99996 15.0002C11.4916 15.0002 12.7083 13.7835 12.7083 12.2918C12.7083 10.8002 11.4916 9.5835 9.99996 9.5835C8.50829 9.5835 7.29163 10.8002 7.29163 12.2918C7.29163 13.7835 8.50829 15.0002 9.99996 15.0002Z"
      stroke="white"
      strokeOpacity="0.7"
      strokeWidth="1.5"
      strokeLinecap="round"
      strokeLinejoin="round"
    />
  </Svg>
);
