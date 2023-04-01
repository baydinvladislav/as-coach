import React, { useEffect } from 'react';
import { StyleSheet, View } from 'react-native';

import { Formik } from 'formik';
import { observer } from 'mobx-react';
import styled from 'styled-components';

import { LogoIcon } from '@assets';
import { PasswordInput } from '@components';
import { PHONE_MASK } from '@constants';
import { useStore } from '@hooks';
import { t } from '@i18n';
import { Screens, useNavigation } from '@navigation';
import { colors, normVert } from '@theme';
import { Button, Input, Layout, Text } from '@ui';

import { ButtonType, FontSize } from '~types';

export const LoginScreen = observer(() => {
  const { navigate } = useNavigation();

  const { user, loading } = useStore();
  const idDisabled = loading.isLoading;

  const handleLogin = (value: { phone: string; password: string }) => {
    user
      .login({
        phone: '+' + value.phone.replace(/[^0-9]/g, ''),
        password: value.password,
      })
      .then(data => navigate(Screens.LkScreen));
  };

  return (
    <Layout backgroundBlurRadius={10} backgroundOpacity={0.3}>
      <Logo />
      <Text
        style={styles.title}
        align="center"
        fontSize={FontSize.S24}
        color={colors.white}
      >
        {t('auth.loginTitle')}
      </Text>
      <Formik
        initialValues={{ phone: '', password: '' }}
        onSubmit={handleLogin}
      >
        {({ handleChange, handleSubmit, values }) => (
          <>
            <InputsContainer>
              <Input
                mask={PHONE_MASK}
                style={styles.input}
                placeholder={t('inputs.phone')}
                value={values.phone}
                onChangeText={handleChange('phone')}
              />
              <PasswordInput
                value={values.password}
                placeholder={t('inputs.password')}
                onChangeText={handleChange('password')}
              />
            </InputsContainer>
            <Button
              style={styles.button}
              type={ButtonType.PRIMARY}
              onPress={() => handleSubmit()}
              isDisabled={idDisabled}
            >
              {t('buttons.login')}
            </Button>
            <Flex>
              <Text fontSize={FontSize.S17} color={colors.white}>
                {t('auth.noAccount')}
              </Text>
              <Button
                style={styles.button2}
                type={ButtonType.TEXT}
                onPress={() => navigate(Screens.RegistrationScreen)}
              >
                {t('buttons.registration')}
              </Button>
            </Flex>
          </>
        )}
      </Formik>
    </Layout>
  );
});

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

const Flex = styled(View)`
  flex-direction: row;
  align-items: center;
  justify-content: center;
`;

const Logo = styled(LogoIcon)`
  margin-left: auto;
  margin-right: auto;
  margin-bottom: ${normVert(119)}px;
`;
