import React, { useEffect, useState } from 'react';
import { StyleSheet, View } from 'react-native';

import { observer } from 'mobx-react';
import {
  NestableDraggableFlatList,
  RenderItemParams,
} from 'react-native-draggable-flatlist';
import styled from 'styled-components';

import { CheckboxWithSets } from '@components';
import { useStore } from '@hooks';
import { t } from '@i18n';
import { colors, normHor, normVert } from '@theme';
import { Text, ViewWithButtons } from '@ui';
import { modifyPlan } from '@utils';

import { FontSize, TPlan, TPropsExercises } from '~types';

import { PlanScreens } from './plan';

type TProps = {
  handleNavigate: (
    nextScreen: PlanScreens,
    params?: Record<string, any>,
    withValidate?: boolean,
  ) => void;
  values: TPlan;
  handleChange: (e: string | React.ChangeEvent<any>) => () => void;
  setValues: React.Dispatch<React.SetStateAction<TPlan>>;
  params: Record<string, any>;
  errors: Record<string, any>;
};

export const EditExercisesScreen = observer(
  ({ handleNavigate, values, setValues, params, errors }: TProps) => {
    const [data, setData] = useState<TPropsExercises[]>([]);
    const [selected, setSelected] = useState<string[]>([]);
    const { customer } = useStore();

    const handlePress = (id: string) => {
      setSelected(selected => {
        if (selected.includes(id)) {
          return [...selected.filter(item => item !== id)];
        } else {
          return [...selected, id];
        }
      });
    };

    const exercises = values?.trainings?.[params.dayNumber]?.exercises;
    const dayName = values?.trainings?.[params.dayNumber]?.name;

    const handleChangeSets = (id: string, e: React.ChangeEvent<any>) => {
      setData(data =>
        data.map(item =>
          item.id === id ? { ...item, sets: e.target.value } : item,
        ),
      );
    };

    const handleCancel = () => {
      handleNavigate(PlanScreens.CREATE_SUPERSETS_SCREEN, params);
    };

    const handleConfirm = () => {
      setValues(values => modifyPlan(values, dayName, data ?? []));
      handleNavigate(PlanScreens.CREATE_SUPERSETS_SCREEN, params, true);
    };

    useEffect(() => {
      setData(exercises);
      // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [exercises]);

    const handleSuperset = (arr: string[]) => {
      if (arr.length >= 2) {
        setData(data => {
          const exercise = data.find(item => selected.includes(item.id));
          const index = data.findIndex(item => selected.includes(item.id));
          const supersets = selected.filter(item => item !== exercise?.id);
          data[index] = {
            ...exercise,
            supersets,
          } as TPropsExercises;
          return data.filter(
            item => !(selected.includes(item.id) && !item.supersets?.length),
          );
        });
        setSelected([]);
      }
    };

    const handleDelete = (arr: string[]) => {
      if (arr.length) {
        setSelected([]);
        setData(data =>
          data
            .map(item => ({
              ...item,
              supersets: item.supersets?.filter(
                superset => !arr.includes(superset),
              ),
            }))
            .filter(item => !arr.includes(item.id)),
        );
      }
    };

    const renderItem = ({
      item,
      drag,
      isActive,
      getIndex,
    }: RenderItemParams<TPropsExercises>) => {
      const { name } = customer.getExerciseById(item.id);
      const index = getIndex() ?? 0;
      const isSelected = selected.includes(item.id);

      return (
        <View style={{ position: 'relative' }}>
          <CheckboxWithSets
            key={item.id}
            placeholder={name}
            isFirst={index === 0}
            handlePress={() => handlePress(item.id)}
            exercise={item}
            errors={errors}
            handleChangeSets={e => handleChangeSets(item.id, e)}
            index={index}
            isSelected={isSelected}
            onDrag={drag}
          />
          {item.supersets?.map((superset, key) => {
            const { name } = customer.getExerciseById(superset);
            const isSelected = selected.includes(superset);
            return (
              <View key={key}>
                <Line />
                <CheckboxWithSets
                  key={superset}
                  placeholder={name}
                  isFirst={true}
                  handlePress={() => handlePress(superset)}
                  exercise={item}
                  errors={errors}
                  handleChangeSets={e => handleChangeSets(item.id, e)}
                  index={index}
                  isSelected={isSelected}
                  onDrag={drag}
                />
              </View>
            );
          })}
        </View>
      );
    };

    return (
      <>
        <View style={styles.row}>
          <Text
            style={styles.title}
            color={colors.white}
            fontSize={FontSize.S24}
          >
            {t('supersets.title', {
              quantity: exercises.length,
            })}
          </Text>
          <Text color={colors.black4} fontSize={FontSize.S12}>
            {t('supersets.editMode')}
          </Text>
        </View>
        <Text
          style={styles.exercisesText}
          color={colors.black4}
          fontSize={FontSize.S10}
        >
          {t('supersets.dayTitle', {
            day: params.dayNumber + 1,
            name: dayName,
          })}
        </Text>
        <ViewWithButtons
          style={{ justifyContent: 'space-between', height: '100%' }}
          onCancel={handleCancel}
          onConfirm={handleConfirm}
          confirmText={t('buttons.saveChanges')}
          cancelText={t('buttons.cancel')}
          onSuperset={() => handleSuperset(selected)}
          onDelete={() => handleDelete(selected)}
          isSelected={Boolean(selected.length)}
          isScroll={true}
          isDraggable={true}
        >
          <NestableDraggableFlatList
            data={data}
            renderItem={renderItem}
            keyExtractor={item => item.id}
            onDragEnd={({ data }) => setData(data)}
          />
        </ViewWithButtons>
      </>
    );
  },
);

const styles = StyleSheet.create({
  checkboxGroup: {
    marginTop: normVert(20),
  },
  row: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginLeft: normHor(16),
    marginRight: normHor(16),
  },
  exercisesText: {
    textTransform: 'uppercase',
    marginBottom: normVert(40),
    marginLeft: normHor(16),
  },
  title: {
    marginTop: normVert(14),
    marginBottom: normVert(16),
  },
});

const Line = styled(View)`
  background-color: ${colors.green};
  width: 1px;
  height: ${normVert(64)}px;
  position: absolute;
  bottom: ${normVert(106)}px;
  left: ${normHor(11)}px;
`;
