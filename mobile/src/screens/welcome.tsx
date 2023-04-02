import React from 'react';
import { StyleSheet, View } from 'react-native';

import styled from 'styled-components';

import { LogoIcon } from '@assets';
import { t } from '@i18n';
import { Screens, useNavigation } from '@navigation';
import { normVert } from '@theme';
import { Button } from '@ui';

import { ButtonType } from '~types';

export const WelcomeScreen = () => {
  const { navigate } = useNavigation();

  return (
    <View style={{ flex: 1, justifyContent: 'flex-end' }}>
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
        {t('buttons.registration')}
      </Button>
    </View>
  );
};

const styles = StyleSheet.create({
  button: {
    marginBottom: normVert(20),
  },
});

const Logo = styled(LogoIcon)`
  margin-left: auto;
  margin-right: auto;
  margin-bottom: ${normVert(40)}px;
`;
