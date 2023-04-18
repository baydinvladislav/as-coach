import React from 'react';
import { StyleSheet } from 'react-native';

import { observer } from 'mobx-react';
import moment from 'moment';
import styled from 'styled-components';

import { AddIcon } from '@assets';
import { CreatePlanItem, ExercisesCard } from '@components';
import { useStore } from '@hooks';
import { t } from '@i18n';
import { CustomerProps } from '@store';
import { colors, normVert } from '@theme';
import {
  Button,
  Checkbox,
  Input,
  InputSpinner,
  Text,
  ViewWithButtons,
} from '@ui';

import { ButtonType, FontSize, TPlan } from '~types';

import { PlanScreens } from './plan';

type TProps = {
  customer: CustomerProps;
  handleSubmit: () => void;
  values: TPlan;
  handleChange: (e: string | React.ChangeEvent<any>) => () => void;
  handleNavigate: (nextScreen: PlanScreens) => void;
};

export const CreatePlanScreen = observer(
  ({
    customer,
    handleNavigate,
    handleSubmit,
    values,
    handleChange,
  }: TProps) => {
    const { loading } = useStore();

    const isLoading = loading.isLoading;

    return (
      <ViewWithButtons
        style={{ justifyContent: 'space-between' }}
        onCancel={() => handleNavigate(PlanScreens.CREATE_DATE_SCREEN)}
        onConfirm={handleSubmit}
        confirmText={t('buttons.next')}
        cancelText={t('buttons.prev')}
        isLoading={isLoading}
        isScroll={true}
      >
        <NameText>
          {customer?.first_name} {customer?.last_name}
        </NameText>
        <Text style={styles.title} color={colors.white} fontSize={FontSize.S24}>
          {moment(values.start_date).format('D MMM').slice(0, -1)} —{' '}
          {moment(values.end_date).format('D MMM').slice(0, -1)}
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
            value={values.diets[0].proteins}
            onChangeText={handleChange('diets[0].proteins')}
          />
          <InputSpinner
            style={styles.input}
            placeholder={t('createPlan.placeholder2')}
            value={values.diets[0].fats}
            onChangeText={handleChange('diets[0].fats')}
          />
          <InputSpinner
            placeholder={t('createPlan.placeholder3')}
            value={values.diets[0].carbs}
            onChangeText={handleChange('diets[0].carbs')}
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
                value={values.diets[1].proteins}
                onChangeText={handleChange('diets[1].proteins')}
              />
              <InputSpinner
                style={styles.input}
                placeholder={t('createPlan.placeholder2')}
                value={values.diets[1].fats}
                onChangeText={handleChange('diets[1].fats')}
              />
              <InputSpinner
                placeholder={t('createPlan.placeholder3')}
                value={values.diets[1].carbs}
                onChangeText={handleChange('diets[1].carbs')}
              />
            </>
          )}
        </CreatePlanItem>
        <CreatePlanItem title={t('createPlan.title2')}>
          {values.trainings.map(exercise => (
            <ExercisesCard key={exercise.name} exercises={exercise} />
          ))}
          <Button
            style={styles.addDayButton}
            type={ButtonType.TEXT}
            onPress={() => handleNavigate(PlanScreens.CREATE_DAY_SCREEN)}
            leftIcon={<AddIcon stroke={colors.green} />}
          >
            {t('buttons.addDay')}
          </Button>
          <InputSpinner
            style={styles.input}
            placeholder={t('createPlan.description1')}
            value={values.set_rest}
            onChangeText={handleChange('set_rest')}
          />
          <InputSpinner
            style={styles.input}
            placeholder={t('createPlan.description2')}
            value={values.exercise_rest}
            onChangeText={handleChange('exercise_rest')}
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
    textTransform: 'uppercase',
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
