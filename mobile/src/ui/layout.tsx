import React from 'react';
import { Image, SafeAreaView, StyleProp, View, ViewStyle } from 'react-native';

import styled from 'styled-components';

import { BackgroundImage } from '@assets';
import { normHor } from '@theme';

type TProps = {
  children: React.ReactNode;
  style?: StyleProp<ViewStyle>;
};

export const Layout = ({ children, style }: TProps) => (
  <SafeAreaView style={style}>
    <Background source={BackgroundImage} opacity={1} blurRadius={0} />
    <Container>{children}</Container>
  </SafeAreaView>
);

const Background = styled(Image)<{ opacity: number }>`
  position: absolute;
  width: 100%;
  opacity: ${({ opacity }) => opacity};
  top: 0;
`;

const Container = styled(View)`
  padding-horizontal: ${normHor(16)}px;
`;
