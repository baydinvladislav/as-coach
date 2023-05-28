import React, { useEffect, useState } from 'react';
import { StyleSheet, View } from 'react-native';

import moment from 'moment';
import { TouchableOpacity } from 'react-native-gesture-handler';

import { ArrowRightIcon } from '@assets';
import { colors, normHor, normVert } from '@theme';
import { Badge, BadgeStatuses, Text } from '@ui';

import { FontSize } from '~types';

type ClientCardProps = {
  firstName: string;
  lastName: string;
  dateEnd: string;
  onPress: () => void;
};

export const ClientCard: React.FC<ClientCardProps> = ({
  firstName,
  lastName,
  dateEnd,
  onPress,
}) => {
  const [bageStatus, setBageStatus] = useState<BadgeStatuses>(
    BadgeStatuses.PLAN_NOT_EXISTS,
  );
  const [toCompletion, setToCompletion] = useState<number>(0);

  useEffect(() => {
    setBageStatus(getStatus());
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const getStatus = () => {
    let status: BadgeStatuses;

    if (!dateEnd) {
      status = BadgeStatuses.PLAN_NOT_EXISTS;
    } else {
      const currentDate = moment();
      const dateCompletion = moment(dateEnd);

      const duration = moment.duration(dateCompletion.diff(currentDate));
      const differenceInDays = Math.round(duration.asDays());
      setToCompletion(differenceInDays);

      if (differenceInDays > 3) {
        status = BadgeStatuses.GOOD;
      } else if (0 < differenceInDays && differenceInDays < 3) {
        status = BadgeStatuses.WARNING;
      } else {
        status = BadgeStatuses.EXPIRED;
      }
    }
    return status;
  };

  const getLineColor = (status: string) => {
    switch (status) {
      case BadgeStatuses.GOOD:
        return colors.green;
      case BadgeStatuses.WARNING:
        return colors.orange;
      case BadgeStatuses.EXPIRED:
        return colors.red;
      case BadgeStatuses.PLAN_NOT_EXISTS:
        return colors.grey4;
      default:
        return colors.grey4;
    }
  };

  const getText = (days: number) => {
    if (!days) {
      return 'Нет плана';
    } else if (days < 0) {
      return `Истек ${Math.abs(days)} дней назад`;
    } else if (days > 0) {
      return `Истечет через ${days} дней`;
    } else {
      return 'Неизвестный промежуток';
    }
  };

  return (
    <TouchableOpacity onPress={onPress} style={styles.card}>
      <View
        style={[styles.line, { backgroundColor: getLineColor(bageStatus) }]}
      />
      <View style={styles.userInfo}>
        <View>
          <Badge text={getText(toCompletion)} status={bageStatus} />
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
