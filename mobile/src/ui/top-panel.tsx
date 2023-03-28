import React from 'react';
import { TouchableOpacity, View } from 'react-native';

import styled from 'styled-components';

import { colors, normVert } from '@theme';
import { Text } from '@ui';

import { FontSize, FontWeight } from '~types';

type TProps = {
  title: string;
  buttonText?: string;
  onPress?: () => void;
};

export const TopPanel = ({ title, buttonText, onPress }: TProps) => (
  <TopPanelContainer>
    <Text weight={FontWeight.Bold} fontSize={FontSize.S16} color={colors.black}>
      {title}
    </Text>
    {buttonText && onPress && (
      <TouchableOpacity onPress={onPress}>
        <Text
          weight={FontWeight.Medium}
          fontSize={FontSize.S14}
          color={colors.blue}
        >
          {buttonText}
        </Text>
      </TouchableOpacity>
    )}
  </TopPanelContainer>
);

const TopPanelContainer = styled(View)`
  justify-content: space-between;
  flex-direction: row;
  margin-bottom: ${normVert(12)}px;
`;
