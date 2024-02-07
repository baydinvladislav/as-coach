import React, { ReactNode } from 'react';
import {
  ScrollView,
  StyleProp,
  StyleSheet,
  View,
  ViewStyle,
} from 'react-native';

import { NestableScrollContainer } from 'react-native-draggable-flatlist';
import styled from 'styled-components';

import { t } from '@i18n';
import { colors, normHor, normVert } from '@theme';
import { Button } from '@ui';
import { windowWidth } from '@utils';

import { ButtonType } from '~types';

type TProps = {
  children: React.ReactNode;
  style?: StyleProp<ViewStyle>;
  containerStyle?: StyleProp<ViewStyle>;
  onCancel?: () => void;
  onConfirm?: () => void;
  isLoading?: boolean;
  confirmText?: string;
  cancelText?: string;
  isScroll?: boolean;
  withConfirm?: boolean;
  onDelete?: () => void;
  onSuperset?: () => void;
  isSelected?: boolean;
  isDraggable?: boolean;
  circles?: ReactNode;
};

export const ViewWithButtons = ({
  children,
  style,
  containerStyle,
  onCancel,
  onConfirm,
  confirmText = t('buttons.save'),
  cancelText = t('buttons.cancel'),
  isLoading = false,
  isScroll = false,
  circles: Circles,
  isDraggable,
}: TProps) => {
  const Container = isScroll
    ? isDraggable
      ? NestableScrollContainer
      : ScrollView
    : View;
  return (
    <ChildrenContainer style={style}>
      {Circles}
      <Container
        style={[styles.container, containerStyle]}
        contentContainerStyle={[styles.container, containerStyle]}
      >
        {children}
      </Container>
      <ButtonsContainer>
        {onConfirm && (
          <Button
            style={styles.button}
            type={ButtonType.PRIMARY}
            onPress={onConfirm}
            isLoading={isLoading}
          >
            {confirmText}
          </Button>
        )}
        {onCancel && (
          <Button type={ButtonType.SECONDARY} onPress={onCancel}>
            {cancelText}
          </Button>
        )}
      </ButtonsContainer>
    </ChildrenContainer>
  );
};

const styles = StyleSheet.create({
  button: { marginBottom: normVert(20) },
  container: { paddingBottom: normVert(16) },
});

const ChildrenContainer = styled(View)`
  padding-horizontal: ${normHor(16)}px;
  flex: 1;
`;

const ButtonsContainer = styled(View)`
  background-color: ${colors.grey2};
  width: ${windowWidth}px;
  left: -${normHor(16)}px;
  padding-horizontal: ${normHor(16)}px;
  padding-vertical: ${normVert(20)}px;
`;
