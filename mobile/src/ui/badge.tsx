import React from 'react';
import { View } from 'react-native';

import styled from 'styled-components';

import { colors, normHor, normVert } from '@theme';

import { FontSize, FontWeight } from '~types';

import { Text } from './text';

export enum BadgeStatuses {
  GOOD = 'good',
  WARNING = 'warning',
  WARNING_TODAY = 'warning_today',
  WARNING_TOMORROW = 'warning_tomorrow',
  EXPIRED = 'expired',
  PLAN_NOT_EXISTS = 'plan_not_exists',
}

type TProps = {
  status: BadgeStatuses;
  text: string;
};

export const Badge: React.FC<TProps> = ({ status, text }) => (
  <Background status={status}>
    <Text
      style={{ textTransform: 'uppercase' }}
      fontSize={FontSize.S10}
      color={switchFontColor(status)}
      weight={FontWeight.Bold}
    >
      {text}
    </Text>
  </Background>
);

const Background = styled(View)<{ status: BadgeStatuses }>`
  background-color: ${({ status }) => switchBackgroundColor(status)};
  align-self: flex-start;
  padding: ${normVert(2)}px ${normHor(6)}px;
  border-radius: 6px;
`;

const switchFontColor = (status: BadgeStatuses) => {
  switch (status) {
    case BadgeStatuses.GOOD:
      return colors.green;
    case BadgeStatuses.WARNING:
    case BadgeStatuses.WARNING_TODAY:
    case BadgeStatuses.WARNING_TOMORROW:
      return colors.orange;
    case BadgeStatuses.EXPIRED:
      return colors.red;
    case BadgeStatuses.PLAN_NOT_EXISTS:
      return colors.grey4;
    default:
      return colors.grey4;
  }
};

const switchBackgroundColor = (status: BadgeStatuses) => {
  switch (status) {
    case BadgeStatuses.GOOD:
      return colors.green3;
    case BadgeStatuses.WARNING:
    case BadgeStatuses.WARNING_TODAY:
    case BadgeStatuses.WARNING_TOMORROW:
      return colors.orange2;
    case BadgeStatuses.EXPIRED:
      return colors.red2;
    case BadgeStatuses.PLAN_NOT_EXISTS:
      return colors.grey5;
    default:
      return colors.grey5;
  }
};
