import React from 'react';
import { Image, StyleSheet } from 'react-native';

import { useFormik } from 'formik';
import { observer } from 'mobx-react';
import { formatWithMask } from 'react-native-mask-input';
import styled from 'styled-components';

import { DefaultAvatarImage } from '@assets';
import { PHONE_MASK } from '@constants';
import { useStore } from '@hooks';
import { t } from '@i18n';
import { Screens, useNavigation } from '@navigation';
import { UserProps } from '@store';
import { colors, normHor, normVert } from '@theme';
import { Input, Keyboard, Select, Text, ViewWithButtons } from '@ui';
import { profileEditValidationSchema, transformPhone } from '@utils';

import { FontSize } from '~types';

export const ProfileEditScreen = observer(() => {
  const { navigate } = useNavigation();

  const { user, loading } = useStore();

  const isDisabled = loading.isLoading;

  const handleEdit = (values: Partial<UserProps>) => {
    user
      .profileEdit({ ...values, username: transformPhone(values?.username) })
      .then(() => {
        navigate(Screens.ProfileScreen);
      });
  };

  const { errors, handleChange, handleSubmit, values } = useFormik({
    initialValues: {
      ...user.me,
      username: formatWithMask({ text: user.me.username, mask: PHONE_MASK })
        .masked,
    },
    onSubmit: handleEdit,
    validationSchema: profileEditValidationSchema,
    validateOnChange: false,
    validateOnBlur: false,
  });

  return (
    <Keyboard>
      <ViewWithButtons
        onCancel={() => navigate(Screens.ProfileScreen)}
        onConfirm={() => handleSubmit()}
        style={{ paddingTop: normVert(80) }}
        isDisabled={isDisabled}
        isScroll={true}
      >
        <Text align="center" fontSize={FontSize.S17} color={colors.white}>
          {t('edit.editTitle')}
        </Text>
        <Avatar source={DefaultAvatarImage} />
        <Input
          style={styles.input}
          placeholder={t('inputs.firstName')}
          value={values.first_name}
          onChangeText={handleChange('first_name')}
          error={errors.first_name}
        />
        <Input
          style={styles.input}
          placeholder={t('inputs.lastName')}
          value={values.last_name}
          onChangeText={handleChange('last_name')}
          error={errors.last_name}
        />
        <Select
          style={styles.input}
          placeholder={t('inputs.gender')}
          value={values.gender}
          onChangeText={handleChange('gender')}
          error={errors.gender}
          data={{ keys: ['Мужской', 'Женский'], values: ['male', 'female'] }}
        />
        <Input
          style={styles.input}
          placeholder={t('inputs.birthday')}
          value={values.birthday}
          onChangeText={handleChange('birthday')}
          error={errors.birthday}
        />
        <Input
          style={styles.input}
          placeholder={t('inputs.email')}
          value={values.email}
          onChangeText={handleChange('email')}
          error={errors.email}
          autoCapitalize="none"
        />
        <Input
          mask={PHONE_MASK}
          keyboardType="phone-pad"
          placeholder={t('inputs.phone')}
          value={values.username}
          onChangeText={handleChange('username')}
          error={errors.username}
        />
      </ViewWithButtons>
    </Keyboard>
  );
});

const styles = StyleSheet.create({
  text: { marginBottom: normVert(62) },
  input: {
    marginBottom: normVert(20),
  },
});

const Avatar = styled(Image)`
  width: ${normHor(92)}px;
  height: ${normVert(92)}px;
  border-radius: 100px;
  margin-left: auto;
  margin-right: auto;
  margin-vertical: ${normVert(32)}px;
`;
