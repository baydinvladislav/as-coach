import React, { ChangeEvent, useState } from 'react';
import {
  StyleProp,
  StyleSheet,
  TextInputProps,
  TouchableOpacity,
  View,
  ViewStyle,
} from 'react-native';

import styled from 'styled-components';

import { CheckIcon } from '@assets';
import { colors, normHor, normVert } from '@theme';
import { Text } from '@ui';

import { FontSize } from '~types';

type TProps = {
  placeholder: string;
  style?: StyleProp<ViewStyle>;
  value: boolean;
  onChangeCheckbox: (e: string | React.ChangeEvent<any>) => void;
} & Omit<TextInputProps, 'value'>;

export const Checkbox = ({ placeholder, style, value, ...props }: TProps) => {
  const [isChecked, setIsChecked] = useState(value);

  const handleChange = () => {
    props.onChangeCheckbox?.({
      target: { value: !isChecked },
    } as ChangeEvent<any>);
    setIsChecked(isChecked => !isChecked);
  };

  return (
    <Container style={style} onPress={handleChange}>
      <Square isChecked={isChecked}>{isChecked && <CheckIcon />}</Square>
      <Text style={styles.text} fontSize={FontSize.S16} color={colors.black4}>
        {placeholder}
      </Text>
    </Container>
  );
};

const styles = StyleSheet.create({
  text: { marginLeft: normHor(14) },
});

const Container = styled(TouchableOpacity)`
  flex-direction: row;
  align-items: center;
`;

const Square = styled(View)<{ isChecked: boolean }>`
  width: ${normHor(22)}px;
  height: ${normVert(22)}px;
  border-radius: 6px;
  border: 1px solid
    ${({ isChecked }) =>
      isChecked ? colors.green : 'rgba(255, 255, 255, 0.5)'};
  background-color: ${({ isChecked }) =>
    isChecked ? colors.green : colors.transparent};
  align-items: center;
  justify-content: center;
`;
