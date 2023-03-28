import React from 'react';
import {
  StyleProp,
  TextInput,
  TextInputProps,
  View,
  ViewStyle,
} from 'react-native';

import styled from 'styled-components';

import { colors, normHor, normVert } from '@theme';

import { FontSize } from '~types';

type TProps = {
  placeholder?: string;
  leftIcon?: JSX.Element;
  rightIcon?: JSX.Element;
  width?: string;
  height?: number;
  isTextarea?: boolean;
  style?: StyleProp<ViewStyle>;
} & TextInputProps;

export const Input = ({
  placeholder,
  leftIcon,
  rightIcon,
  width = '100%',
  height = normVert(48),
  isTextarea = false,
  style,
  ...props
}: TProps) => (
  <InputContainer
    style={style}
    isTextarea={isTextarea}
    height={height}
    width={width}
  >
    {leftIcon}
    <InputRN {...props} placeholder={placeholder} isTextarea={isTextarea} />
    {rightIcon}
  </InputContainer>
);

const InputContainer = styled(View)<{
  width: string;
  height: number;
  isTextarea: boolean;
}>`
  height: ${({ height }) => height}px;
  width: ${({ width }) => width};
  padding-horizontal: ${normHor(20)}px;
  background-color: ${colors.black3};
  border-radius: 12px;
  flex-direction: row;
  align-items: center;
  ${({ isTextarea }) => isTextarea && `padding-top: ${normVert(16)}px`};
`;

const InputRN = styled(TextInput)<{ isTextarea: boolean }>`
  font-size: ${FontSize.S17};
  width: 100%;
  height: 100%;
`;
