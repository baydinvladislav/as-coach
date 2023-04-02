import React from 'react';
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
import { Button, Input, Text } from '@ui';
import { transformPhone } from '@utils';

import { ButtonType, FontSize } from '~types';

export const RegistrationScreen = observer(() => {
  const { navigate } = useNavigation();

  const { user, loading } = useStore();
  const isDisabled = loading.isLoading;

  const handleRegister = (values: {
    phone: string;
    username: string;
    password: string;
  }) => {
    user
      .register({
        ...values,
        phone: transformPhone(values.phone),
      })
      .then(() => navigate(Screens.LoginScreen));
  };

  return (
    <>
      <Logo />
      <Text
        style={styles.title}
        align="center"
        fontSize={FontSize.S24}
        color={colors.white}
      >
        {t('auth.registrationTitle')}
      </Text>
      <Formik
        initialValues={{ username: '', phone: '', password: '' }}
        onSubmit={handleRegister}
      >
        {({ handleChange, handleSubmit, values }) => (
          <>
            <InputsContainer>
              <Input
                style={styles.input}
                placeholder={t('inputs.firstName')}
                value={values.username}
                onChangeText={handleChange('username')}
              />
              <Input
                mask={PHONE_MASK}
                style={styles.input}
                placeholder={t('inputs.phone')}
                value={values.phone}
                onChangeText={handleChange('phone')}
              />
              <PasswordInput
                placeholder={t('inputs.password')}
                value={values.password}
                onChangeText={handleChange('password')}
              />
            </InputsContainer>
            <Button
              style={styles.button}
              type={ButtonType.PRIMARY}
              onPress={() => handleSubmit()}
              isDisabled={isDisabled}
            >
              {t('buttons.continue')}
            </Button>
            <Flex>
              <Text fontSize={FontSize.S17} color={colors.white}>
                {t('auth.hasAccount')}
              </Text>
              <Button
                style={styles.button2}
                type={ButtonType.TEXT}
                onPress={() => navigate(Screens.LoginScreen)}
              >
                {t('buttons.login')}
              </Button>
            </Flex>
          </>
        )}
      </Formik>
    </>
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
