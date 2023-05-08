import React from 'react';
import {
  ScrollView,
  StyleProp,
  StyleSheet,
  TouchableOpacity,
  View,
  ViewStyle,
} from 'react-native';

import { NestableScrollContainer } from 'react-native-draggable-flatlist';
import styled from 'styled-components';

import { SupersetIcon, TrashIcon } from '@assets';
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
};

export const ViewWithButtons = ({
  children,
  style,
  containerStyle,
  onCancel,
  onConfirm,
  confirmText = t('buttons.save'),
  cancelText = t('buttons.cancel'),
  isLoading,
  isScroll = false,
  onSuperset,
  onDelete,
  isSelected,
  isDraggable,
}: TProps) => {
  const Container = isScroll
    ? isDraggable
      ? NestableScrollContainer
      : ScrollView
    : View;
  return (
    <ChildrenContainer style={style}>
      {onSuperset && (
        <Circle1 activeOpacity={isSelected ? 0.5 : 1} onPress={onSuperset}>
          <SupersetIcon opacity={isSelected ? 1 : 0.5} />
        </Circle1>
      )}
      {onDelete && (
        <Circle2 activeOpacity={isSelected ? 0.5 : 1} onPress={onDelete}>
          <TrashIcon opacity={isSelected ? 1 : 0.5} />
        </Circle2>
      )}
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

const Circle1 = styled(TouchableOpacity)`
  position: absolute;
  z-index: 1;
  right: ${normHor(24)}px;
  bottom: ${normVert(174)}px;
  border-radius: 100px;
  width: ${normHor(52)}px;
  height: ${normVert(52)}px;
  background-color: ${colors.grey};
  justify-content: center;
  align-items: center;
`;

const Circle2 = styled(TouchableOpacity)`
  position: absolute;
  z-index: 1;
  right: ${normHor(88)}px;
  bottom: ${normVert(174)}px;
  border-radius: 100px;
  width: ${normHor(52)}px;
  height: ${normVert(52)}px;
  background-color: ${colors.grey};
  justify-content: center;
  align-items: center;
`;
