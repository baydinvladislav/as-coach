import React from 'react';
import {
  FlatList,
  ScrollView as RNScrollView,
  StyleProp,
  StyleSheet,
  View,
  ViewStyle,
} from 'react-native';

import { useSafeAreaInsets } from 'react-native-safe-area-context';
import styled from 'styled-components';

import { t } from '@i18n';
import { colors, normHor, normVert } from '@theme';
import { Button } from '@ui';
import { windowWidth } from '@utils';

import { ButtonType } from '~types';

type TProps = {
  children: React.ReactNode;
  style?: StyleProp<ViewStyle>;
  onCancel: () => void;
  onConfirm: () => void;
};

export const ScrollContainer = ({
  children,
  style,
  onCancel,
  onConfirm,
}: TProps) => {
  const insets = useSafeAreaInsets();

  return (
    <View style={{ flex: 1 }}>
      <ScrollView
        contentContainerStyle={[
          style,
          { flexGrow: 1, paddingBottom: normVert(136) },
        ]}
      >
        {children}
      </ScrollView>
      <ButtonsContainer bottom={insets.bottom}>
        <Button
          style={styles.button}
          type={ButtonType.PRIMARY}
          onPress={onConfirm}
        >
          {t('buttons.save')}
        </Button>
        <Button type={ButtonType.SECONDARY} onPress={onCancel}>
          {t('buttons.cancel')}
        </Button>
      </ButtonsContainer>
    </View>
  );
};

const styles = StyleSheet.create({
  button: { marginBottom: normVert(20) },
});

const ScrollView = styled(RNScrollView)``;

const ButtonsContainer = styled(View)<{ bottom: number }>`
  background-color: ${colors.grey2};
  width: ${windowWidth}px;
  padding-horizontal: ${normHor(16)}px;
  padding-vertical: ${normHor(20)}px;
  position: absolute;
  bottom: -${({ bottom }) => bottom}px;
  left: -${normVert(16)}px;
`;
