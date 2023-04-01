import React from 'react';
import { StyleSheet, View } from 'react-native';

import { Formik } from 'formik';
import styled from 'styled-components';

import { LogoIcon } from '@assets';
import { useStore } from '@hooks';
import { t } from '@i18n';
import { Screens, useNavigation } from '@navigation';
import { colors, normVert } from '@theme';
import { Button, Input, Layout, Text } from '@ui';

import { ButtonType, FontSize } from '~types';

export const RegistrationScreen = () => {
  const { navigate } = useNavigation();

  const { user } = useStore();

  const handleRegister = (values: { username: string; password: string }) => {
    user.register({ username: '+79991899544', password: '123123123' });
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
        {t('auth.registrationTitle')}
      </Text>
      <Formik
        initialValues={{ username: '', password: '' }}
        onSubmit={handleRegister}
      >
        {({ handleChange, handleSubmit, values }) => (
          <>
            <InputsContainer>
              <Input style={styles.input} placeholder={t('inputs.firstName')} />
              <Input style={styles.input} placeholder={t('inputs.phone')} />
              <Input placeholder={t('inputs.password')} />
            </InputsContainer>
            <Button
              style={styles.button}
              type={ButtonType.PRIMARY}
              onPress={() => {
                handleSubmit();
                // navigate(Screens.SmsScreen, {
                //   from: Screens.RegistrationScreen,
                // })
              }}
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
    </Layout>
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
