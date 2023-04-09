import React, { useEffect, useState } from 'react';
import { StyleSheet, View } from 'react-native';

import { TouchableOpacity } from 'react-native-gesture-handler';
import styled from 'styled-components';

import { ArrowLeftIcon } from '@assets';
import { LkEmpty } from '@components';
import { TOP_PADDING } from '@constants';
import { useStore } from '@hooks';
import { t } from '@i18n';
import { RoutesProps, Screens, useNavigation } from '@navigation';
import { CustomerProps } from '@store';
import { colors, normHor, normVert } from '@theme';
import { Badge, BadgeStatuses, Text } from '@ui';

import { FontSize } from '~types';

export const DetailClient = ({ route }: RoutesProps) => {
  const { navigate, goBack } = useNavigation();
  const [data, setData] = useState<Partial<CustomerProps>>({});
  const { customer } = useStore();

  const id = (route.params as { id: string })?.id;

  useEffect(() => {
    const data = customer.getCustomerById(id);
    setData(data);
  }, [customer, id]);

  return (
    <View style={{ flex: 1, paddingTop: TOP_PADDING }}>
      <Circle style={styles.back} onPress={() => goBack()}>
        <ArrowLeftIcon />
      </Circle>
      <Badge text={t('common.nonePlan')} status={BadgeStatuses.NONE} />
      <Text style={styles.title} color={colors.white} fontSize={FontSize.S24}>
        {data.first_name}
      </Text>
      <LkEmpty
        title={t('detailCustomer.herePlans')}
        description={t('detailCustomer.hereCanAdd')}
        onPress={() => navigate(Screens.NewPlanScreen)}
        buttonText={t('buttons.createPlan')}
      />
    </View>
  );
};

const styles = StyleSheet.create({
  title: {
    marginTop: normVert(10),
  },
  back: {
    marginBottom: normVert(24),
  },
});

const Circle = styled(TouchableOpacity)`
  border-radius: 100px;
  background-color: ${colors.grey};
  width: ${normHor(32)}px;
  height: ${normVert(32)}px;
  align-items: center;
  justify-content: center;
`;
