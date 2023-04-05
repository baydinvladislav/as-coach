import React from 'react';
import { StyleSheet, View } from 'react-native';

import { AxiosError } from 'axios';
import { useFormik } from 'formik';
import { observer } from 'mobx-react';
import styled from 'styled-components';

import { LogoIcon } from '@assets';
import { PasswordInput } from '@components';
import { PHONE_MASK, TOP_PADDING } from '@constants';
import { useStore } from '@hooks';
import { t } from '@i18n';
import { Screens, useNavigation } from '@navigation';
import { colors, normVert } from '@theme';
import { Button, Input, Keyboard, Text } from '@ui';
import { loginValidationSchema, transformPhone } from '@utils';

import { ButtonType, FontSize } from '~types';

export const LoginScreen = observer(() => {
  const { navigate } = useNavigation();

  const { user, loading } = useStore();
  const isDisabled = loading.isLoading;

  const handleLogin = (values: { username: string; password: string }) => {
    user
      .login({
        ...values,
        username: transformPhone(values.username),
      })
      .then(() => navigate(Screens.LkScreen))
      .catch((e: AxiosError<{ detail: string }>) => {
        setErrors({ password: e.response?.data.detail });
      });
  };

  const { setErrors, errors, handleChange, handleSubmit, values } = useFormik({
    initialValues: { username: '', password: '' },
    onSubmit: handleLogin,
    validationSchema: loginValidationSchema,
    validateOnChange: false,
    validateOnBlur: false,
  });

  return (
    <View style={{ flex: 1 }}>
      <Keyboard style={{ paddingTop: TOP_PADDING }}>
        <Logo />
        <Text
          style={styles.title}
          align="center"
          fontSize={FontSize.S24}
          color={colors.white}
        >
          {t('auth.loginTitle')}
        </Text>
        <Inputs>
          <Input
            keyboardType={'phone-pad'}
            mask={PHONE_MASK}
            style={styles.input}
            placeholder={t('inputs.phone')}
            value={values.username}
            onChangeText={handleChange('username')}
            error={errors.username}
          />
          <PasswordInput
            value={values.password}
            placeholder={t('inputs.password')}
            onChangeText={handleChange('password')}
            error={errors.password}
          />
        </Inputs>
      </Keyboard>
      <Button
        style={styles.button}
        type={ButtonType.PRIMARY}
        onPress={() => handleSubmit()}
        isDisabled={isDisabled}
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
    </View>
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

const Inputs = styled(View)`
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
