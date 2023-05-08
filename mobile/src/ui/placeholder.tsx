import React, { memo, useEffect, useLayoutEffect, useRef } from 'react';
import { View } from 'react-native';

import Reanimated, {
  useAnimatedStyle,
  useSharedValue,
  withTiming,
} from 'react-native-reanimated';
import styled from 'styled-components';

import { colors, normHor, normVert } from '@theme';
import { isIOS } from '@utils';

import { FontSize } from '~types';

type TProps = {
  text: string;
  isActive: boolean;
};

export const Placeholder = memo(({ text, isActive }: TProps) => {
  const firstRender = useRef(true);

  useLayoutEffect(() => {
    if (firstRender.current) {
      firstRender.current = false;
      return;
    }
  });

  const placeholderAnimY = useSharedValue(normVert(isIOS ? 14 : 10));
  const placeholderAnimSize = useSharedValue(+FontSize.S17.slice(0, -2));

  const duration = firstRender.current ? 0 : 300;

  const movePlaceholderYIn = () => {
    placeholderAnimY.value = withTiming(normVert(isIOS ? 6 : 2), {
      duration,
    });
  };

  const movePlaceholderYOut = () => {
    placeholderAnimY.value = withTiming(normVert(isIOS ? 14 : 10), {
      duration,
    });
  };

  const sizePlaceholderIn = () => {
    placeholderAnimSize.value = withTiming(+FontSize.S12.slice(0, -2), {
      duration,
    });
  };

  const sizePlaceholderOut = () => {
    placeholderAnimSize.value = withTiming(+FontSize.S17.slice(0, -2), {
      duration,
    });
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

  const animatedStyles = useAnimatedStyle(
    () => ({
      top: placeholderAnimY.value,
      fontSize: placeholderAnimSize.value,
    }),
    [placeholderAnimY.value, placeholderAnimSize.value],
  );

  return (
    <View pointerEvents="none" style={{ position: 'absolute' }}>
      <Container style={animatedStyles}>{text}</Container>
    </View>
  );
});

const Container = styled(Reanimated.Text)`
  position: absolute;
  color: ${colors.black5};
  font-size: ${FontSize.S17};
  margin-left: ${normHor(16)}px;
`;
