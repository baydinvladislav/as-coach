import React from 'react';
import { Image, SafeAreaView, StyleProp, View, ViewStyle } from 'react-native';

import styled from 'styled-components';

import { BackgroundImage } from '@assets';
import { normHor, normVert } from '@theme';

type TProps = {
  children: React.ReactNode;
  style?: StyleProp<ViewStyle>;
  backgroundBlurRadius?: number;
  backgroundOpacity?: number;
  topOffset?: number;
};

export const Layout = ({
  children,
  style,
  backgroundBlurRadius = 0,
  backgroundOpacity = 1,
  topOffset = 60,
}: TProps) => (
  <SafeAreaView style={{ flex: 1 }}>
    <Background
      source={BackgroundImage}
      opacity={backgroundOpacity}
      blurRadius={backgroundBlurRadius}
    />
    <Container style={style} topOffset={topOffset}>
      {children}
    </Container>
  </SafeAreaView>
);

const Background = styled(Image)<{ opacity: number }>`
  position: absolute;
  width: 100%;
  opacity: ${({ opacity }) => opacity};
  top: 0;
`;

const Container = styled(View)<{ topOffset: number }>`
  padding-top: ${({ topOffset }) => normVert(topOffset)}px;
  padding-horizontal: ${normHor(16)}px;
  flex: 1;
`;
