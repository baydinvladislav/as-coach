import React from 'react';
import { StyleSheet, View } from 'react-native';

import { TouchableOpacity } from 'react-native-gesture-handler';

import { ArrowRightIcon } from '@assets';
import { colors, normHor, normVert } from '@theme';
import { Text } from '@ui';

import { FontSize } from '~types';

type ClientCardProps = {
  firstName: string;
  lastName: string;
  onPress: () => void;
};

export const ClientCard: React.FC<ClientCardProps> = ({
  firstName,
  lastName,
  onPress,
}) => (
  <TouchableOpacity onPress={onPress} style={styles.card}>
    <View style={styles.line} />
    <View style={styles.userInfo}>
      <Text
        style={styles.lastName}
        color={colors.white}
        fontSize={FontSize.S17}
      >
        {lastName}
      </Text>
      <Text
        style={styles.firstName}
        color={colors.white}
        fontSize={FontSize.S17}
      >
        {firstName}
      </Text>
    </View>
    <View style={styles.arrowContainer}>
      <ArrowRightIcon />
    </View>
  </TouchableOpacity>
);

const styles = StyleSheet.create({
  card: {
    flexDirection: 'row',
    justifyContent: 'flex-start',
    alignItems: 'center',
    backgroundColor: colors.grey5,
    width: normHor(343),
    height: normVert(84),
    borderRadius: 12,
    marginVertical: normVert(10),
  },

  line: {
    backgroundColor: colors.green,
    height: normVert(60),
    position: 'absolute',
    marginLeft: normVert(8),
    width: normHor(3),
    borderRadius: 10,
  },

  userInfo: {
    flex: 0.8,
    height: normVert(50),
    flexDirection: 'row',
    marginLeft: normHor(24),
    borderRadius: 10,
  },

  lastName: {
    alignSelf: 'flex-end',
  },

  firstName: {
    alignSelf: 'flex-end',
    marginLeft: normHor(4),
  },

  arrowContainer: {
    flexDirection: 'column',
    justifyContent: 'center',
    alignItems: 'flex-end',
    flex: 0.2,
    marginRight: normVert(32),
  },
});
