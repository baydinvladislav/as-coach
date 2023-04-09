import React from 'react';
import { StyleSheet, View } from 'react-native';

import { useFormik } from 'formik';
import { observer } from 'mobx-react';
import styled from 'styled-components';

import { PHONE_MASK, TOP_PADDING } from '@constants';
import { t } from '@i18n';
import { Screens, useNavigation } from '@navigation';
import { colors, normHor, normVert } from '@theme';
import { Input, Text, ViewWithButtons } from '@ui';
import { isIOS } from '@utils';

import { FontSize } from '~types';

export const AddClientScreen = observer(() => {
  const { navigate } = useNavigation();

  const { errors, handleChange, values } = useFormik({
    initialValues: { username: '', firstName: '', lastName: '' },
    onSubmit: () => console.log(123),
    validationSchema: () => console.log(123),
    validateOnChange: false,
    validateOnBlur: false,
  });
  return (
    <View style={{ flex: 1, paddingTop: isIOS ? TOP_PADDING : 0 }}>
      {isIOS && (
        <TopBackground>
          <Line />
        </TopBackground>
      )}
      <Background style={{ paddingTop: isIOS ? 0 : TOP_PADDING }}>
        <Text style={styles.title} color={colors.white} fontSize={FontSize.S24}>
          {t('addClient.title')}
        </Text>
        <ViewWithButtons
          style={{ justifyContent: 'space-between' }}
          onCancel={() => navigate(Screens.LkScreen)}
          onConfirm={() => navigate(Screens.LkScreen)}
          confirmText={t('buttons.add')}
        >
          <View>
            <Input
              keyboardType={'phone-pad'}
              style={styles.input}
              placeholder={t('inputs.firstName')}
              value={values.firstName}
              onChangeText={handleChange('firstName')}
              error={errors.firstName}
            />
            <Input
              style={styles.input}
              placeholder={t('inputs.lastName')}
              value={values.lastName}
              onChangeText={handleChange('lastName')}
              error={errors.lastName}
            />
            <Input
              style={styles.input}
              placeholder={t('inputs.phone')}
              mask={PHONE_MASK}
              value={values.username}
              onChangeText={handleChange('username')}
              error={errors.username}
              description={t('addClient.phoneDescription')}
            />
          </View>
        </ViewWithButtons>
      </Background>
    </View>
  );
});

const styles = StyleSheet.create({
  title: {
    marginTop: normVert(14),
    marginBottom: normVert(20),
    marginLeft: normVert(16),
  },
  input: {
    marginBottom: normVert(20),
  },
});

const Background = styled(View)`
  background-color: ${colors.black6};
  flex: 1;
  padding-top: ${normVert(40)}px;
`;

const TopBackground = styled(View)`
  background-color: ${colors.black6};
  flex: 1;
  position: absolute;
  top: ${normVert(34)}px;
  width: 100%;
  border-top-left-radius: 16px;
  border-top-right-radius: 16px;
  justify-content: center;
  align-items: center;
`;

const Line = styled(View)`
  background-color: ${colors.grey3};
  width: ${normHor(76)}px;
  height: ${normVert(6)}px;
  border-radius: 100px;
  margin-vertical: ${normVert(10)}px;
`;
