import React, { useEffect } from 'react';
import { StyleSheet, View } from 'react-native';

import { observer } from 'mobx-react';
import { useFormik } from 'formik';

import { useStore } from '@hooks';
import { t } from '@i18n';
import { CustomerProps } from '@store';
import { colors, normHor, normVert } from '@theme';
import { RadioButtonGroup, Input, Text, ViewWithButtons } from '@ui';
import { createExercise } from '@api';
import { createExerciseSchema } from '@utils';
import { Screens, useNavigation } from '@navigation';

import { FontSize, TPlan, TMuscleGroups } from '~types';

import { PlanScreens } from './plan';

type TProps = {
  params: Record<string, any>;
  customer: CustomerProps;
  errors: Record<string, any>;
  handleSubmit: () => void;
  handleNavigate: (
    nextScreen: PlanScreens,
    params?: Record<string, any>,
    withValidate?: boolean,
  ) => void;
  setValues: React.Dispatch<React.SetStateAction<TPlan>>;
  handleChange: (e: string | React.ChangeEvent<any>) => () => void;
};

export const CreateExerciseScreen = observer(
  ({
    params,
    errors,
    handleSubmit,
    handleNavigate,
    setValues,
    handleChange,
  }: TProps) => {
    const { loading, user } = useStore();
    const isLoading = loading.isLoading;
    const data = user.muscleGroups;
    const { navigate } = useNavigation();
    
    useEffect(() => {
      user.getMuscleGroups();
      // eslint-disable-next-line react-hooks/exhaustive-deps
    }, []);

    const onSubmit = (values: TMuscleGroups) => {
      createExercise(user.id, {
        ...values,
      }).then(() => navigate(Screens.DetailClient, { id: user.id }));
    };
  
    const {
      handleChange,
      handleSubmit,
      errors,
      values,
      setValues,
      validateForm,
      setErrors,
    } = useFormik({
      initialValues: {
        name: '',
        muscle_group_id: '',
      },
      onSubmit,
      validationSchema: createExerciseSchema,
      validateOnChange: false,
      validateOnBlur: false,
    });

    return (
      <>
        <Text style={styles.title} color={colors.white} fontSize={FontSize.S20}>
          {t('newExercise.title')}
        </Text>
        <View style={styles.input}>
          <Input
            placeholder={t('newExercise.placeholder')}
            // value={values.trainings?.[params.dayNumber]?.name}
            onChangeText={handleChange(`trainings[${params.dayNumber}].name`)}
            error={errors.trainings?.[params.dayNumber]?.name}
          />
        </View>
        <Text
          style={styles.subtitle}
          color={colors.grey4}
          fontSize={FontSize.S12}
        >
          {t('newExercise.subtitle')}
        </Text>
        <ViewWithButtons
          style={{ justifyContent: 'space-between' }}
          confirmText={t('buttons.create')}
          onConfirm={handleSubmit}
          cancelText={t('buttons.cancel')}
          onCancel={() => handleNavigate(PlanScreens.CREATE_DATE_SCREEN)}
          isLoading={isLoading}
          isScroll={true}
        >
          {data.map((item: { id: string; name: string; }) => (
            <RadioButtonGroup
              key={item.id}
              style={[
                styles.checkbox,
                item.name != data[0].name && styles.border,
              ]}
              placeholder={item.name}
              value={false}
            />
          ))}
        </ViewWithButtons>
      </>
    );
  },
);

const styles = StyleSheet.create({
  checkbox: {
    paddingVertical: normVert(16),
  },

  title: {
    marginTop: normVert(14),
    marginBottom: normVert(16),
    marginLeft: normHor(16),
  },

  subtitle: {
    textTransform: 'uppercase',
    marginLeft: normHor(16),
    marginBottom: normVert(8),
    fontWeight: 'bold',
  },

  border: {
    borderTopColor: colors.black3,
    borderTopWidth: 1,
  },

  input: {
    marginBottom: normVert(40),
    marginHorizontal: normHor(16),
  },
});
