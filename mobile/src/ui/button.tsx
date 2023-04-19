import React from 'react';
import { TouchableOpacity, TouchableOpacityProps, View } from 'react-native';

import styled from 'styled-components';

import { LoadingIcon } from '@assets';
import { colors, normHor, normVert } from '@theme';

import { ButtonType } from '~types';

import { Text } from './text';

type TProps = {
  children: React.ReactNode;
  type: ButtonType;
  leftIcon?: JSX.Element;
  isDisabled?: boolean;
  isLoading?: boolean;
} & TouchableOpacityProps;

export const Button = ({
  children,
  leftIcon,
  isDisabled = false,
  isLoading = false,
  ...props
}: TProps) => (
  <ButtonStyled
    {...props}
    activeOpacity={0.5}
    disabled={isLoading || isDisabled}
  >
    {leftIcon && <View style={{ marginRight: normHor(12) }}>{leftIcon}</View>}
    {isLoading ? (
      <LoadingIcon />
    ) : (
      <Text
        style={{ opacity: isDisabled ? 0.4 : 1 }}
        color={switchFontColor(props.type)}
      >
        {children}
      </Text>
    )}
  </ButtonStyled>
);

const ButtonStyled = styled(TouchableOpacity)<{ type: ButtonType }>`
  background: ${({ type }) => switchBackgroundColor(type)};
  flex-direction: row;
  justify-content: center;
  align-items: center;
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
