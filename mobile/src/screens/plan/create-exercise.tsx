import React, { useEffect, useState } from 'react';
import { StyleSheet, View } from 'react-native';

import { observer } from 'mobx-react';
import { RadioButton } from 'react-native-radio-buttons-group';

import { useStore } from '@hooks';
import { t } from '@i18n';
import { colors, normHor, normVert } from '@theme';
import { Input, Text, ViewWithButtons } from '@ui';

import { FontSize } from '~types';

import { PlanScreens } from './plan';

type TProps = {
  params: Record<string, any>;
  handleNavigate: (
    nextScreen: PlanScreens,
    params?: Record<string, any>,
    withValidate?: boolean,
  ) => void;
};

export const CreateExerciseScreen = observer(
  ({ handleNavigate, params }: TProps) => {
    const { loading, user } = useStore();
    const isLoading = loading.isLoading;
    const muscleGroups = user.muscleGroups;
    const [muscleGroupId, setMuscleGroupId] = useState<string | undefined>();
    const [exerciseName, setExerciseName] = useState('');

    // send request to api to fetch muscle groups
    useEffect(() => {
      user.getMuscleGroups();
      // eslint-disable-next-line react-hooks/exhaustive-deps
    }, []);

    // mapping response to create radio buttons
    const formattedOptions = muscleGroups.map(option => ({
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

    // send request to create exercise
    const handleSubmit = () => {
      user
        .createExercise({
          name: exerciseName,
          muscle_group_id: muscleGroupId,
        })
        .then(() =>
          handleNavigate(PlanScreens.CREATE_DAY_EXERCISES_SCREEN, params, true),
        );
    };

    function handlePress(id: string) {
      if (id !== muscleGroupId && setMuscleGroupId) {
        setMuscleGroupId(id);
      }
    }

    return (
      <>
        <Text style={styles.title} color={colors.white} fontSize={FontSize.S20}>
          {t('newExercise.title')}
        </Text>
        <View style={styles.input}>
          <Input
            placeholder={t('newExercise.placeholder')}
            onChangeText={setExerciseName}
            value={exerciseName}
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
          <View>
            {formattedOptions.map(button => (
              <RadioButton
                {...button}
                key={button.id}
                containerStyle={[
                  button.value != formattedOptions[0].value && styles.border,
                ]}
                selected={button.id === muscleGroupId}
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
