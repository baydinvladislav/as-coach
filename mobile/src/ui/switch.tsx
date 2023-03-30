import React, { useState } from 'react';
import { Switch as RNSwitch } from 'react-native';

import { colors } from '@theme';

export const Switch = () => {
  const [state, setState] = useState({
    value: false,
  });
  const toggleSwitch = () => {
    setState(state => ({ ...state, value: !state.value }));
  };
  return (
    <RNSwitch
      style={{
        transform: [{ scaleX: 0.7 }, { scaleY: 0.7 }],
      }}
      trackColor={{ false: '#eee', true: colors.green }}
      thumbColor={state.value ? colors.black : colors.green}
      ios_backgroundColor={colors.black3}
      value={state.value}
      onValueChange={toggleSwitch}
    />
  );
};
