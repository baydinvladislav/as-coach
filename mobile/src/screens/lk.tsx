import React from 'react';
import { Image, StyleSheet, TouchableOpacity, View } from 'react-native';

import styled from 'styled-components';

import { AddIcon, BicepsImage, DefaultAvatarImage } from '@assets';
import { t } from '@i18n';
import { Screens, useNavigation } from '@navigation';
import { colors, normHor, normVert } from '@theme';
import { Button, Layout, Text } from '@ui';

import { ButtonType, FontSize, FontWeight } from '~types';

export const LkScreen = () => {
  const { navigate } = useNavigation();
  return (
    <Layout backgroundBlurRadius={10} backgroundOpacity={0.3}>
      <DateText>Четверг, 29 Дек</DateText>
      <Flex>
        <Flex>
          <WelcomeText>{t('lk.welcome', { name: 'Александр' })}</WelcomeText>
          <Biceps source={BicepsImage} />
        </Flex>
        <TouchableOpacity onPress={() => navigate(Screens.ProfileScreen)}>
          <Avatar source={DefaultAvatarImage} />
        </TouchableOpacity>
      </Flex>

      <View style={styles.text}>
        <Text
          align="center"
          style={{ lineHeight: 24, marginBottom: normVert(16) }}
          fontSize={FontSize.S24}
          color={colors.black5}
        >
          {t('lk.hereClients')}
        </Text>
        <Text
          align="center"
          style={{ lineHeight: 24 }}
          fontSize={FontSize.S17}
          color={colors.black4}
        >
          {t('lk.hereCanAdd')}
        </Text>
      </View>

      <Button
        type={ButtonType.TEXT}
        onPress={() => null}
        leftIcon={<AddIcon stroke={colors.green} />}
      >
        {t('buttons.addClient')}
      </Button>
    </Layout>
  );
};

const styles = StyleSheet.create({
  text: { marginTop: normVert(213), marginBottom: normVert(24) },
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

const WelcomeText = styled(Text)`
  color: ${colors.white};
  font-size: ${FontSize.S24};
`;
