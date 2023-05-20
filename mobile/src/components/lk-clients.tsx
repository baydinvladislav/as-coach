import React, { useCallback, useEffect, useState } from 'react';
import { FlatList, ListRenderItemInfo, StyleSheet, View } from 'react-native';

import { debounce } from 'lodash';
import styled from 'styled-components';

import { AddIcon } from '@assets';
import { ClientCard, LkEmpty, NotFound, SearchInput } from '@components';
import { useStore } from '@hooks';
import { t } from '@i18n';
import { Screens, useNavigation } from '@navigation';
import { CustomerProps } from '@store';
import { colors, normVert } from '@theme';
import { Button, Text } from '@ui';

import { ButtonType, FontSize } from '~types';

type TProps = {
  searchInputKey?: number;
  setSearchInputKey: React.Dispatch<React.SetStateAction<number>>;
};

export const LkClients = ({ searchInputKey, setSearchInputKey }: TProps) => {
  const [searchValue, setSearchValue] = useState<string | undefined>();

  const { customer, loading } = useStore();

  const { navigate } = useNavigation();

  useEffect(() => {
    customer.getCustomers();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

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

  const handleNavigateDetailClient = (id: string) => {
    setSearchInputKey(key => key + 1);
    loading.increaseLoadingStatus();
    navigate(Screens.DetailClient, {
      id,
      from: Screens.LkScreen,
    });
  };

  const handleNavigateAddClientScreen = () => {
    setSearchInputKey(key => key + 1);
    navigate(Screens.AddClientScreen);
  };

  const renderItem = (customer: ListRenderItemInfo<CustomerProps>) => (
    <ClientCard
      key={customer.item.id}
      firstName={customer.item.first_name}
      lastName={customer.item.last_name}
      onPress={() => handleNavigateDetailClient(customer.item.id)}
    />
  );

  return customers.length ? (
    <>
      <TopContainer>
        <Text fontSize={FontSize.S20} color={colors.white}>
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
};

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
