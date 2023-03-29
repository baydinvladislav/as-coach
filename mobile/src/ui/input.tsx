import React, { useState } from 'react';
import {
  StyleProp,
  TextInput,
  TextInputProps,
  View,
  ViewStyle,
} from 'react-native';

import styled from 'styled-components';

import { colors, normHor, normVert } from '@theme';
import { Text } from '@ui';

import { FontSize } from '~types';

export type TInputProps = {
  placeholder?: string;
  rightIcon?: JSX.Element;
  width?: string;
  height?: number;
  isTextarea?: boolean;
  style?: StyleProp<ViewStyle>;
} & TextInputProps;

export const Input = ({
  placeholder,
  rightIcon,
  width = '100%',
  height = normVert(48),
  isTextarea = false,
  style,
  ...props
}: TInputProps) => {
  const [state, setState] = useState({
    value: '',
    isFocused: false,
  });

  const handleChange = (value: string) => {
    setState(state => ({ ...state, value }));
  };

  const handleFocus = () => {
    setState(state => ({ ...state, isFocused: !state.isFocused }));
  };

  const isActive = state.value !== '' || state.isFocused;

  return (
    <InputContainer
      style={style}
      isTextarea={isTextarea}
      height={height}
      width={width}
    >
      <Placeholder isActive={isActive}>{placeholder}</Placeholder>
      <InputRN
        {...props}
        isTextarea={isTextarea}
        clearTextOnFocus={false}
        placeholderTextColor={colors.white}
        onChangeText={handleChange}
        onFocus={handleFocus}
        onBlur={handleFocus}
      />
      <Icon>{rightIcon}</Icon>
    </InputContainer>
  );
};
const InputContainer = styled(View)<{
  width: string;
  height: number;
  isTextarea: boolean;
}>`
  height: ${({ height }) => height}px;
  width: ${({ width }) => width};
  padding-horizontal: ${normHor(16)}px;
  background-color: ${colors.black3};
  border-radius: 12px;
  flex-direction: row;
  align-items: center;
  ${({ isTextarea }) => isTextarea && `padding-top: ${normVert(16)}px`};
  padding-top: ${normVert(14)}px;
`;

const Icon = styled(View)`
  position: absolute;
  right: ${normHor(16)}px;
`;

const InputRN = styled(TextInput)<{ isTextarea: boolean }>`
  font-size: ${FontSize.S16};
  width: 100%;
  height: 100%;
  color: ${colors.white};
`;

const Placeholder = styled(Text)<{ isActive: boolean }>`
  position: absolute;
  color: ${colors.black5};
  left: ${normHor(16)}px;
  top: ${({ isActive }) => (isActive ? normVert(6) : normVert(15))}px;
  font-size: ${({ isActive }) => (isActive ? FontSize.S12 : FontSize.S17)};
`;
