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
import { changePasswordSchema } from '@utils';

import { ButtonType, FontSize } from '~types';

export const NewChangePasswordScreen = observer(() => {
  const { user, loading } = useStore();
  const { navigate } = useNavigation();

  const isLoading = loading.isLoading;

  const handleChangePassword = (values: Pick<UserProps, 'password'>) => {
    user.changePassword(values).then(() => {
      navigate(Screens.ProfileScreen);
    });
  };

  const { errors, handleChange, handleSubmit, values } = useFormik({
    initialValues: {
      password: '',
      newPassword: '',
    },
    validationSchema: changePasswordSchema,
    onSubmit: handleChangePassword,
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
      <Inputs>
        <PasswordInput
          style={styles.input}
          placeholder={t('inputs.password')}
          value={values.password}
          onChangeText={handleChange('password')}
          error={errors.password}
        />
        <PasswordInput
          style={styles.input}
          placeholder={t('inputs.newPassword')}
          value={values.newPassword}
          onChangeText={handleChange('newPassword')}
          error={errors.newPassword}
        />
      </Inputs>
      <Button
        style={styles.button}
        type={ButtonType.PRIMARY}
        onPress={() => handleSubmit()}
        isLoading={isLoading}
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
    </Keyboard>
  );
});

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

const Inputs = styled(View)`
  flex: 1;
  margin-top: ${normVert(32)}px;
`;

const Logo = styled(LogoIcon)`
  margin-left: auto;
  margin-right: auto;
  margin-bottom: ${normVert(119)}px;
`;
