import React, { useCallback, useEffect, useRef } from 'react';
import { Animated, Easing, StyleProp, View, ViewStyle } from 'react-native';

import { Edge, SafeAreaView } from 'react-native-safe-area-context';
import styled from 'styled-components';

import { BackgroundImage } from '@assets';
import { colors, normHor } from '@theme';
import { windowHeight, windowWidth } from '@utils';

type TProps = {
  children: React.ReactNode;
  style?: StyleProp<ViewStyle>;
  backgroundBlurRadius?: number;
  backgroundOpacity?: number;
  edges?: Edge[];
};

export const Layout = ({
  children,
  style,
  backgroundBlurRadius = 0,
  backgroundOpacity = 1,
  edges,
}: TProps) => {
  const opacityAnim = useRef(new Animated.Value(backgroundOpacity)).current;

  const changeOpacityUp = useCallback(() => {
    Animated.timing(opacityAnim, {
      toValue: backgroundOpacity,
      duration: 100,
      useNativeDriver: true,
      easing: Easing.linear,
    }).start();
  }, [backgroundOpacity, opacityAnim]);

  useEffect(() => {
    changeOpacityUp();
  }, [backgroundOpacity, changeOpacityUp]);

  return (
    <SafeAreaView style={{ flex: 1 }} edges={edges}>
      <BackgroundColor />
      <Background
        blurRadius={backgroundBlurRadius}
        source={BackgroundImage}
        style={{ opacity: opacityAnim }}
      />
      <Container style={style}>{children}</Container>
    </SafeAreaView>
  );
};

const Background = styled(Animated.Image)`
  position: absolute;
  width: ${windowWidth}px;
  height: ${windowHeight}px;
`;

const BackgroundColor = styled(Animated.View)`
  position: absolute;
  width: ${windowWidth}px;
  height: ${windowHeight}px;
  top: 0;
  background-color: ${colors.black};
`;

const Container = styled(View)`
  padding-horizontal: ${normHor(16)}px;
  flex: 1;
`;
