import React from 'react';
import { Image, StyleSheet, TouchableOpacity, View } from 'react-native';

import { observer } from 'mobx-react';
import styled from 'styled-components';

import {
  ArrowLeftIcon,
  ArrowRightIcon,
  DefaultAvatarImage,
  LockIcon,
  LogoutIcon,
  NotificationIcon,
  UserEditIcon,
} from '@assets';
import { ProfileListItem } from '@components';
import { TOP_PADDING } from '@constants';
import { useStore } from '@hooks';
import { t } from '@i18n';
import { Screens, useNavigation } from '@navigation';
import { colors, normHor, normVert } from '@theme';
import { Switch, Text } from '@ui';

import { FontSize } from '~types';

const DATA = (
  onPress1: () => void,
  onPress2: () => void,
  onPress3: () => void,
  onPress4: () => void,
) => [
  {
    id: 1,
    name: t('profile.nav1'),
    icon: <UserEditIcon stroke={colors.green} />,
    rightIcon: <ArrowRightIcon />,
    onPress: onPress1,
  },
  {
    id: 2,
    name: t('profile.nav2'),
    icon: <LockIcon stroke={colors.green} />,
    rightIcon: <ArrowRightIcon />,
    onPress: onPress2,
  },
  {
    id: 3,
    name: t('profile.nav3'),
    icon: <NotificationIcon stroke={colors.green} />,
    rightIcon: <Switch />,
    onPress: onPress3,
  },
  {
    id: 4,
    color: colors.red,
    name: t('profile.nav4'),
    icon: <LogoutIcon stroke={colors.red} />,
    onPress: onPress4,
  },
];

export const ProfileScreen = observer(() => {
  const { user, customer } = useStore();

  const { navigate } = useNavigation();

  const handleGoEdit = () => {
    navigate(Screens.ProfileEditScreen);
  };

  const handleGoChangePassword = () => {
    navigate(Screens.ChangePasswordScreen);
  };

  const handleLogout = () => {
    customer.setInitialCustomers();
    user.logout().then(() => navigate(Screens.WelcomeScreen));
  };

  return (
    <View style={{ paddingTop: TOP_PADDING }}>
      <BackButton
        style={{ width: normHor(20) }}
        onPress={() => navigate(Screens.LkScreen)}
      >
        <ArrowLeftIcon />
      </BackButton>
      <Text align="center" fontSize={FontSize.S17} color={colors.white}>
        {t('profile.profileTitle')}
      </Text>
      <Avatar source={DefaultAvatarImage} />
      <Text
        style={styles.text}
        align="center"
        fontSize={FontSize.S24}
        color={colors.white}
      >
        {user.me.first_name}
      </Text>
      {DATA(handleGoEdit, handleGoChangePassword, () => null, handleLogout).map(
        (item, key) => (
          <ProfileListItem
            index={key}
            color={item.color}
            icon={item.icon}
            name={item.name}
            key={item.id}
            rightIcon={item.rightIcon}
            handlePress={item.onPress}
          />
        ),
      )}
    </View>
  );
});

const styles = StyleSheet.create({
  text: { marginBottom: normVert(62) },
});

const BackButton = styled(TouchableOpacity)`
  margin-bottom: ${normVert(24)}px;
`;

const Avatar = styled(Image)`
  width: ${normHor(113.5)}px;
  height: ${normVert(113.5)}px;
  border-radius: 100px;
  margin-left: auto;
  margin-right: auto;
  margin-vertical: ${normVert(32)}px;
`;
