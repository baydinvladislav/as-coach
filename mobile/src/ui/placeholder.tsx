import React, { useEffect, useLayoutEffect, useRef, useState } from 'react';
import { Animated } from 'react-native';

import { withAnchorPoint } from 'react-native-anchor-point';
import styled from 'styled-components';

import { colors, normHor, normVert } from '@theme';

import { FontSize } from '~types';

type TProps = {
  text: string;
  isActive: boolean;
};

export const Placeholder = ({ text, isActive }: TProps) => {
  const firstRender = useRef(true);

  useLayoutEffect(() => {
    if (firstRender.current) {
      firstRender.current = false;
      return;
    }
  });

  const [placeholderWidth, setPlaceholderWidth] = useState(0);
  const [placeholderHeight, setPlaceholderHeight] = useState(0);

  const placeholderAnimY = useRef(new Animated.Value(normVert(14))).current;
  const placeholderAnimSize = useRef(new Animated.Value(1)).current;

  const duration = firstRender.current ? 0 : 300;

  const movePlaceholderYIn = () => {
    Animated.timing(placeholderAnimY, {
      toValue: normVert(6),
      duration,
      useNativeDriver: true,
    }).start();
  };

  const movePlaceholderYOut = () => {
    Animated.timing(placeholderAnimY, {
      toValue: normVert(14),
      duration,
      useNativeDriver: true,
    }).start();
  };

  const sizePlaceholderIn = () => {
    Animated.timing(placeholderAnimSize, {
      toValue: 0.8,
      duration,
      useNativeDriver: true,
    }).start();
  };

  const sizePlaceholderOut = () => {
    Animated.timing(placeholderAnimSize, {
      toValue: 1,
      duration,
      useNativeDriver: true,
    }).start();
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

  const getTransform = () => {
    const transform = {
      transform: [
        {
          translateY: placeholderAnimY as unknown as number,
        },
        {
          translateX: normHor(16),
        },
        {
          scale: placeholderAnimSize as unknown as number,
        },
      ],
    };
    return withAnchorPoint(
      transform,
      { x: 0, y: 0 },
      { width: placeholderWidth, height: placeholderHeight },
    );
  };

  return (
    <Container
      onLayout={event => {
        setPlaceholderWidth(event.nativeEvent.layout.width);
        setPlaceholderHeight(event.nativeEvent.layout.height);
      }}
      style={getTransform()}
    >
      {text}
    </Container>
  );
};

const Container = styled(Animated.Text)`
  position: absolute;
  color: ${colors.black5};
  font-size: ${FontSize.S17};
`;
