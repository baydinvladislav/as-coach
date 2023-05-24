import React, { useState } from 'react';
import { Image, StyleSheet, TouchableOpacity, View } from 'react-native';

import { useFormik } from 'formik';
import { isEmpty } from 'lodash';
import { observer } from 'mobx-react';
import moment from 'moment';
import {
  ImagePickerResponse,
  launchImageLibrary,
} from 'react-native-image-picker';
import { formatWithMask } from 'react-native-mask-input';
import styled from 'styled-components';

import { CameraIcon, DefaultAvatarImage } from '@assets';
import { DATE_MASK, PHONE_MASK } from '@constants';
import { useStore } from '@hooks';
import { t } from '@i18n';
import { Screens, useNavigation } from '@navigation';
import { UserProps } from '@store';
import { colors, normHor, normVert } from '@theme';
import { Input, Keyboard, Select, Text, ViewWithButtons } from '@ui';
import {
  makeAvatarLink,
  profileEditValidationSchema,
  transformPhone,
} from '@utils';

import { FontSize } from '~types';

export const ProfileEditScreen = observer(() => {
  const [response, setResponse] = useState<ImagePickerResponse>();
  const [uri, setUri] = useState('');

  const { navigate } = useNavigation();

  const { user, loading } = useStore();

  const isLoading = loading.isLoading;

  const handleEdit = (values: Partial<UserProps>) => {
    user
      .profileEdit({
        ...values,
        birthday: values.birthday
          ? moment(values.birthday, 'DD.mm.yy').format('yyyy-M-DD')
          : '',
        username: transformPhone(values?.username),
        photo: response?.assets?.[0],
      })
      .then(() => {
        navigate(Screens.ProfileScreen);
      });
  };

  const { errors, handleChange, handleSubmit, values } = useFormik({
    initialValues: {
      ...user.me,
      username: formatWithMask({ text: user.me.username, mask: PHONE_MASK })
        .masked,
      birthday: user.me.birthday
        ? moment(user.me.birthday, 'yyyy-mm-DD').format('DD.mm.yy')
        : '',
      photo: undefined as unknown as Blob,
    },
    onSubmit: handleEdit,
    validationSchema: profileEditValidationSchema,
    validateOnChange: false,
    validateOnBlur: false,
  });

  const handleChoosePhoto = async () => {
    await launchImageLibrary(
      {
        mediaType: 'photo',
        includeBase64: false,
      },
      async response => {
        if (!isEmpty(response)) {
          setResponse(response);
          setUri(
            'file:///' +
              (response.assets && response.assets[0].uri?.split('file:///')[1]),
          );
        }
      },
    );
  };

  return (
    <Keyboard style={{ flex: 1 }}>
      <ViewWithButtons
        onCancel={() => navigate(Screens.ProfileScreen)}
        onConfirm={() => handleSubmit()}
        style={{ paddingTop: normVert(80), justifyContent: 'space-between' }}
        isLoading={isLoading}
        isScroll={true}
      >
        <Text align="center" fontSize={FontSize.S17} color={colors.white}>
          {t('edit.editTitle')}
        </Text>
        <AvatarCircle
          style={{ alignItems: 'center', justifyContent: 'center' }}
          onPress={handleChoosePhoto}
        >
          <View style={styles.photo}>
            <CameraIcon stroke={colors.green} />
          </View>
          <Avatar
            source={
              uri
                ? {
                    uri: 'file://' + uri,
                  }
                : user.me.photo_path
                ? { uri: makeAvatarLink(user.me.photo_path) }
                : DefaultAvatarImage
            }
          />
        </AvatarCircle>
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
          data={{
            keys: ['Мужской', 'Женский'],
            values: ['male', 'female'],
          }}
        />
        <Input
          style={styles.input}
          placeholder={t('inputs.birthday')}
          value={values.birthday}
          onChangeText={handleChange('birthday')}
          error={errors.birthday}
          mask={DATE_MASK}
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
          isDisabled={true}
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
  photo: {
    backgroundColor: colors.black8,
    width: normHor(92),
    height: normVert(92),
    alignItems: 'center',
    justifyContent: 'center',
    borderRadius: 100,
    position: 'absolute',
    zIndex: 1,
  },
});

const Avatar = styled(Image)`
  width: 100%;
  height: 100%;
`;

const AvatarCircle = styled(TouchableOpacity)`
  width: ${normHor(92)}px;
  height: ${normVert(92)}px;
  border-radius: 100px;
  margin-left: auto;
  overflow: hidden;
  margin-right: auto;
  margin-vertical: ${normVert(32)}px;
`;
