import React from 'react';
import { View } from 'react-native';

import { TouchableOpacity } from 'react-native-gesture-handler';
import styled from 'styled-components';

import { AddIcon, MinusIcon } from '@assets';
import { RANGE_MASK } from '@constants';
import { colors, normHor, normVert } from '@theme';

import { Input, TInputProps } from './input';

export const InputSpinner = ({ style, ...props }: TInputProps) => {
  const handlePlus = () => {
    props.onChangeText?.(String(Number(props.value) + 10));
  };

  const handleMinus = () => {
    const value = Number(props.value) - 10;
    if (value >= 0) {
      props.onChangeText?.(String(value));
    } else {
      props.onChangeText?.(String(0));
    }
  };

  return (
    <Container style={style}>
      <Icon onPress={handleMinus}>
        <MinusIcon stroke={colors.green} />
      </Icon>
      <Input
        keyboardType="number-pad"
        mask={RANGE_MASK}
        width={`${normHor(221)}px`}
        {...props}
      />
      <Icon onPress={handlePlus}>
        <AddIcon fill={colors.green} />
      </Icon>
    </Container>
  );
};

const Icon = styled(TouchableOpacity)`
  background: ${colors.grey};
  border-radius: 12px;
  width: ${normHor(46)}px;
  height: ${normVert(46)}px;
  justify-content: center;
  align-items: center;
`;

const Container = styled(View)`
  flex-direction: row;
  justify-content: space-between;
  align-items: center;
`;
