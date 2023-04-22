import React, { useCallback, useEffect, useState } from 'react';
import {
  FlatList,
  Image,
  ListRenderItemInfo,
  StyleSheet,
  TouchableOpacity,
  View,
} from 'react-native';

import { debounce } from 'lodash';
import { observer } from 'mobx-react';
import moment from 'moment';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import styled from 'styled-components';

import {
  AddIcon,
  BackgroundImage,
  BicepsImage,
  DefaultAvatarImage,
} from '@assets';
import { ClientCard, LkEmpty, NotFound, SearchInput } from '@components';
import { TOP_PADDING } from '@constants';
import { useStore } from '@hooks';
import { t } from '@i18n';
import { Screens, useNavigation } from '@navigation';
import { CustomerProps } from '@store';
import { colors, normHor, normVert } from '@theme';
import { Button, Text } from '@ui';
import { windowHeight, windowWidth } from '@utils';

import { ButtonType, FontSize, FontWeight } from '~types';

moment.locale('ru');

export const LkScreen = observer(() => {
  const [searchValue, setSearchValue] = useState<string | undefined>();

  const { user, customer } = useStore();
  const { top } = useSafeAreaInsets();

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

  const renderItem = (customer: ListRenderItemInfo<CustomerProps>) => (
    <ClientCard
      key={customer.item.id}
      firstName={customer.item.first_name}
      lastName={customer.item.last_name}
      onPress={() => navigate(Screens.DetailClient, { id: customer.item.id })}
    />
  );

  return (
    <View
      style={{
        flex: 1,
        paddingHorizontal: normHor(16),
        paddingTop: TOP_PADDING + top,
      }}
    >
      <BackgroundColor />
      <Background
        blurRadius={10}
        source={BackgroundImage}
        style={{ opacity: 0.3 }}
      />

      <DateText>{moment().format('dddd, D MMM')}</DateText>
      <Flex>
        <Flex>
          <Text color={colors.white} fontSize={FontSize.S24}>
            {t('lk.welcome', { name: user.me.first_name })}
          </Text>
          <Biceps source={BicepsImage} />
        </Flex>
        <TouchableOpacity onPress={() => navigate(Screens.ProfileScreen)}>
          <Avatar source={DefaultAvatarImage} />
        </TouchableOpacity>
      </Flex>

      {customers.length ? (
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
            <SearchInput value={searchValue} onChangeText={setSearchValue} />
          </View>
          {searchCustomers.length ? (
            <FlatList
              data={searchCustomers}
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
          onPress={() => navigate(Screens.AddClientScreen)}
          buttonText={t('buttons.addClient')}
        />
      )}
    </View>
  );
});

const styles = StyleSheet.create({
  searchInput: {
    marginBottom: normVert(20),
  },
});

const Avatar = styled(Image)`
  width: ${normHor(44)}px;
  height: ${normVert(44)}px;
  border-radius: 100px;
`;

const Biceps = styled(Image)`
  width: ${normHor(26)}px;
  height: ${normVert(26)}px;
  margin-left: 6px;
`;

const Flex = styled(View)`
  flex-direction: row;
  justify-content: space-between;
  align-items: center;
`;

const DateText = styled(Text)`
  text-transform: uppercase;
  color: ${colors.black4};
  font-size: ${FontSize.S10};
  margin-bottom: ${normVert(16)}px;
  font-family: ${FontWeight.Bold};
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
