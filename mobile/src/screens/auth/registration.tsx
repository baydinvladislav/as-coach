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
import { UserProps } from '@store';
import { colors, normVert } from '@theme';
import { Button, Input, Keyboard, Text } from '@ui';
import { registrationValidationSchema, transformPhone } from '@utils';

import { ButtonType, FontSize } from '~types';

export const RegistrationScreen = observer(() => {
  const { navigate } = useNavigation();

  const { user, loading } = useStore();
  const isLoading = loading.isLoading;

  const handleRegister = (values: Partial<UserProps>) => {
    user
      .register({
        ...values,
        username: transformPhone(values.username),
      })
      .then(() => navigate(Screens.LkScreen))
      .catch((e: AxiosError<{ detail: string }>) => {
        setErrors({ username: e.response?.data.detail });
      });
  };

  const { setErrors, errors, handleChange, handleSubmit, values } = useFormik({
    initialValues: { first_name: '', username: '', password: '' },
    onSubmit: handleRegister,
    validationSchema: registrationValidationSchema,
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
          {t('auth.registrationTitle')}
        </Text>
        <Inputs>
          <Input
            style={styles.input}
            placeholder={t('inputs.firstName')}
            value={values.first_name}
            onChangeText={handleChange('first_name')}
            error={errors.first_name}
          />
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
            placeholder={t('inputs.password')}
            value={values.password}
            onChangeText={handleChange('password')}
            error={errors.password}
          />
        </Inputs>
      </Keyboard>
      <Button
        style={styles.button}
        type={ButtonType.PRIMARY}
        onPress={() => handleSubmit()}
        isLoading={isLoading}
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
