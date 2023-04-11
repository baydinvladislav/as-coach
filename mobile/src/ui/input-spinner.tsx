import React from 'react';
import { View } from 'react-native';

import { TouchableOpacity } from 'react-native-gesture-handler';
import styled from 'styled-components';

import { AddIcon, MinusIcon } from '@assets';
import { RANGE_MASK } from '@constants';
import { colors, normHor, normVert } from '@theme';

import { Input, TInputProps } from './input';

export const InputSpinner = ({ style, ...props }: TInputProps) => {
  console.log(123);
  return (
    <Container style={style}>
      <Icon>
        <MinusIcon stroke={colors.green} fill={colors.green} />
      </Icon>
      <Input
        keyboardType="number-pad"
        mask={RANGE_MASK}
        width={`${normHor(221)}px`}
        {...props}
      />
      <Icon>
        <AddIcon stroke={colors.green} fill={colors.green} />
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
