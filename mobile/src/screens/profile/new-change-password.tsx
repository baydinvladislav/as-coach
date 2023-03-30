import React from 'react';
import { StyleSheet, View } from 'react-native';

import styled from 'styled-components';

import { LogoIcon } from '@assets';
import { PasswordInput } from '@components';
import { t } from '@i18n';
import { Screens, useNavigation } from '@navigation';
import { colors, normVert } from '@theme';
import { Button, Input, Layout, Text } from '@ui';

import { ButtonType, FontSize } from '~types';

export const NewChangePasswordScreen = () => {
  const { navigate } = useNavigation();

  return (
    <Layout backgroundBlurRadius={10} backgroundOpacity={0.3}>
      <Logo />
      <Text
        style={styles.title}
        align="center"
        fontSize={FontSize.S24}
        color={colors.white}
      >
        {t('changePassword.changeNewPasswordTitle')}
      </Text>
      <Text
        align="center"
        style={{ lineHeight: 22 }}
        fontSize={FontSize.S17}
        color={colors.black4}
      >
        {t('changePassword.changePasswordDescription')}
      </Text>
      <InputsContainer>
        <PasswordInput
          style={styles.input}
          placeholder={t('inputs.password')}
        />
        <PasswordInput
          style={styles.input}
          placeholder={t('inputs.newPassword')}
        />
      </InputsContainer>
      <Button
        style={styles.button}
        type={ButtonType.PRIMARY}
        onPress={() => navigate(Screens.ProfileScreen)}
      >
        {t('buttons.save')}
      </Button>
      <Button
        style={styles.button2}
        type={ButtonType.TEXT}
        onPress={() => navigate(Screens.ProfileScreen)}
      >
        {t('buttons.cancel')}
      </Button>
    </Layout>
  );
};

const styles = StyleSheet.create({
  title: {
    marginBottom: normVert(16),
  },
  button: {
    marginBottom: normVert(20),
  },
  button2: {
    marginLeft: 5,
  },
  input: {
    marginBottom: normVert(20),
  },
});

const InputsContainer = styled(View)`
  margin-top: ${normVert(32)}px;
  flex: 1;
`;

const Logo = styled(LogoIcon)`
  margin-left: auto;
  margin-right: auto;
  margin-bottom: ${normVert(119)}px;
`;
