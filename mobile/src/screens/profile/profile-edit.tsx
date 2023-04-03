import React from 'react';
import { Image, StyleSheet } from 'react-native';

import styled from 'styled-components';

import { DefaultAvatarImage } from '@assets';
import { t } from '@i18n';
import { Screens, useNavigation } from '@navigation';
import { colors, normHor, normVert } from '@theme';
import { Input, Keyboard, Text, ViewWithButtons } from '@ui';

import { FontSize } from '~types';

export const ProfileEditScreen = () => {
  const { navigate } = useNavigation();
  return (
    <Keyboard>
      <ViewWithButtons
        onCancel={() => navigate(Screens.ProfileScreen)}
        onConfirm={() => navigate(Screens.ProfileScreen)}
        style={{ paddingTop: normVert(80) }}
      >
        <Text align="center" fontSize={FontSize.S17} color={colors.white}>
          {t('edit.editTitle')}
        </Text>
        <Avatar source={DefaultAvatarImage} />
        <Input
          error={'Некорректный номер телефона'}
          style={styles.input}
          placeholder={t('inputs.firstName')}
        />
        <Input style={styles.input} placeholder={t('inputs.lastName')} />
        <Input style={styles.input} placeholder={t('inputs.sex')} />
        <Input style={styles.input} placeholder={t('inputs.birthday')} />
        <Input style={styles.input} placeholder={t('inputs.email')} />
        <Input placeholder={t('inputs.phone')} />
      </ViewWithButtons>
    </Keyboard>
  );
};

const styles = StyleSheet.create({
  text: { marginBottom: normVert(62) },
  input: {
    marginBottom: normVert(20),
  },
});

const Avatar = styled(Image)`
  width: ${normHor(92)}px;
  height: ${normVert(92)}px;
  border-radius: 100px;
  margin-left: auto;
  margin-right: auto;
  margin-vertical: ${normVert(32)}px;
`;
