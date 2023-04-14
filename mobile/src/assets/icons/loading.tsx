import React, { useEffect } from 'react';
import { Animated, Easing } from 'react-native';

import Svg, { Path, SvgProps } from 'react-native-svg';

export const LoadingIcon = (props: SvgProps) => {
  const spinValue = new Animated.Value(0);

  useEffect(() => {
    Animated.loop(
      Animated.timing(spinValue, {
        toValue: 1,
        duration: 1000,
        easing: Easing.linear,
        useNativeDriver: true,
      }),
    ).start();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const spin = spinValue.interpolate({
    inputRange: [0, 1],
    outputRange: ['0deg', '360deg'],
  });

  return (
    <Animated.View style={{ transform: [{ rotate: spin }] }}>
      <Svg width="23" height="22" viewBox="0 0 23 22" fill="none" {...props}>
        <Path
          d="M11.5 1C17.0228 1 21.5 5.47715 21.5 11C21.5 16.5228 17.0228 21 11.5 21C5.97715 21 1.5 16.5229 1.5 11"
          stroke="#192026"
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
        />
      </Svg>
    </Animated.View>
  );
};
