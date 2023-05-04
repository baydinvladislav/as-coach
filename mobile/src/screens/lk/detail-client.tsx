import React, { useCallback, useState } from 'react';
import {
  FlatList,
  Image,
  ListRenderItemInfo,
  StyleSheet,
  View,
} from 'react-native';

import { TouchableOpacity } from 'react-native-gesture-handler';
import styled from 'styled-components';

import { AddIcon, ArrowLeftIcon, BackgroundImage } from '@assets';
import { LkEmpty, PlanCard } from '@components';
import { TOP_PADDING } from '@constants';
import { useStore } from '@hooks';
import { t } from '@i18n';
import { RoutesProps, Screens, useNavigation } from '@navigation';
import { useFocusEffect } from '@react-navigation/native';
import { CustomerProps } from '@store';
import { colors, normHor, normVert } from '@theme';
import { Badge, BadgeStatuses, Button, Text } from '@ui';
import { windowHeight, windowWidth } from '@utils';

import { ButtonType, FontSize, TPlanType } from '~types';

export const DetailClient = ({ route }: RoutesProps) => {
  const [previousScreen, setPreviousScreen] = useState(
    (route.params as { from: Screens })?.from,
  );
  const { navigate, goBack } = useNavigation();
  const [data, setData] = useState<Partial<CustomerProps>>({});
  const { customer, loading } = useStore();

  const id = (route.params as { id: string })?.id;

  useFocusEffect(
    useCallback(() => {
      loading.decreaseLoadingStatus();
      const client = customer.getCustomerById(id);
      customer.getCustomerPlanById(id).then(plans => {
        setData({ ...data, ...client, plans });
      });
      // eslint-disable-next-line react-hooks/exhaustive-deps
    }, []),
  );

  const renderItem = (plan: ListRenderItemInfo<TPlanType>) => (
    <PlanCard
      plan={plan.item}
      onPress={() => handleNavigateDetailPlan(plan.item.id)}
    />
  );

  const handleNavigatePlan = () => {
    setPreviousScreen(Screens.PlanScreen);
    navigate(Screens.PlanScreen, data);
  };

  const handleNavigateDetailPlan = (id: string) => {
    setPreviousScreen(Screens.DetailPlanScreen);
    navigate(Screens.DetailPlanScreen, { id: data.id, planId: id });
  };

  return (
    <View
      style={{
        flex: 1,
        paddingHorizontal: normHor(16),
        paddingTop: TOP_PADDING,
      }}
    >
      {previousScreen !== Screens.LkScreen && (
        <>
          <BackgroundColor />
          <Background
            blurRadius={10}
            source={BackgroundImage}
            style={{ opacity: 0.3 }}
          />
        </>
      )}

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
              onPress={handleNavigatePlan}
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
          onPress={handleNavigatePlan}
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
