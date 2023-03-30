import React from 'react';
import { Image, StyleSheet, TouchableOpacity } from 'react-native';

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
import { t } from '@i18n';
import { Screens, useNavigation } from '@navigation';
import { colors, normHor, normVert } from '@theme';
import { Layout, Switch, Text } from '@ui';

import { FontSize } from '~types';

const DATA = (onClick1: () => void, onClick2: () => void) => [
  {
    id: 1,
    name: t('profile.nav1'),
    icon: <UserEditIcon stroke={colors.green} />,
    rightIcon: <ArrowRightIcon />,
    onPress: onClick1,
  },
  {
    id: 2,
    name: t('profile.nav2'),
    icon: <LockIcon stroke={colors.green} />,
    rightIcon: <ArrowRightIcon />,
    onPress: onClick2,
  },
  {
    id: 3,
    name: t('profile.nav3'),
    icon: <NotificationIcon stroke={colors.green} />,
    rightIcon: <Switch />,
    onPress: () => console.log(123),
  },
  {
    id: 4,
    color: colors.red,
    name: t('profile.nav4'),
    icon: <LogoutIcon stroke={colors.red} />,
    onPress: () => console.log(123),
  },
];

export const ProfileScreen = () => {
  const { navigate } = useNavigation();

  const handleGoEdit = () => {
    navigate(Screens.ProfileEditScreen);
  };

  const handleGoChangePassword = () => {
    navigate(Screens.ChangePasswordScreen);
  };

  return (
    <Layout backgroundBlurRadius={10} backgroundOpacity={0.3}>
      <BackButton onPress={() => navigate(Screens.LkScreen)}>
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
        {'Александр'}
      </Text>
      {DATA(handleGoEdit, handleGoChangePassword).map((item, key) => (
        <ProfileListItem
          index={key}
          color={item.color}
          icon={item.icon}
          name={item.name}
          key={item.id}
          rightIcon={item.rightIcon}
          handlePress={item.onPress}
        />
      ))}
    </Layout>
  );
};

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
