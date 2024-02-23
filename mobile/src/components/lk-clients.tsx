import React, { useCallback, useEffect, useState } from 'react';
import { FlatList, ListRenderItemInfo, StyleSheet, View } from 'react-native';

import { debounce } from 'lodash';
import { observer } from 'mobx-react';
import moment from 'moment';
import styled from 'styled-components';

import { AddIcon } from '@assets';
import { ClientCard, LkEmpty, NotFound, SearchInput } from '@components';
import { useStore } from '@hooks';
import { t } from '@i18n';
import { Screens, useNavigation } from '@navigation';
import { useFocusEffect } from '@react-navigation/native';
import { CustomerProps } from '@store';
import { colors, normVert } from '@theme';
import { BadgeStatuses, Button, Text } from '@ui';
import { getCustomerStatusAndText } from '@utils';

import { ButtonType, FontSize, FontWeight } from '~types';

export const LkClients = observer(() => {
  const [searchInputKey, setSearchInputKey] = useState(0);
  const [searchValue, setSearchValue] = useState<string | undefined>();
  const [isFetching, setIsFetching] = useState(false);
  const { customer, loading } = useStore();

  const clearSearch = () => {
    setSearchInputKey(key => key + 1);
    setSearchValue(undefined);
    customer.setSearchCustomer([]);
  };

  const { navigate } = useNavigation();

  useEffect(() => {
    customer.getCustomers();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  // eslint-disable-next-line react-hooks/exhaustive-deps
  useFocusEffect(useCallback(() => () => clearSearch(), []));

  // eslint-disable-next-line react-hooks/exhaustive-deps
  const search = useCallback(
    debounce(() => {
      customer.searchCustomerByName(searchValue);
    }, 200),
    [searchValue],
  );

  useEffect(() => {
    search();
  }, [customer, search, searchValue]);

  const customers = customer.customers;
  const searchCustomers = customer.searchCustomers;

  const handleRefresh = () => {
    setIsFetching(true);
    customer.getCustomers();
    setIsFetching(false);
  };

  const handleNavigateDetailClient = (
    id: string,
    text: string,
    status: BadgeStatuses,
  ) => {
    clearSearch();
    loading.increaseLoadingStatus();
    navigate(Screens.DetailClient, {
      id,
      status,
      text,
      from: Screens.LkScreen,
    });
  };

  const handleNavigateAddClientScreen = () => {
    clearSearch();
    navigate(Screens.AddClientScreen);
  };

  const renderItem = (customer: ListRenderItemInfo<CustomerProps>) => {
    const { status, text } = getCustomerStatusAndText(customer.item.last_plan_end_date);

    return (
      <ClientCard
        key={customer.item.id}
        firstName={customer.item.first_name}
        lastName={customer.item.last_name}
        text={text}
        status={status}
        onPress={() =>
          handleNavigateDetailClient(customer.item.id, text, status)
        }
      />
    );
  };

  return customers.length ? (
    <>
      <TopContainer>
        <Text
          fontSize={FontSize.S20}
          color={colors.white}
          weight={FontWeight.Bold}
        >
          {t('lk.clients')}
        </Text>
        <Button
          type={ButtonType.TEXT}
          onPress={() => navigate(Screens.AddClientScreen)}
          leftIcon={<AddIcon fill={colors.green} />}
        >
          {t('buttons.addClient')}
        </Button>
      </TopContainer>
      <View style={styles.searchInput}>
        <SearchInput
          key={searchInputKey}
          value={searchValue}
          onChangeText={setSearchValue}
        />
      </View>
      {(searchValue && searchCustomers.length) || !searchValue ? (
        <FlatList
          data={
            !searchValue && !searchCustomers.length
              ? customers
              : searchCustomers
          }
          renderItem={renderItem}
          keyExtractor={item => item.id}
          refreshing={isFetching}
          onRefresh={handleRefresh}
          bounces={!isFetching}
        />
      ) : (
        <NotFound />
      )}
    </>
  ) : (
    <LkEmpty
      title={t('lk.hereClients')}
      description={t('lk.hereCanAdd')}
      onPress={handleNavigateAddClientScreen}
      buttonText={t('buttons.addClient')}
    />
  );
});

const styles = StyleSheet.create({
  searchInput: {
    marginBottom: normVert(20),
  },
});

const TopContainer = styled(View)`
  margin-top: ${normVert(24)}px;
  margin-bottom: ${normVert(16)}px;
  padding-vertical: ${normVert(10)}px;
  flex-direction: row;
  align-items: center;
  justify-content: space-between;
`;
