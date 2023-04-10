import React, { useEffect } from 'react';
import { Image, TouchableOpacity, View } from 'react-native';

import { observer } from 'mobx-react';
import moment from 'moment';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import styled from 'styled-components';

import { BackgroundImage, BicepsImage, DefaultAvatarImage } from '@assets';
import { LkEmpty } from '@components';
import { TOP_PADDING } from '@constants';
import { useStore } from '@hooks';
import { t } from '@i18n';
import { Screens, useNavigation } from '@navigation';
import { colors, normHor, normVert } from '@theme';
import { Text } from '@ui';
import { windowHeight, windowWidth } from '@utils';

import { FontSize, FontWeight } from '~types';

moment.locale('ru');

export const LkScreen = observer(() => {
  const { user, customer } = useStore();
  const { top } = useSafeAreaInsets();

  const { navigate } = useNavigation();

  useEffect(() => {
    customer.getCustomers();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const customers = customer.customers;

  return (
    <LkBackground
      style={{
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
        customers.map(customer => (
          <TouchableOpacity // TODO: Заместо всего блока TouchableOpacity должны быть стилизованые плашки с клиентом типа <ClientCard key={} firstName={} lastName={} onPress={} /> (нужно создать компонент src/components/client-card.tsx)
            onPress={() => navigate(Screens.DetailClient, { id: customer.id })}
            key={customer.id}
          >
            <Text color={colors.white} fontSize={FontSize.S24}>
              {customer.first_name}
            </Text>
          </TouchableOpacity>
        ))
      ) : (
        <LkEmpty
          title={t('lk.hereClients')}
          description={t('lk.hereCanAdd')}
          onPress={() => navigate(Screens.AddClientScreen)}
          buttonText={t('buttons.addClient')}
        />
      )}
    </LkBackground>
  );
});

const LkBackground = styled(View)`
  padding-horizontal: ${normVert(16)}px;
`;

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
