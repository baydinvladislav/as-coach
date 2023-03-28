import React from 'react';
import { TextProps, Text as TextRN, TextStyle } from 'react-native';

import styled from 'styled-components';

import { colors } from '@theme';

import { FontSize, FontWeight } from '~types';

type TProps = {
  children: React.ReactNode;
  textStyle?: TextStyle;
  weight?: FontWeight;
  fontSize?: FontSize;
  color?: string;
} & TextProps;

export const Text = ({
  children,
  textStyle,
  weight = FontWeight.Medium,
  fontSize = FontSize.S17,
  color = colors.black,
  ...props
}: TProps) => (
  <TextContainer
    {...props}
    weight={weight}
    fontSize={fontSize}
    color={color}
    style={textStyle}
  >
    {children}
  </TextContainer>
);
const TextContainer = styled(TextRN)<{
  weight: FontWeight;
  fontSize: FontSize;
  color: string;
}>`
  font-family: ${p => p.weight};
  font-size: ${p => p.fontSize};
  color: ${p => p.color};
`;
