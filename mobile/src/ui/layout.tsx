import React, { useEffect, useRef } from 'react';
import {
  Animated,
  Easing,
  Image,
  SafeAreaView,
  StyleProp,
  View,
  ViewStyle,
} from 'react-native';

import styled from 'styled-components';

import { BackgroundImage } from '@assets';
import { colors, normHor, normVert } from '@theme';

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
}: TProps) => {
  const opacityAnim = useRef(new Animated.Value(backgroundOpacity)).current;

  const changeOpacityUp = () => {
    Animated.timing(opacityAnim, {
      toValue: backgroundOpacity,
      duration: 100,
      useNativeDriver: true,
      easing: Easing.linear,
    }).start();
  };

  useEffect(() => {
    changeOpacityUp();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [backgroundOpacity]);

  return (
    <>
      <BackgroundColor />
      <Background
        blurRadius={backgroundBlurRadius}
        source={BackgroundImage}
        style={{ opacity: opacityAnim }}
      />
      <SafeAreaView style={{ flex: 1 }}>
        <Container style={style} topOffset={topOffset}>
          {children}
        </Container>
      </SafeAreaView>
    </>
  );
};

const Background = styled(Animated.Image)`
  position: absolute;
  width: 100%;
  height: 100%;
  top: 0;
`;

const BackgroundColor = styled(Animated.View)`
  position: absolute;
  width: 100%;
  height: 100%;
  top: 0;
  background-color: ${colors.black};
`;

const Container = styled(View)<{ topOffset: number }>`
  padding-top: ${({ topOffset }) => normVert(topOffset)}px;
  padding-horizontal: ${normHor(16)}px;
  flex: 1;
`;
