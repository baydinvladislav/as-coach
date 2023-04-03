import React from 'react';
import { Image, StyleSheet, TouchableOpacity, View } from 'react-native';

import { observer } from 'mobx-react';
import styled from 'styled-components';

import { AddIcon, BicepsImage, DefaultAvatarImage } from '@assets';
import { TOP_PADDING } from '@constants';
import { useStore } from '@hooks';
import { t } from '@i18n';
import { Screens, useNavigation } from '@navigation';
import { colors, normHor, normVert } from '@theme';
import { Button, Text } from '@ui';

import { ButtonType, FontSize, FontWeight } from '~types';

export const LkScreen = observer(() => {
  const { user } = useStore();

  const { navigate } = useNavigation();
  return (
    <View style={{ paddingTop: TOP_PADDING }}>
      <DateText>Четверг, 29 Дек</DateText>
      <Flex>
        <Flex>
          <WelcomeText>
            {t('lk.welcome', { name: user.me.username })}
          </WelcomeText>
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
    </View>
  );
});

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
