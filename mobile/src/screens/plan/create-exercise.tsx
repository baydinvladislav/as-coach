import React, { useEffect, useState } from 'react';
import { StyleSheet, View } from 'react-native';

import { observer } from 'mobx-react';
import RadioGroup from 'react-native-radio-buttons-group';

import { useStore } from '@hooks';
import { t } from '@i18n';
import { CustomerProps } from '@store';
import { colors, normHor, normVert } from '@theme';
import { Input, Text, ViewWithButtons } from '@ui';

import { FontSize, TPlan } from '~types';

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
    const [selectedId, setSelectedId] = useState<string | undefined>();

    // send request to api
    useEffect(() => {
      user.getMuscleGroups();
      // eslint-disable-next-line react-hooks/exhaustive-deps
    }, []);

    // mapping response
    const formattedOptions = data.map(option => ({
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
          <RadioGroup
            radioButtons={formattedOptions}
            onPress={setSelectedId}
            selectedId={selectedId}
            containerStyle={styles.radioButton}
          />
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
    borderTopWidth: 1,
  },

  input: {
    marginBottom: normVert(40),
    marginHorizontal: normHor(16),
  },
});
