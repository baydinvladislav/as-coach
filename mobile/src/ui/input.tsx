import React from 'react';
import { TextInput, TextInputProps, View } from 'react-native';

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
} & TextInputProps;

export const Input = ({
  placeholder,
  leftIcon,
  rightIcon,
  width = '100%',
  height = normVert(48),
  isTextarea = false,
  ...props
}: TProps) => (
  <InputContainer isTextarea={isTextarea} height={height} width={width}>
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
  height: ${p => p.height}px;
  width: ${p => p.width};
  padding-horizontal: ${normHor(20)}px;
  border: 1px solid ${colors.black};
  background-color: ${colors.white};
  border-radius: 16px;
  flex-direction: row;
  align-items: center;
  ${p => p.isTextarea && `padding-top: ${normVert(16)}px`};
`;

const InputRN = styled(TextInput)<{ isTextarea: boolean }>`
  font-size: ${FontSize.S17};
  width: 100%;
  height: 100%;
`;
