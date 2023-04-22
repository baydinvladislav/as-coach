import React, { useEffect, useState } from 'react';
import {
  FlatList,
  Image,
  ListRenderItemInfo,
  StyleSheet,
  View,
} from 'react-native';

import { TouchableOpacity } from 'react-native-gesture-handler';
import styled from 'styled-components';

import { getCustomerPlan } from '@api';
import { AddIcon, ArrowLeftIcon, BackgroundImage } from '@assets';
import { LkEmpty, PlanCard } from '@components';
import { TOP_PADDING } from '@constants';
import { useStore } from '@hooks';
import { t } from '@i18n';
import { RoutesProps, Screens, useNavigation } from '@navigation';
import { CustomerProps } from '@store';
import { colors, normHor, normVert } from '@theme';
import { Badge, BadgeStatuses, Button, Text } from '@ui';
import { windowHeight, windowWidth } from '@utils';

import { ButtonType, FontSize, TPlanType } from '~types';

export const DetailClient = ({ route }: RoutesProps) => {
  const { navigate, goBack } = useNavigation();
  const [data, setData] = useState<Partial<CustomerProps>>({});
  const { customer } = useStore();

  const id = (route.params as { id: string })?.id;

  useEffect(() => {
    const client = customer.getCustomerById(id);
    customer.getCustomerPlanById(client).then(plans => {
      setData({ ...data, plans });
    });
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [customer, id]);

  const renderItem = (plan: ListRenderItemInfo<TPlanType>) => (
    <PlanCard plan={plan.item} />
  );

  return (
    <View
      style={{
        flex: 1,
        paddingHorizontal: normHor(16),
        paddingTop: TOP_PADDING,
      }}
    >
      <BackgroundColor />
      <Background
        blurRadius={10}
        source={BackgroundImage}
        style={{ opacity: 0.3 }}
      />

      <Circle style={styles.back} onPress={goBack}>
        <ArrowLeftIcon />
      </Circle>
      <Badge text={t('common.nonePlan')} status={BadgeStatuses.NONE} />
      <Text style={styles.title} color={colors.white} fontSize={FontSize.S24}>
        {data.first_name}
      </Text>
      {data.plans?.length ? (
        <>
          <TopContainer>
            <Text fontSize={FontSize.S20} color={colors.white}>
              {t('detailCustomer.plans')}
            </Text>
            <Button
              type={ButtonType.TEXT}
              onPress={() => navigate(Screens.PlanScreen, data)}
              leftIcon={<AddIcon fill={colors.green} />}
            >
              {t('buttons.createPlan')}
            </Button>
          </TopContainer>

          <FlatList
            nestedScrollEnabled={true}
            data={data.plans}
            renderItem={renderItem}
            keyExtractor={item => item.id}
          />
        </>
      ) : (
        <LkEmpty
          title={t('detailCustomer.herePlans')}
          description={t('detailCustomer.hereCanAdd')}
          onPress={() => navigate(Screens.PlanScreen, data)}
          buttonText={t('buttons.createPlan')}
        />
      )}
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

const Background = styled(Image)`
  position: absolute;
  width: ${windowWidth}px;
  height: ${windowHeight}px;
`;

const BackgroundColor = styled(View)`
  position: absolute;
  width: ${windowWidth}px;
  height: ${windowHeight}px;
  background-color: ${colors.black};
`;

const TopContainer = styled(View)`
  margin-top: ${normVert(24)}px;
  margin-bottom: ${normVert(16)}px;
  padding-vertical: ${normVert(10)}px;
  flex-direction: row;
  align-items: center;
  justify-content: space-between;
`;
