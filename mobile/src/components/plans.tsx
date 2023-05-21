import React, { useState } from 'react';
import { FlatList, ListRenderItemInfo, View } from 'react-native';

import styled from 'styled-components';

import { AddIcon } from '@assets';
import { LkEmpty, PlanCard } from '@components';
import { useStore } from '@hooks';
import { t } from '@i18n';
import { Screens, useNavigation } from '@navigation';
import { CustomerProps } from '@store';
import { colors, normVert } from '@theme';
import { Button, Text } from '@ui';

import { ButtonType, FontSize, TPlanType, UserType } from '~types';

type TProps = {
  data: Partial<CustomerProps>;
  setPreviousScreen?: React.Dispatch<React.SetStateAction<Screens>>;
  title: string;
  description: string;
  withAddButton?: boolean;
};

export const Plans = ({
  data,
  setPreviousScreen,
  title,
  description,
  withAddButton = true,
}: TProps) => {
  const { navigate } = useNavigation();
  const { user } = useStore();

  const plans = data?.plans;

  const isCouch = user.me.user_type === UserType.COACH;

  const renderItem = (plan: ListRenderItemInfo<TPlanType>) => (
    <PlanCard
      plan={plan.item}
      onPress={() => handleNavigateDetailPlan(plan.item.id)}
      withMenu={isCouch}
    />
  );

  const handleNavigatePlan = () => {
    setPreviousScreen?.(Screens.PlanScreen);
    navigate(Screens.PlanScreen, data);
  };

  const handleNavigateDetailPlan = (id: string) => {
    setPreviousScreen?.(Screens.DetailPlanScreen);
    navigate(Screens.DetailPlanScreen, { id: data.id, planId: id });
  };

  return plans?.length ? (
    <>
      <TopContainer>
        <Text fontSize={FontSize.S20} color={colors.white}>
          {t('detailCustomer.plans')}
        </Text>
        {isCouch && (
          <Button
            type={ButtonType.TEXT}
            onPress={handleNavigatePlan}
            leftIcon={<AddIcon fill={colors.green} />}
          >
            {t('buttons.createPlan')}
          </Button>
        )}
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
      title={title}
      description={description}
      onPress={handleNavigatePlan}
      buttonText={withAddButton ? t('buttons.createPlan') : undefined}
    />
  );
};

const TopContainer = styled(View)`
  margin-top: ${normVert(24)}px;
  margin-bottom: ${normVert(16)}px;
  padding-vertical: ${normVert(10)}px;
  flex-direction: row;
  align-items: center;
  justify-content: space-between;
`;
