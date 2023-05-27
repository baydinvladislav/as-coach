import React from 'react';
import { StyleSheet, View } from 'react-native';

import { NotFoundIcon } from '@assets';
import { t } from '@i18n';
import { colors, normVert } from '@theme';
import { Text } from '@ui';

import { FontSize } from '~types';

type TProps = {
  text?: string;
};

export const NotFound = ({ text = t('notFound.client') }: TProps) => (
  <View style={styles.container}>
    <NotFoundIcon style={styles.icon} />
    <Text
      align="center"
      style={styles.text}
      fontSize={FontSize.S17}
      color={colors.black4}
    >
      {t('notFound.title', { name: text })}
    </Text>
  </View>
);

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
  },
  icon: {
    marginLeft: 'auto',
    marginRight: 'auto',
  },
  text: { marginTop: normVert(28) },
});
