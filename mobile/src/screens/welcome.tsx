import React from 'react';
import { StyleSheet } from 'react-native';

import { t } from 'src/i18n';
import styled from 'styled-components';

import { LogoIcon } from '@assets';
import { Screens, useNavigation } from '@navigation';
import { normVert } from '@theme';
import { Button, Layout } from '@ui';

import { ButtonType } from '~types';

export const WelcomeScreen = () => {
  const { navigate } = useNavigation();

  return (
    <Layout style={styles.layout}>
      <Logo />
      <Button
        style={styles.button}
        type={ButtonType.PRIMARY}
        onPress={() => navigate(Screens.LoginScreen)}
      >
        {t('buttons.login')}
      </Button>
      <Button
        type={ButtonType.SECONDARY}
        onPress={() => navigate(Screens.RegistrationScreen)}
      >
        {t('auth.registration')}
      </Button>
    </Layout>
  );
};

const styles = StyleSheet.create({
  layout: { flex: 1, justifyContent: 'flex-end' },
  button: {
    marginBottom: normVert(20),
  },
});

const Logo = styled(LogoIcon)`
  margin-left: auto;
  margin-right: auto;
  margin-bottom: ${normVert(40)}px;
`;
