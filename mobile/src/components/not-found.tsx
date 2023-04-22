import React from 'react';
import { StyleSheet } from 'react-native';

import { NotFoundIcon } from '@assets';
import { t } from '@i18n';
import { colors, normVert } from '@theme';
import { Text } from '@ui';

import { FontSize } from '~types';

type TProps = {
  text?: string;
};

export const NotFound = ({ text = t('notFound.client') }: TProps) => (
  <>
    <NotFoundIcon style={styles.icon} />
    <Text
      align="center"
      style={styles.text}
      fontSize={FontSize.S17}
      color={colors.black4}
    >
      {t('notFound.title', { name: text })}
    </Text>
  </>
);

const styles = StyleSheet.create({
  icon: { marginLeft: 'auto', marginRight: 'auto', marginTop: normVert(125) },
  text: { marginTop: normVert(28) },
});
