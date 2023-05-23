import React from 'react';
import { StyleSheet, View } from 'react-native';

import { useFormik } from 'formik';
import { observer } from 'mobx-react';
import styled from 'styled-components';

import { LogoIcon } from '@assets';
import { PasswordInput } from '@components';
import { TOP_PADDING } from '@constants';
import { useStore } from '@hooks';
import { t } from '@i18n';
import { Screens, useNavigation } from '@navigation';
import { UserProps } from '@store';
import { colors, normVert } from '@theme';
import { Button, Keyboard, Text } from '@ui';
import { confirmPasswordSchema } from '@utils';

import { ButtonType, FontSize } from '~types';

export const ChangePasswordScreen = observer(() => {
  const { user, loading } = useStore();
  const { navigate } = useNavigation();

  const isLoading = loading.isLoading;

  const handleConfirmPassword = (values: Pick<UserProps, 'password'>) => {
    user.confirmPassword(values).then(data => {
      if (data.confirmed_password) {
        navigate(Screens.NewChangePasswordScreen);
      } else {
        setErrors({ password: t('errors.confirmPasswordError') });
      }
    });
  };

  const { setErrors, errors, handleChange, handleSubmit, values } = useFormik({
    initialValues: {
      password: '',
    },
    validationSchema: confirmPasswordSchema,
    onSubmit: handleConfirmPassword,
    validateOnChange: false,
    validateOnBlur: false,
  });

  return (
    <Keyboard style={{ flex: 1, paddingTop: TOP_PADDING }}>
      <Logo />
      <Text
        style={styles.title}
        align="center"
        fontSize={FontSize.S24}
        color={colors.white}
      >
        {t('changePassword.changePasswordTitle')}
      </Text>
      <Inputs>
        <PasswordInput
          style={styles.input}
          placeholder={t('inputs.password')}
          value={values.password}
          onChangeText={handleChange('password')}
          error={errors.password}
        />
      </Inputs>
      <Button
        style={styles.button}
        type={ButtonType.PRIMARY}
        onPress={() => handleSubmit()}
        isLoading={isLoading}
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
    </Keyboard>
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

const Logo = styled(LogoIcon)`
  margin-left: auto;
  margin-right: auto;
  margin-bottom: ${normVert(119)}px;
`;
