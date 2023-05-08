import React, { useEffect, useRef, useState } from 'react';
import { StyleSheet, View } from 'react-native';

import { getCustomerPlanDetail } from '@api';
import { ExercisesList } from '@components';
import { t } from '@i18n';
import { RoutesProps, Screens, useNavigation } from '@navigation';
import { colors, normVert } from '@theme';
import { ModalLayout, RowBorder, Text, ViewWithButtons } from '@ui';

import { FontSize } from '~types';

const EXERCISES = [
  {
    name: 'Test',
    exercises: [
      {
        id: '4283c861-eb38-4be6-ad5a-0d48f54e9415',
        name: 'test',
        sets: [12, 12, 12],
      },
      {
        id: '4283c861-eb38-4be6-ad5a-0d48f54e9415',
        name: 'test',
        sets: [12, 12, 12],
      },
      {
        id: '4283c861-eb38-4be6-ad5a-0d48f54e9415',
        name: 'test',
        sets: [12, 12, 12],
      },
      {
        id: '4283c861-eb38-4be6-ad5a-0d48f54e9415',
        name: 'test',
        sets: [12, 12, 12],
      },
      {
        id: '4283c861-eb38-4be6-ad5a-0d48f54e9415',
        name: 'test',
        sets: [12, 12, 12],
      },
      {
        id: '4283c861-eb38-4be6-ad5a-0d48f54e9415',
        name: 'test',
        sets: [12, 12, 12],
      },
      {
        id: '4283c861-eb38-4be6-ad5a-0d48f54e9415',
        name: 'test',
        sets: [12, 12, 12],
      },
      {
        id: '4283c861-eb38-4be6-ad5a-0d48f54e9415',
        name: 'test',
        sets: [12, 12, 12],
      },
    ],
  },
  {
    name: 'Test',
    exercises: [
      {
        id: '7ea243a7-356a-443e-ac44-697320be8f08',
        name: 'test',
        sets: [12, 12, 12],
      },
    ],
  },
  {
    name: 'Test',
    exercises: [
      {
        id: '7ea243a7-356a-443e-ac44-697320be8f08',
        name: 'test',
        sets: [12, 12, 12],
      },
    ],
  },
];

export const DetailPlanScreen = ({ route }: RoutesProps) => {
  const cardsRef = useRef<{
    setCards: (value: React.SetStateAction<boolean[]>) => void;
    cards: boolean[];
    handleOpen: (key: number) => void;
  }>(null);
  const [data, setData] = useState<any>();
  const { navigate } = useNavigation();

  const { id, planId } = route.params as { id: string; planId: string };

  useEffect(() => {
    getCustomerPlanDetail(id, planId).then(data => setData(data));
  }, [id, planId]);

  const handleOpen = (key: number) => {
    cardsRef.current?.handleOpen?.(key);
  };

  return (
    <ModalLayout>
      <ViewWithButtons
        style={{ justifyContent: 'space-between' }}
        onCancel={() => navigate(Screens.DetailClient)}
        cancelText={t('buttons.ok')}
        isScroll={true}
      >
        <Text style={styles.title} color={colors.white} fontSize={FontSize.S24}>
          14 авг — 26 авг
        </Text>
        <RowBorder
          title="Питание"
          cells={[
            { title: 'Белки', value: '180 гр' },
            { title: 'Углеводы', value: '200 гр' },
            { title: 'Жиры', value: '50 гр' },
          ]}
        />
        <RowBorder
          title="Время отдыха"
          cells={[
            { title: 'Между подходами', value: '60 сек' },
            { title: 'Между упражнениями', value: '120 сек' },
          ]}
        />
        <Text
          color={colors.white}
          style={styles.contentTitle}
          fontSize={FontSize.S24}
        >
          Тренировки
        </Text>
        <ExercisesList exercises={EXERCISES} />
        <Text
          color={colors.white}
          style={styles.contentTitle}
          fontSize={FontSize.S24}
        >
          Заметки от тренера
        </Text>
        <Text color={colors.white} fontSize={FontSize.S16}>
          Lorem ipsum dolor sit amet consectetur adipisicing elit.
          Exercitationem, harum similique fugiat dolor laboriosam excepturi unde
          laborum! Corporis saepe reprehenderit ullam rerum quasi exercitationem
          magnam illo facilis, est iure illum.
        </Text>
      </ViewWithButtons>
    </ModalLayout>
  );
};

const styles = StyleSheet.create({
  title: {
    textTransform: 'uppercase',
    marginBottom: normVert(40),
  },
  contentTitle: { marginBottom: normVert(19) },
  list: {
    marginBottom: normVert(21),
  },
});
