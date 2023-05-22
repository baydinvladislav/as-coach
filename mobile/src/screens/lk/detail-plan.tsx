import React, { useEffect, useState } from 'react';
import { StyleSheet, View } from 'react-native';

import moment from 'moment';

import { getCustomerPlanDetail } from '@api';
import { ExercisesList } from '@components';
import { t } from '@i18n';
import { RoutesProps, useNavigation } from '@navigation';
import { colors, normVert } from '@theme';
import { Loader, ModalLayout, RowBorder, Text, ViewWithButtons } from '@ui';

import { FontSize, TPlanType } from '~types';

export const DetailPlanScreen = ({ route }: RoutesProps) => {
  const [data, setData] = useState<TPlanType>();
  const { goBack } = useNavigation();

  const { id, planId } = route.params as { id: string; planId: string };

  useEffect(() => {
    getCustomerPlanDetail(id, planId).then(({ data }) => setData(data));
  }, [id, planId]);

  return (
    <ModalLayout>
      {data ? (
        <ViewWithButtons
          style={{ justifyContent: 'space-between' }}
          onCancel={goBack}
          cancelText={t('buttons.ok')}
          isScroll={true}
        >
          <Text
            style={styles.title}
            color={colors.white}
            fontSize={FontSize.S24}
          >
            {moment(data.start_date).format('D MMM').slice(0, -1)} —{' '}
            {moment(data.end_date).format('D MMM').slice(0, -1)}
          </Text>
          <RowBorder
            title="Питание"
            cells={[
              { title: 'Белки', value: `${data.proteins} гр` },
              { title: 'Углеводы', value: `${data.carbs} гр` },
              { title: 'Жиры', value: `${data.fats} гр` },
            ]}
          />
          <Text
            color={colors.white}
            style={styles.contentTitle}
            fontSize={FontSize.S24}
          >
            Тренировки
          </Text>
          <ExercisesList exercises={data.trainings} />
          <RowBorder
            title="Время отдыха"
            cells={[
              { title: 'Между подходами', value: `${data.set_rest} сек` },
              {
                title: 'Между упражнениями',
                value: `${data.exercise_rest} сек`,
              },
            ]}
          />
          <Text
            color={colors.white}
            style={styles.contentTitle}
            fontSize={FontSize.S24}
          >
            Заметки от тренера
          </Text>
          <Text color={colors.white} fontSize={FontSize.S16}>
            {data.notes}
          </Text>
        </ViewWithButtons>
      ) : (
        <View style={styles.loader}>
          <Loader />
        </View>
      )}
    </ModalLayout>
  );
};

const styles = StyleSheet.create({
  loader: {
    flex: 1,
    justifyContent: 'center',
  },
  title: {
    textTransform: 'uppercase',
    marginBottom: normVert(40),
  },
  contentTitle: { marginBottom: normVert(19) },
  list: {
    marginBottom: normVert(21),
  },
});
