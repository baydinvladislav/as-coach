import React, { memo } from 'react';
import { StyleSheet, TouchableOpacity, View } from 'react-native';

import moment from 'moment';

import { colors, normHor, normVert } from '@theme';
import { Text } from '@ui';
import { getWeek } from '@utils';

import { FontSize } from '~types';

const CustomDay = ({
  date,
  state,
  start,
  end,
  onDayPress,
}: {
  date: string;
  state: string;
  start: string;
  end: string;
  onDayPress: (day: string) => void;
}) => {
  const selected = { start, end };
  const isStart = date === selected.start;
  const isEnd = date === selected.end;
  const isSelect = isStart || isEnd;

  const isStartEmpty = selected.start === '';
  const isEndEmpty = selected.end === '';

  const isToday =
    moment(new Date(date)).format('YYYY-MM-DD') ===
    moment(new Date()).format('YYYY-MM-DD');

  if (new Date(date) <= new Date() && !isToday) {
    state = 'disabled';
  }

  const currentDayOfWeek = new Date(date).getDay();
  const currentDay = new Date(date).getDate();

  const isSixWeek = getWeek(new Date(date)) === 5;

  const isFirstDay = currentDayOfWeek === 0;
  const isLastDay = currentDayOfWeek === 6;

  const isLastDayMonth =
    new Date(date).getDate() ==
    +moment(date, 'YYYY-MM-DD').endOf('month').format('DD');

  const isFirstDayMonth = new Date(date).getDate() == 1;

  const isBetween =
    new Date(date) > new Date(selected.start) &&
    new Date(date) < new Date(selected.end);

  const isVisibleBackground =
    ((isSelect && ((isStart && !isLastDay) || (isEnd && !isFirstDay))) ||
      isBetween) &&
    state !== 'disabled';

  const Background = isVisibleBackground ? View : React.Fragment;
  const props =
    isVisibleBackground && state !== 'disabled'
      ? {
          style: [
            !isEndEmpty &&
              !isStartEmpty &&
              (!isSelect || !isLastDayMonth) &&
              (!isSelect || !isFirstDayMonth) &&
              styles.selectedBackground,
            isStart && !isLastDay && styles.start,
            isEnd && !isFirstDay && styles.end,
            isBetween && styles.center,
            !isSelect && (isFirstDay || isFirstDayMonth) && styles.first,
            !isSelect && (isLastDay || isLastDayMonth) && styles.last,
          ],
        }
      : undefined;
  return (
    <View style={styles.wrapper}>
      <Background {...props} />
      <TouchableOpacity
        activeOpacity={1}
        style={[
          styles.cell,
          isSixWeek && styles.marginBottom,
          isToday && styles.today,
          isSelect && state !== 'disabled' && styles.selected,
        ]}
        onPress={() => onDayPress(date)}
      >
        <Text
          fontSize={FontSize.S16}
          style={[
            styles.customDay,
            isSelect && state !== 'disabled'
              ? styles.selectedText
              : state === 'disabled'
              ? styles.disabledText
              : styles.defaultText,
          ]}
        >
          {currentDay}
        </Text>
      </TouchableOpacity>
    </View>
  );
};

export default memo(CustomDay);

const styles = StyleSheet.create({
  marginBottom: {
    marginBottom: normVert(60),
  },
  cell: {
    width: normHor(32),
    height: normVert(32),
    alignItems: 'center',
    justifyContent: 'center',
  },
  wrapper: {
    position: 'relative',
  },
  selectedBackground: {
    position: 'absolute',
    width: normHor(32),
    height: normVert(32),
    backgroundColor: colors.green4,
  },
  start: {
    right: normHor(-21),
  },
  end: {
    left: normHor(-21),
  },
  center: {
    width: normHor(60),
    left: 0,
    right: 0,
  },
  selected: {
    backgroundColor: colors.green,
    borderRadius: 100,
  },
  today: {
    borderColor: colors.grey10,
    borderWidth: 1,
    borderRadius: 100,
  },
  first: {
    borderTopLeftRadius: 100,
    borderBottomLeftRadius: 100,
  },
  last: {
    width: normHor(32),
    borderTopRightRadius: 100,
    borderBottomRightRadius: 100,
  },
  customDay: {
    textAlign: 'center',
  },
  betweenText: {
    color: colors.red,
  },
  selectedText: {
    color: colors.black,
  },
  disabledText: {
    color: colors.grey8,
  },
  defaultText: {
    color: colors.white,
  },
});
