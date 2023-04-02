import React, { useEffect, useRef, useState } from 'react';
import {
  Animated,
  StyleProp,
  TextInput,
  TextInputProps,
  View,
  ViewStyle,
} from 'react-native';

import { withAnchorPoint } from 'react-native-anchor-point';
import { useMaskedInputProps } from 'react-native-mask-input';
import styled from 'styled-components';

import { colors, normHor, normVert } from '@theme';

import { FontSize } from '~types';

export type TInputProps = {
  placeholder?: string;
  rightIcon?: JSX.Element;
  width?: string;
  height?: number;
  isTextarea?: boolean;
  style?: StyleProp<ViewStyle>;
  mask?: any;
} & TextInputProps;

export const Input = ({
  placeholder,
  rightIcon,
  width = '100%',
  height = 48,
  isTextarea = false,
  style,
  mask,
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

  const isActive = props.value || state.value !== '' || state.isFocused;

  const maskedInputProps = useMaskedInputProps({
    value: props.value,
    onChangeText: props.onChangeText ?? handleChange,
    mask,
  });

  const [placeholderWidth, setPlaceholderWidth] = useState(0);
  const [placeholderHeight, setPlaceholderHeight] = useState(0);

  const placeholderAnimY = useRef(new Animated.Value(0)).current;
  const placeholderAnimSize = useRef(new Animated.Value(1)).current;

  const movePlaceholderYIn = () => {
    Animated.timing(placeholderAnimY, {
      toValue: -normVert(12),
      duration: 300,
      useNativeDriver: true,
    }).start();
  };

  const movePlaceholderYOut = () => {
    Animated.timing(placeholderAnimY, {
      toValue: 0,
      duration: 300,
      useNativeDriver: true,
    }).start();
  };

  const sizePlaceholderIn = () => {
    Animated.timing(placeholderAnimSize, {
      toValue: 0.8,
      duration: 300,
      useNativeDriver: true,
    }).start();
  };

  const sizePlaceholderOut = () => {
    Animated.timing(placeholderAnimSize, {
      toValue: 1,
      duration: 300,
      useNativeDriver: true,
    }).start();
  };

  useEffect(() => {
    if (isActive) {
      movePlaceholderYIn();
      sizePlaceholderIn();
    } else {
      movePlaceholderYOut();
      sizePlaceholderOut();
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [isActive]);

  const getTransform = () => {
    const transform = {
      transform: [
        {
          translateY: placeholderAnimY as unknown as number,
        },
        {
          translateX: normHor(16),
        },
        {
          scale: placeholderAnimSize as unknown as number,
        },
      ],
    };
    return withAnchorPoint(
      transform,
      { x: 0, y: 0 },
      { width: placeholderWidth, height: placeholderHeight },
    );
  };

  return (
    <InputContainer
      style={style}
      isTextarea={isTextarea}
      height={height}
      width={width}
    >
      <Placeholder
        isActive={Boolean(isActive)}
        onLayout={event => {
          setPlaceholderWidth(event.nativeEvent.layout.width);
          setPlaceholderHeight(event.nativeEvent.layout.height);
        }}
        style={getTransform()}
      >
        {placeholder}
      </Placeholder>
      <InputRN
        {...props}
        {...maskedInputProps}
        placeholder=""
        style={{ paddingVertical: 0 }}
        isTextarea={isTextarea}
        clearTextOnFocus={false}
        placeholderTextColor={colors.white}
        onFocus={handleFocus}
        onBlur={handleFocus}
        value={props.value ?? state.value}
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
  height: ${({ height }) => normVert(height)}px;
  width: ${({ width }) => width};
  padding-horizontal: ${normHor(16)}px;
  background-color: ${colors.black3};
  border-radius: 12px;
  flex-direction: row;
  align-items: center;
  ${({ isTextarea }) => isTextarea && `padding-top: ${normVert(16)}px`};
  padding-top: ${normVert(18)}px;
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

const Placeholder = styled(Animated.Text)<{ isActive: boolean }>`
  position: absolute;
  color: ${colors.black5};
  font-size: ${FontSize.S17};
`;
