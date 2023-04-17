import React from 'react';
import { StyleSheet } from 'react-native';

import { observer } from 'mobx-react';
import styled from 'styled-components';

import { AddIcon } from '@assets';
import { CreatePlanItem } from '@components';
import { useStore } from '@hooks';
import { t } from '@i18n';
import { colors, normVert } from '@theme';
import {
  Button,
  Checkbox,
  Input,
  InputSpinner,
  Text,
  ViewWithButtons,
} from '@ui';

import { ButtonType, FontSize } from '~types';

type TProps = {
  onPrev: () => void;
  handleSubmit: () => void;
  values: any;
  handleChange: (e: string | React.ChangeEvent<any>) => () => void;
};

export const CreatePlanScreen = observer(
  ({ onPrev, handleSubmit, values, handleChange }: TProps) => {
    const { loading } = useStore();

    const isLoading = loading.isLoading;

    return (
      <ViewWithButtons
        style={{ justifyContent: 'space-between' }}
        onCancel={onPrev}
        onConfirm={handleSubmit}
        confirmText={t('buttons.next')}
        cancelText={t('buttons.prev')}
        isLoading={isLoading}
        isScroll={true}
      >
        <NameText>Сухарева София</NameText>
        <Text style={styles.title} color={colors.white} fontSize={FontSize.S24}>
          14 АВГ — 26 АВГ
        </Text>
        <CreatePlanItem title={t('createPlan.title1')}>
          <Checkbox
            style={styles.checkbox}
            placeholder={t('createPlan.checkboxDescription')}
            value={values.different_time}
            onChangeCheckbox={handleChange('different_time')}
          />
          {values.different_time && (
            <Text
              style={styles.text}
              fontSize={FontSize.S16}
              color={colors.black4}
            >
              {t('createPlan.days1')}
            </Text>
          )}
          <InputSpinner
            style={styles.input}
            placeholder={t('createPlan.placeholder1')}
            value={values.squirrels1}
            onChangeText={handleChange('squirrels1')}
          />
          <InputSpinner
            style={styles.input}
            placeholder={t('createPlan.placeholder2')}
            value={values.fats1}
            onChangeText={handleChange('fats1')}
          />
          <InputSpinner
            placeholder={t('createPlan.placeholder3')}
            value={values.carbohydrates1}
            onChangeText={handleChange('carbohydrates1')}
          />

          {values.different_time && (
            <>
              <Text
                style={[styles.text, styles.restDays]}
                fontSize={FontSize.S16}
                color={colors.black4}
              >
                {t('createPlan.days2')}
              </Text>
              <InputSpinner
                style={styles.input}
                placeholder={t('createPlan.placeholder1')}
                value={values.squirrels2}
                onChangeText={handleChange('squirrels2')}
              />
              <InputSpinner
                style={styles.input}
                placeholder={t('createPlan.placeholder2')}
                value={values.fats2}
                onChangeText={handleChange('fats2')}
              />
              <InputSpinner
                placeholder={t('createPlan.placeholder3')}
                value={values.carbohydrates2}
                onChangeText={handleChange('carbohydrates2')}
              />
            </>
          )}
        </CreatePlanItem>
        <CreatePlanItem title={t('createPlan.title2')}>
          <Button
            style={styles.addDayButton}
            type={ButtonType.TEXT}
            onPress={() => console.log(123)}
            leftIcon={<AddIcon stroke={colors.green} />}
          >
            {t('buttons.addDay')}
          </Button>
          <InputSpinner
            style={styles.input}
            placeholder={t('createPlan.description1')}
            value={values?.days?.[0]?.rest1}
            onChangeText={handleChange('days[0].rest1')}
          />
          <InputSpinner
            style={styles.input}
            placeholder={t('createPlan.description2')}
            value={values?.days?.[0]?.rest2}
            onChangeText={handleChange('days[0].rest2')}
          />
        </CreatePlanItem>
        <CreatePlanItem title={t('createPlan.title3')}>
          <Input
            placeholder={t('createPlan.enterText')}
            isTextarea={true}
            height={normVert(96)}
            value={values.notes}
            onChangeText={handleChange('notes')}
          />
        </CreatePlanItem>
      </ViewWithButtons>
    );
  },
);

const styles = StyleSheet.create({
  title: {
    marginTop: normVert(14),
  },
  input: {
    marginBottom: normVert(20),
  },
  text: {
    marginBottom: normVert(20),
  },
  restDays: {
    marginTop: normVert(33),
  },
  addDayButton: { marginRight: 'auto', marginBottom: normVert(20) },
  checkbox: {
    marginBottom: normVert(20),
  },
});

const NameText = styled(Text)`
  text-transform: uppercase;
  color: ${colors.black4};
  font-size: ${FontSize.S10};
  margin-bottom: ${normVert(16)}px;
`;