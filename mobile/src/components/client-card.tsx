import React, { useEffect, useState } from 'react';
import { StyleSheet, View } from 'react-native';

import { TouchableOpacity } from 'react-native-gesture-handler';

import { ArrowRightIcon } from '@assets';
import { colors, normHor, normVert } from '@theme';
import { Badge, BadgeStatuses, Text } from '@ui';

import { FontSize } from '~types';

type ClientCardProps = {
  firstName: string;
  lastName: string;
  text: string;
  status: BadgeStatuses;
  onPress: () => void;
};

export const ClientCard: React.FC<ClientCardProps> = ({
  firstName,
  lastName,
  text,
  status,
  onPress,
}) => {
  const [lineColor, setLineColor] = useState('');

  const switchLineColor = (status: BadgeStatuses) => {
    let color = '';

    if (status === BadgeStatuses.GOOD) {
      color = colors.green;
    } else if (status === BadgeStatuses.WARNING) {
      color = colors.orange;
    } else if (status === BadgeStatuses.EXPIRED) {
      color = colors.red;
    } else if (status === BadgeStatuses.PLAN_NOT_EXISTS) {
      color = colors.grey4;
    }
    setLineColor(color);
  };

  useEffect(() => {
    switchLineColor(status);
  }, [status]);

  return (
    <TouchableOpacity onPress={onPress} style={styles.card}>
      <View style={[styles.line, { backgroundColor: lineColor }]} />
      <View style={styles.userInfo}>
        <View>
          <Badge status={status} text={text} />
        </View>
        <View style={styles.names}>
          <Text color={colors.white} fontSize={FontSize.S17}>
            {lastName}
          </Text>
          <Text
            style={{ marginLeft: normHor(4) }}
            color={colors.white}
            fontSize={FontSize.S17}
          >
            {firstName}
          </Text>
        </View>
      </View>
      <View style={styles.arrowContainer}>
        <ArrowRightIcon />
      </View>
    </TouchableOpacity>
  );
};

const styles = StyleSheet.create({
  card: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingTop: normVert(16),
    paddingBottom: normVert(18),
    backgroundColor: colors.grey5,
    borderRadius: 12,
    marginVertical: normVert(10),
  },

  line: {
    height: normVert(60),
    position: 'absolute',
    marginLeft: normVert(8),
    width: normHor(3),
    borderRadius: 10,
  },

  userInfo: {
    height: normVert(50),
    flexDirection: 'column',
    marginLeft: normHor(24),
    borderRadius: 10,
    justifyContent: 'space-between',
  },

  names: {
    alignSelf: 'flex-start',
    flexDirection: 'row',
  },

  arrowContainer: {
    flexDirection: 'column',
    justifyContent: 'center',
    alignItems: 'flex-end',
    marginRight: normVert(32),
  },
});
