import React from 'react';
import { StyleSheet, View } from 'react-native';

import { useFormik } from 'formik';
import { observer } from 'mobx-react';
import styled from 'styled-components';

import { PHONE_MASK, TOP_PADDING } from '@constants';
import { useStore } from '@hooks';
import { t } from '@i18n';
import { Screens, useNavigation } from '@navigation';
import { CustomerProps } from '@store';
import { colors, normHor, normVert } from '@theme';
import { Input, Keyboard, ModalLayout, Text, ViewWithButtons } from '@ui';
import { addClientValidationSchema, isIOS, transformPhone } from '@utils';

import { FontSize } from '~types';

export const AddClientScreen = observer(() => {
  const { customer, loading } = useStore();

  const isLoading = loading.isLoading;

  const { navigate } = useNavigation();

  const handleAddClient = (values: Partial<CustomerProps>) => {
    customer
      .createCustomer({
        ...values,
        phone_number: transformPhone(values.phone_number),
      })
      .then(() => navigate(Screens.LkScreen));
  };

  const { errors, handleChange, values, handleSubmit } = useFormik({
    initialValues: { phone_number: '', first_name: '', last_name: '' },
    onSubmit: handleAddClient,
    validationSchema: addClientValidationSchema,
    validateOnChange: false,
    validateOnBlur: false,
  });

  return (
    <ModalLayout>
      <Text style={styles.title} color={colors.white} fontSize={FontSize.S24}>
        {t('addClient.title')}
      </Text>
      <ViewWithButtons
        style={{ justifyContent: 'space-between' }}
        onCancel={() => navigate(Screens.LkScreen)}
        onConfirm={handleSubmit}
        confirmText={t('buttons.add')}
        isLoading={isLoading}
      >
        <View>
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
          <Input
            keyboardType={'phone-pad'}
            mask={PHONE_MASK}
            style={styles.input}
            placeholder={t('inputs.phone')}
            value={values.phone_number}
            onChangeText={handleChange('phone_number')}
            error={errors.phone_number}
            description={t('addClient.phoneDescription')}
          />
        </View>
      </ViewWithButtons>
    </ModalLayout>
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
