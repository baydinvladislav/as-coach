import React from 'react';
import { StyleSheet, View } from 'react-native';

import styled from 'styled-components';

import { LogoIcon } from '@assets';
import { PasswordInput } from '@components';
import { t } from '@i18n';
import { Screens, useNavigation } from '@navigation';
import { colors, normVert } from '@theme';
import { Button, Text } from '@ui';

import { ButtonType, FontSize } from '~types';

export const ChangePasswordScreen = () => {
  const { navigate } = useNavigation();

  return (
    <>
      <Logo />
      <Text
        style={styles.title}
        align="center"
        fontSize={FontSize.S24}
        color={colors.white}
      >
        {t('changePassword.changePasswordTitle')}
      </Text>
      <InputsContainer>
        <PasswordInput
          style={styles.input}
          placeholder={t('inputs.password')}
        />
      </InputsContainer>
      <Button
        style={styles.button}
        type={ButtonType.PRIMARY}
        onPress={() => navigate(Screens.NewChangePasswordScreen)}
      >
        {t('buttons.continue')}
      </Button>
      <Button
        style={styles.button2}
        type={ButtonType.TEXT}
        onPress={() =>
          navigate(Screens.SmsScreen, { from: Screens.ChangePasswordScreen })
        }
      >
        {t('buttons.forgotPassword')}
      </Button>
    </>
  );
};

const styles = StyleSheet.create({
  title: {
    marginBottom: normVert(32),
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
  flex: 1;
`;

const Logo = styled(LogoIcon)`
  margin-left: auto;
  margin-right: auto;
  margin-bottom: ${normVert(119)}px;
`;
