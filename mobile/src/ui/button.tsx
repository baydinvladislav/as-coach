import React from 'react';
import { TouchableOpacity, TouchableOpacityProps } from 'react-native';

import styled from 'styled-components';

import { colors, normVert } from '@theme';

import { Text } from './text';

type TProps = {
  children: React.ReactNode;
  type: ButtonType;
} & TouchableOpacityProps;

export enum ButtonType {
  PRIMARY = 'primary',
  SECONDARY = 'secondary',
  TEXT = 'text',
}

export const Button = ({ children, ...props }: TProps) => (
  <ButtonStyled {...props}>
    <Text color={switchFontColor(props.type)}>{children}</Text>
  </ButtonStyled>
);

const ButtonStyled = styled(TouchableOpacity)<{ type: ButtonType }>`
  background: ${({ type }) => switchBackgroundColor(type)};
  flex-direction: row;
  justify-content: center;
  padding-vertical: ${normVert(13)}px;
  border-radius: 12px;
`;

const switchFontColor = (type: ButtonType) => {
  switch (type) {
    case ButtonType.PRIMARY:
      return colors.black2;
    case ButtonType.SECONDARY:
      return colors.green;
    case ButtonType.TEXT:
      return colors.green;
    default:
      return colors.green;
  }
};

const switchBackgroundColor = (type: ButtonType) => {
  switch (type) {
    case ButtonType.PRIMARY:
      return colors.green;
    case ButtonType.SECONDARY:
      return colors.grey;
    case ButtonType.TEXT:
      return colors.transparent;
    default:
      return colors.green;
  }
};
