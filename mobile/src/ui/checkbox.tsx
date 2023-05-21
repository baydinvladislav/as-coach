import React, { ChangeEvent, useEffect, useState } from 'react';
import {
  StyleProp,
  StyleSheet,
  TextInputProps,
  TouchableOpacity,
  View,
  ViewStyle,
} from 'react-native';

import styled from 'styled-components';

import { CheckIcon, MenuIcon } from '@assets';
import { colors, normHor, normVert } from '@theme';
import { Text } from '@ui';

import { FontSize } from '~types';

type TProps = {
  placeholder: string;
  style?: StyleProp<ViewStyle>;
  onChangeCheckbox: (e: string | React.ChangeEvent<any>) => void;
  value?: boolean;
  onDrag?: () => void;
} & Omit<TextInputProps, 'value'>;

export const Checkbox = ({
  placeholder,
  style,
  value,
  onDrag,
  ...props
}: TProps) => {
  const [isChecked, setIsChecked] = useState(value ?? false);

  const handleChange = () => {
    props.onChangeCheckbox?.({
      target: { value: !isChecked },
    } as ChangeEvent<any>);
    setIsChecked(isChecked => !isChecked);
  };

  useEffect(() => {
    setIsChecked(value ?? isChecked);
  }, [value]);

  return (
    <Container style={style} onPress={handleChange}>
      <Square isChecked={value || isChecked}>
        {(value || isChecked) && <CheckIcon />}
      </Square>
      <Text style={styles.text} fontSize={FontSize.S16} color={colors.white}>
        {placeholder}
      </Text>
      {onDrag && (
        <TouchableOpacity
          style={{ marginLeft: 'auto' }}
          onLongPress={onDrag}
          delayLongPress={0}
        >
          <MenuIcon />
        </TouchableOpacity>
      )}
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
