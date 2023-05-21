import React, { useCallback, useState } from 'react';
import { Image, TouchableOpacity, View } from 'react-native';

import { observer } from 'mobx-react';
import moment from 'moment';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import styled from 'styled-components';

import { BackgroundImage, BicepsImage, DefaultAvatarImage } from '@assets';
import { LkClients, Plans } from '@components';
import { TOP_PADDING } from '@constants';
import { useStore } from '@hooks';
import { t } from '@i18n';
import { Screens, useNavigation } from '@navigation';
import { useFocusEffect } from '@react-navigation/native';
import { CustomerProps } from '@store';
import { colors, normHor, normVert } from '@theme';
import { Text } from '@ui';
import { windowHeight, windowWidth } from '@utils';

import { FontSize, FontWeight, UserType } from '~types';

moment.locale('ru');

export const LkScreen = observer(() => {
  const [searchInputKey, setSearchInputKey] = useState(0);

  const { user, customer } = useStore();
  const { top } = useSafeAreaInsets();

  const isCouch = user.me.user_type === UserType.COACH;

  const { navigate } = useNavigation();

  const [data, setData] = useState<Partial<CustomerProps>>({});
  useFocusEffect(
    useCallback(() => {
      if (isCouch) return;
      customer.getCustomerPlanById(user.me.id).then(plans => {
        setData({ ...data, plans });
      });
      // eslint-disable-next-line react-hooks/exhaustive-deps
    }, []),
  );

  const handleNavigateProfileScreen = () => {
    setSearchInputKey(key => key + 1);
    navigate(Screens.ProfileScreen);
  };

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
        <TouchableOpacity onPress={handleNavigateProfileScreen}>
          <Avatar source={DefaultAvatarImage} />
        </TouchableOpacity>
      </Flex>

      {isCouch ? (
        <LkClients
          setSearchInputKey={setSearchInputKey}
          searchInputKey={searchInputKey}
        />
      ) : (
        <Plans
          data={data}
          title={t('lk.herePlans')}
          description={t('lk.hereAddPlans')}
          withAddButton={false}
        />
      )}
    </View>
  );
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
