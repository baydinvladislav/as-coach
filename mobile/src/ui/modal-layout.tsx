import React, { PropsWithChildren } from 'react';
import { FlatList, View } from 'react-native';

import styled from 'styled-components';

import { TOP_PADDING } from '@constants';
import { colors, normHor, normVert } from '@theme';
import { Keyboard } from '@ui';
import { isIOS } from '@utils';

export const ModalLayout = ({
  children,
  isScroll = true,
  onPress,
}: PropsWithChildren<{ isScroll?: boolean; onPress: () => void }>) => {
  const Container = isScroll ? Keyboard : View;

  return (
    <Container
      onTouchEnd={onPress}
      style={{ flex: 1, paddingTop: isIOS ? TOP_PADDING : 0 }}
    >
      {isIOS && (
        <TopBackground>
          <Line />
        </TopBackground>
      )}
      <Background
        style={{ paddingTop: isIOS ? 0 : TOP_PADDING }}
        onTouchEnd={e => {
          e.stopPropagation();
        }}
      >
        {children}
      </Background>
    </Container>
  );
};

const Background = styled(View)`
  background-color: ${colors.black6};
  flex: 1;
  padding-top: ${normVert(40)}px;
`;

const TopBackground = styled(View)`
  background-color: ${colors.black6};
  flex: 1;
  position: absolute;
  top: ${normVert(34)}px;
  width: 100%;
  border-top-left-radius: 16px;
  border-top-right-radius: 16px;
  justify-content: center;
  align-items: center;
`;

const Line = styled(View)`
  background-color: ${colors.grey3};
  width: ${normHor(76)}px;
  height: ${normVert(6)}px;
  border-radius: 100px;
  margin-vertical: ${normVert(10)}px;
`;
