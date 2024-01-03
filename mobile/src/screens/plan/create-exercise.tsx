import React, { useEffect } from 'react';
import { StyleSheet, View } from 'react-native';

import { useFormik } from 'formik';
import { observer } from 'mobx-react';
import { RadioButton } from 'react-native-radio-buttons-group';

import { useStore } from '@hooks';
import { t } from '@i18n';
import { colors, normHor, normVert } from '@theme';
import { Input, Text, ViewWithButtons } from '@ui';
import { createExerciseSchema } from '@utils';

import { FontSize, TExercises } from '~types';

import { PlanScreens } from './plan';

type TProps = {
  params: Record<string, any>;
  values: TExercises;
  setValues: React.Dispatch<React.SetStateAction<TExercises>>;
  handleNavigate: (
    nextScreen: PlanScreens,
    params?: Record<string, any>,
    withValidate?: boolean,
  ) => void;
};

/**
 * Screen for creating new exercise in library.
 *
 * @param handleNavigate - use to move in next screen
 * @param params - screen params
 */
export const CreateExerciseScreen = observer(
  ({ handleNavigate, params }: TProps) => {
    const { loading, user } = useStore();

    /**
     * Formats data for every radio button
     * based on muscle group
     */
    const formattedOptions = user.muscleGroups.map(option => ({
      id: option.id,
      label: option.name,
      value: option.id,
      color: colors.green,
      labelStyle: {
        color: colors.white,
        fontSize: 16,
        paddingVertical: normVert(10),
      },
    }));

    /**
     * If user submits the form,
     * it sends request to server and moves user
     * to exercises mapping screen again
     */
    const handleCreation = () => {
      user
        .createExercise({
          name: values.name,
          muscle_group_id: values.muscle_group_id,
        })
        .then(() =>
          handleNavigate(PlanScreens.CREATE_DAY_EXERCISES_SCREEN, params, true),
        );
    };

    const { handleSubmit, handleChange, values, setValues } = useFormik({
      initialValues: { name: '', muscle_group_id: '' },
      onSubmit: handleCreation,
      validationSchema: createExerciseSchema,
    });

    /**
     * Changes active element in
     * muscle group radio button list
     */
    function handlePress(id: string) {
      if (id !== values.muscle_group_id) {
        setValues(values => ({
          ...values,
          muscle_group_id: id,
        }));
      }
    }

    useEffect(() => {
      user.getMuscleGroups();
    }, [user]);

    return (
      <>
        <Text style={styles.title} color={colors.white} fontSize={FontSize.S20}>
          {t('newExercise.title')}
        </Text>
        <View style={styles.input}>
          <Input
            placeholder={t('newExercise.placeholder')}
            onChangeText={handleChange('name')}
            value={values.name}
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
          onConfirm={() => handleSubmit()}
          cancelText={t('buttons.cancel')}
          onCancel={() =>
            handleNavigate(
              PlanScreens.CREATE_DAY_EXERCISES_SCREEN,
              params,
              true,
            )
          }
          isLoading={loading.isLoading}
          isScroll={true}
        >
          <View>
            {formattedOptions.map(button => (
              <RadioButton
                {...button}
                key={button.id}
                containerStyle={[
                  button.value != formattedOptions[0].value && styles.border,
                ]}
                selected={button.id === values.muscle_group_id}
                onPress={() => handlePress(button.id)}
              />
            ))}
          </View>
        </ViewWithButtons>
      </>
    );
  },
);

const styles = StyleSheet.create({
  radioButton: {
    alignItems: 'flex-start',
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
    paddingTop: normVert(10),
    borderTopWidth: 1,
  },

  input: {
    marginBottom: normVert(40),
    marginHorizontal: normHor(16),
  },
});
