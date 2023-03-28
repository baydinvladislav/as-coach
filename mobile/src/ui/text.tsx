import React from 'react';
import { StyleProp, TextProps, Text as TextRN, TextStyle } from 'react-native';

import styled from 'styled-components';

import { colors } from '@theme';

import { FontSize, FontWeight } from '~types';

type TProps = {
  children: React.ReactNode;
  weight?: FontWeight;
  fontSize?: FontSize;
  color?: string;
  align?: 'center' | 'left' | 'right';
  style?: StyleProp<TextStyle>;
} & TextProps;

export const Text = ({
  children,
  weight = FontWeight.Medium,
  fontSize = FontSize.S17,
  color = colors.black,
  align = 'left',
  ...props
}: TProps) => (
  <TextContainer
    {...props}
    weight={weight}
    fontSize={fontSize}
    color={color}
    align={align}
  >
    {children}
  </TextContainer>
);
const TextContainer = styled(TextRN)<{
  weight: FontWeight;
  fontSize: FontSize;
  color: string;
  align: 'center' | 'left' | 'right';
}>`
  font-family: ${({ weight }) => weight};
  font-size: ${({ fontSize }) => fontSize};
  color: ${({ color }) => color};
  text-align: ${({ align }) => align};
`;
