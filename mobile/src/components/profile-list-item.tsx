import React, { ReactNode } from 'react';
import { StyleSheet, View } from 'react-native';

import { TouchableOpacity } from 'react-native-gesture-handler';
import styled from 'styled-components';

import { colors, normHor, normVert } from '@theme';
import { Text } from '@ui';

import { FontSize } from '~types';

type TProps = {
  name: string;
  icon: ReactNode;
  rightIcon?: ReactNode;
  color?: string;
  index: number;
  handlePress: () => void;
};

export const ProfileListItem = ({
  name,
  icon,
  rightIcon,
  color = colors.white,
  index,
  handlePress,
}: TProps) => (
  <Container hasBorderTop={index !== 0} onPress={handlePress}>
    <View style={styles.container}>
      {icon}
      <Text style={styles.text} fontSize={FontSize.S16} color={color}>
        {name}
      </Text>
    </View>
    {rightIcon}
  </Container>
);

const styles = StyleSheet.create({
  container: { flexDirection: 'row', alignItems: 'center' },
  text: { marginLeft: normHor(14) },
});

const Container = styled(TouchableOpacity)<{ hasBorderTop: boolean }>`
  flex-direction: row;
  justify-content: space-between;
  align-items: center;
  padding-vertical: ${normVert(24)}px;
  ${({ hasBorderTop }) =>
    hasBorderTop &&
    `border-top-width: 1px;
     border-top-color: ${colors.black3};`}
`;
