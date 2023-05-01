import React, { useEffect } from 'react';
import { StyleSheet, View } from 'react-native';

import { observer } from 'mobx-react';

import { useStore } from '@hooks';
import { t } from '@i18n';
import { CustomerProps } from '@store';
import { colors, normHor, normVert } from '@theme';
import { Checkbox, Input, Text, ViewWithButtons } from '@ui';

import { FontSize, TPlan } from '~types';

import { PlanScreens } from './plan';

type TProps = {
  customer: CustomerProps;
  handleSubmit: () => void;
  values: TPlan;
  params: Record<string, any>;
  handleChange: (e: string | React.ChangeEvent<any>) => () => void;
  handleNavigate: (
    nextScreen: PlanScreens,
    params?: Record<string, any>,
    withValidate?: boolean,
  ) => void;
  errors: Record<string, any>;
  setValues: React.Dispatch<React.SetStateAction<TPlan>>;
};

export const CreateExerciseScreen = observer(
  ({
    handleNavigate,
    handleSubmit,
    values,
    handleChange,
    errors,
    params,
    setValues,
  }: TProps) => {
    const { loading, user } = useStore();
    const isLoading = loading.isLoading;
    const data = user.muscleGroups;
    const handlePress = () => {
      '§12';
    };

    useEffect(() => {
      user.getMuscleGroups();
      // eslint-disable-next-line react-hooks/exhaustive-deps
    }, []);

    return (
      <>
        <Text style={styles.title} color={colors.white} fontSize={FontSize.S20}>
          {t('newExercise.title')}
        </Text>
        <View style={styles.input}>
          <Input
            placeholder="Название"
            // value={values.trainings?.[params.dayNumber]?.name}
            onChangeText={handleChange(`trainings[${params.dayNumber}].name`)}
            error={errors.trainings?.[params.dayNumber]?.name}
          />
        </View>
        <ViewWithButtons
          style={{ justifyContent: 'space-between' }}
          onCancel={() => handleNavigate(PlanScreens.CREATE_DATE_SCREEN)}
          onConfirm={handleSubmit}
          confirmText={t('buttons.create')}
          cancelText={t('buttons.cancel')}
          isLoading={isLoading}
          isScroll={true}
        >
          {data.map(item => (
            <Checkbox
              key={item.id}
              style={[
                styles.checkbox,
                item.name != data[0].name && styles.border,
              ]}
              onChangeCheckbox={() => handlePress()}
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

  border: {
    borderTopColor: colors.black3,
    borderTopWidth: 1,
  },

  input: {
    marginBottom: normVert(40),
    marginHorizontal: normHor(16),
  },
});
