import React, { useState } from 'react';
import {
  StyleProp,
  TextInput,
  TextInputProps,
  View,
  ViewStyle,
} from 'react-native';

import { useMaskedInputProps } from 'react-native-mask-input';
import styled, { css } from 'styled-components';

import { colors, normHor, normVert } from '@theme';

import { FontSize } from '~types';

import { Placeholder } from './placeholder';
import { Text } from './text';

export type TInputProps = {
  placeholder?: string;
  rightIcon?: JSX.Element;
  leftIcon?: JSX.Element;
  width?: string;
  height?: number;
  isTextarea?: boolean;
  style?: StyleProp<ViewStyle>;
  mask?: any;
  error?: string;
  description?: string;
  onFocus?: () => void;
  onBlur?: () => void;
  onPress?: () => void;
} & TextInputProps;

export const Input = ({
  placeholder,
  rightIcon,
  leftIcon,
  width = '100%',
  height = 48,
  isTextarea = false,
  style,
  mask,
  error,
  description,
  onPress,
  ...props
}: TInputProps) => {
  const [state, setState] = useState({
    value: '',
    isFocused: false,
  });

  const handleChange = (value: string) => {
    setState(state => ({ ...state, value }));
  };

  const handleBlur = () => {
    props?.onBlur?.();
    setState(state => ({ ...state, isFocused: false }));
  };

  const handleFocus = () => {
    props?.onFocus?.();
    setState(state => ({ ...state, isFocused: true }));
  };

  const isActive = props.value || state.value !== '' || state.isFocused;

  const maskedInputProps = useMaskedInputProps({
    value: props.value,
    onChangeText: props.onChangeText ?? handleChange,
    mask,
  });

  const direction = (leftIcon && 'left') || (rightIcon && 'right') || null;

  return (
    <View style={style}>
      <InputContainer
        error={error ?? ''}
        isTextarea={isTextarea}
        height={height}
        width={width}
        isFocused={state.isFocused}
        dir={direction}
      >
        {leftIcon && <Icon dir="left">{leftIcon}</Icon>}
        {placeholder && (
          <Placeholder isActive={Boolean(isActive)} text={placeholder} />
        )}
        <InputRN
          {...props}
          {...maskedInputProps}
          placeholder=""
          style={{ paddingVertical: 0 }}
          clearTextOnFocus={false}
          onFocus={handleFocus}
          onBlur={handleBlur}
          multiline={isTextarea}
          numberOfLines={4}
          value={props.value ?? state.value}
          onPressIn={onPress}
        />
        {rightIcon && <Icon dir="right">{rightIcon}</Icon>}
      </InputContainer>
      {error && (
        <ErrorText fontSize={FontSize.S12} color={colors.red}>
          {error}
        </ErrorText>
      )}
      {description && (
        <ErrorText align="center" fontSize={FontSize.S12} color={colors.black5}>
          {description}
        </ErrorText>
      )}
    </View>
  );
};

const paddingStyle = css<{ dir: 'left' | 'right' | null }>`
  padding-left: ${({ dir }) =>
    dir === 'right' || dir === null ? normHor(16) : normHor(44)}px;
  padding-top: ${({ dir }) => (dir === 'left' ? 0 : normVert(18))}px;
`;

const InputContainer = styled(View)<{
  width: string;
  height: number;
  isTextarea: boolean;
  error: string;
  isFocused: boolean;
  dir: 'left' | 'right' | null;
}>`
  ${paddingStyle}

  border-width: 1px;
  border-color: ${colors.transparent};
  height: ${({ height }) => normVert(height)}px;
  width: ${({ width }) => width};
  padding-horizontal: ${normHor(16)}px;
  background-color: ${({ error }) => (error ? colors.red2 : colors.black3)};
  ${({ error }) =>
    error &&
    `border-width: 1px;
     border-color: ${colors.red};`};
  border-radius: 12px;
  flex-direction: row;
  align-items: flex-start;
  ${({ isFocused, error }) =>
    isFocused &&
    !error &&
    `border-width: 1px;
     border-color: ${colors.green};`}
`;

const ErrorText = styled(Text)`
  margin-top: ${normVert(4)}px;
  margin-left: ${normHor(16)}px;
`;

const Icon = styled(View)<{ dir: 'left' | 'right' }>`
  position: absolute;
  top: ${normVert(14)}px;
  ${({ dir }) =>
    dir === 'left' ? `left: ${normHor(16)}px` : `right: ${normHor(16)}px`}
`;

const InputRN = styled(TextInput)`
  font-size: ${FontSize.S16};
  width: 100%;
  height: 100%;
  color: ${colors.white};
`;
