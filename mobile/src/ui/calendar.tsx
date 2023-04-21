import React, { ChangeEvent, ComponentType, useMemo } from 'react';
import { StyleSheet, TextStyle, TouchableOpacity, View } from 'react-native';

import moment from 'moment';
import { CalendarList, DateData, LocaleConfig } from 'react-native-calendars';
import { DayProps } from 'react-native-calendars/src/calendar/day';

import { colors, normHor, normVert } from '@theme';
import { windowWidth } from '@utils';

import { FontSize } from '~types';

import { Text } from './text';

LocaleConfig.locales['ru'] = {
  monthNames: [
    'Январь',
    'Февраль',
    'Март',
    'Апрель',
    'Май',
    'Июнь',
    'Июль',
    'Август',
    'Сентябрь',
    'Октябрь',
    'Ноябрь',
    'Декабрь',
  ],
  monthNamesShort: [
    'янв.',
    'февр.',
    'март',
    'апр.',
    'май',
    'июнь',
    'июль',
    'авг.',
    'сент.',
    'окт.',
    'нояб.',
    'дек.',
  ],
  dayNames: [
    'Понедельник',
    'Вторник',
    'Среда',
    'Четверг',
    'Пятница',
    'Суббота',
    'Воскресенье',
  ],
  dayNamesShort: ['ПН', 'ВТ', 'СР', 'ЧТ', 'ПТ', 'СС', 'ВС'],
  today: 'Сегодня',
};

LocaleConfig.defaultLocale = 'ru';

const RANGE = 2;

const INITIAL_DATE = '2022-04-20';

type TProps = {
  horizontalView?: boolean;
  values: { start: string; end: string };
  onChange: {
    start: (e: string | React.ChangeEvent<any>) => void;
    end: (e: string | React.ChangeEvent<any>) => void;
  };
  dateType: 'start' | 'end' | null;
};

export const Calendar = ({ values, onChange, dateType, ...props }: TProps) => {
  const { horizontalView } = props;

  const selected = useMemo(
    () => ({
      start: values.start,
      end: values.end,
    }),
    [values.end, values.start],
  );

  const isStartEmpty = selected.start === '';
  const isEndEmpty = selected.end === '';

  const onDayPress = (day: DateData) => {
    const value = {
      target: { value: day.dateString },
    } as ChangeEvent<any>;

    if (
      dateType === 'start' &&
      (isEndEmpty || new Date(day.dateString) < new Date(selected.end))
    ) {
      onChange.start(value);
    }
    if (
      dateType === 'end' &&
      (isStartEmpty || new Date(day.dateString) > new Date(selected.start))
    ) {
      onChange.end(value);
    }
  };

  const CustomDay = ({ date, state }: { date: DateData; state: any }) => {
    const isStart = date.dateString === selected.start;
    const isEnd = date.dateString === selected.end;
    const isSelect = isStart || isEnd;

    const isFirstDay = new Date(date.dateString).getDay() === 0;
    const isLastDay = new Date(date.dateString).getDay() === 6;

    const isLastDayMonth =
      new Date(date.dateString).getDate() ==
      +moment(date.dateString, 'DD.mm.yy').endOf('month').format('DD');

    const isFirstDayMonth = new Date(date.dateString).getDate() == 1;

    const isBetween =
      new Date(date.dateString) > new Date(selected.start) &&
      new Date(date.dateString) < new Date(selected.end);

    const isVisibleBackground =
      ((isSelect && ((isStart && !isLastDay) || (isEnd && !isFirstDay))) ||
        isBetween) &&
      state !== 'disabled';

    const Background = isVisibleBackground ? View : React.Fragment;
    const props =
      isVisibleBackground && state !== 'disabled'
        ? {
            style: [
              !isEndEmpty && !isStartEmpty && styles.selectedBackground,
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
            {date.day}
          </Text>
        </TouchableOpacity>
      </View>
    );
  };

  return (
    <View style={{ flex: 1 }}>
      <CalendarList
        style={{
          width: windowWidth + normHor(22),
          marginLeft: normHor(-28),
          height: '100%',
        }}
        calendarStyle={styles.calendarStyle}
        current={INITIAL_DATE}
        pastScrollRange={0}
        futureScrollRange={RANGE}
        theme={theme}
        dayComponent={
          CustomDay as
            | ComponentType<DayProps & { date?: DateData | undefined }>
            | undefined
        }
        markingType={'period'}
        renderHeader={!horizontalView ? renderCustomHeader : undefined}
        calendarHeight={normVert(442)}
        horizontal={horizontalView}
        pagingEnabled={horizontalView}
        staticHeader={horizontalView}
      />
    </View>
  );
};

const theme = {
  calendarBackground: colors.black2,
  weekVerticalMargin: normVert(6),
};

const styles = StyleSheet.create({
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
  first: {
    borderTopLeftRadius: 100,
    borderBottomLeftRadius: 100,
  },
  last: {
    width: normHor(32),
    borderTopRightRadius: 100,
    borderBottomRightRadius: 100,
  },
  calendarStyle: {
    width: '100%',
    marginBottom: normVert(-120),
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
  header: {
    flexDirection: 'row',
    width: '100%',
    justifyContent: 'space-between',
    marginBottom: normVert(24),
  },
  month: {
    marginLeft: 5,
  },
});

function renderCustomHeader(date: any) {
  const header = date.toString('MMMM yyyy');
  const [month, year] = header.split(' ');
  const textStyle: TextStyle = {
    fontSize: 18,
    fontWeight: 'bold',
    color: colors.white,
  };

  return (
    <View style={styles.header}>
      <Text style={[styles.month, textStyle]}>{`${month}, ${year}`}</Text>
    </View>
  );
}
