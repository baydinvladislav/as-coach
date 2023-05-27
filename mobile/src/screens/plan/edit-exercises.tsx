import React, { useCallback, useState } from 'react';
import {
  LayoutAnimation,
  StyleSheet,
  TouchableOpacity,
  UIManager,
  View,
} from 'react-native';

import { observer } from 'mobx-react';
import {
  NestableDraggableFlatList,
  RenderItemParams,
} from 'react-native-draggable-flatlist';
import styled from 'styled-components';

import { SupersetIcon, TrashIcon } from '@assets';
import { CheckboxWithSets } from '@components';
import { useStore } from '@hooks';
import { t } from '@i18n';
import { useFocusEffect } from '@react-navigation/native';
import { colors, normHor, normVert } from '@theme';
import { Text, ViewWithButtons } from '@ui';
import {
  changeFirstSupersetId,
  clearArray,
  isIOS,
  modifyPlan,
  moveExerciseFromDown,
  moveExerciseFromUp,
} from '@utils';

import { FontSize, FontWeight, TFormProps, TPropsExercises } from '~types';

import { PlanScreens } from './plan';

if (!isIOS && UIManager.setLayoutAnimationEnabledExperimental) {
  UIManager.setLayoutAnimationEnabledExperimental(true);
}

export const EditExercisesScreen = observer(
  ({ handleNavigate, values, setValues, params, errors }: TFormProps) => {
    const [data, setData] = useState<TPropsExercises[]>([]);
    const [selected, setSelected] = useState<string[]>([]);
    const { customer } = useStore();

    const isSelectedDelete = Boolean(selected.length);
    const isSelectedSuperset = selected.length >= 2;

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

    const handleCancel = () => {
      handleNavigate(PlanScreens.CREATE_SUPERSETS_SCREEN, params);
    };

    const handleConfirm = () => {
      setValues(values => modifyPlan(values, dayName, data ?? []));
      handleNavigate(PlanScreens.CREATE_SUPERSETS_SCREEN, params, true);
    };

    useFocusEffect(
      useCallback(() => {
        console.clear();
        setData(
          exercises.map(item => {
            item.supersetId = item?.supersets?.[0];
            delete item.supersets;
            return item;
          }),
        );
        // eslint-disable-next-line react-hooks/exhaustive-deps
      }, []),
    );

    const handleSuperset = (arr: string[]) => {
      const isExist = data.filter(
        item => arr.includes(item.id) && item.supersetId,
      ).length;

      if (isSelectedSuperset) {
        if (isExist) {
          setData(data =>
            clearArray(
              data.map(item =>
                arr.includes(item.supersetId ?? '')
                  ? { ...item, supersetId: undefined }
                  : item,
              ),
            ),
          );
        } else {
          setData(data => {
            const index = Math.min(
              ...arr.map(item => data.findIndex(el => el.id === item)),
            );
            const { id: supersetId } = data[index];
            const maxSetsLength = data
              .filter(item => arr.includes(item.id))
              .reduce(
                (acc, item) =>
                  item.sets.length > acc ? item.sets.length : acc,
                0,
              );

            const items = data
              .filter(item => arr.includes(item.id))
              .map(item => ({
                ...item,
                sets:
                  maxSetsLength > item.sets.length
                    ? (() => {
                        for (
                          let i = 0;
                          i <= maxSetsLength - item.sets.length;
                          i++
                        ) {
                          item.sets.push(item.sets[item.sets.length - 1]);
                        }
                        return item.sets;
                      })()
                    : item.sets,
                supersetId,
              }));
            data = data.filter(item => !arr.includes(item.id));
            data.splice(index, 0, ...items);
            return data;
          });
        }
        LayoutAnimation.configureNext(LayoutAnimation.Presets.easeInEaseOut);
        setSelected([]);
      }
    };

    const handleChangeSets = (
      id: string,
      e: React.ChangeEvent<any>,
      supersetId?: string,
    ) => {
      setData(data =>
        data.map(el => {
          const item = { ...el };
          if (item.supersetId === supersetId && supersetId !== undefined) {
            const setsLength = e.target.value.length;
            if (setsLength) {
              if (item.sets.length > setsLength) {
                item.sets.length = setsLength;
              }
              if (item.sets.length < setsLength) {
                item.sets = [...item.sets, item.sets[item.sets.length - 1]];
              }
            }
          }
          if (item.id === id) {
            item.sets = e.target.value;
          }
          return item;
        }),
      );
    };

    const handleDelete = (arr: string[]) => {
      if (arr.length) {
        setSelected([]);
        setData(data => {
          let array: TPropsExercises[] = data.filter(
            item => !arr.includes(item.id),
          );
          arr.map(item => {
            const index = array.findIndex(el => item === el.supersetId);
            array = array.map((el, _, array) =>
              el.supersetId === array?.[index]?.supersetId
                ? {
                    ...el,
                    supersetId: array?.[index]?.id,
                  }
                : el,
            );
          });

          return clearArray(array);
        });
        LayoutAnimation.configureNext(LayoutAnimation.Presets.easeInEaseOut);
      }
    };

    const handleDragEnd = ({
      data: updated,
      from,
      to,
    }: {
      data: TPropsExercises[];
      from: number;
      to: number;
    }) => {
      if (from === to) return; // Если изменений нету ничего не делаем

      let arr: TPropsExercises[] = JSON.parse(JSON.stringify(updated));

      const supersets = data.reduce(
        (acc: Record<string, any>, item, index, arr) => {
          !item.supersetId && acc;
          if (
            item.supersetId &&
            arr?.[index - 1]?.supersetId !== item.supersetId
          ) {
            acc[item.supersetId] = [];
          }
          if (
            item.supersetId &&
            (arr?.[index - 1]?.supersetId !== item.supersetId ||
              arr?.[index + 1]?.supersetId !== item.supersetId)
          ) {
            acc[item.supersetId]?.push(index);
          }
          return acc;
        },
        {},
      );

      const [supersetsKeys, supersetsValues] = [
        Object.keys(supersets),
        Object.values(supersets),
      ];

      const isFromDown = to < from;
      const isFromUp = !isFromDown;
      if (data[from].supersetId === data[to].supersetId) {
        // Если перетаскиваем внутри суперсета, и ставим на первую позицию
        for (let i = 0; i < supersetsValues.length; i++) {
          if (to >= supersetsValues[i][0] && to <= supersetsValues[i][1]) {
            for (
              let key = supersetsValues[i][0];
              key <= supersetsValues[i][1];
              key++
            ) {
              arr[key].supersetId = arr[supersetsValues[i][0]].id;
            }
          }
        }
      } else if (
        data[from].supersetId &&
        (!data[to].supersetId ||
          !data?.[to + 1]?.supersetId ||
          !data?.[to - 1]?.supersetId)
      ) {
        // Если перетаскиваем из суперсета вне суперсета (перенос суперсета)
        const items = data.filter(
          item => item.supersetId === arr[to].supersetId,
        );
        arr = data.filter(item => item.supersetId !== arr[to].supersetId);
        arr.splice(to > from ? to - items.length + 1 : to, 0, ...items);
        LayoutAnimation.configureNext(LayoutAnimation.Presets.easeInEaseOut);
      } else if (data[from].supersetId === data[from].id) {
        // Переместили первое упражнение суперсета внутрь другого суперсета
        if (isFromUp) {
          moveExerciseFromUp(to, data, arr, supersetsKeys, supersetsValues);
        } else if (isFromDown) {
          moveExerciseFromDown(to, data, arr, supersetsKeys, supersetsValues);
        }
        arr = changeFirstSupersetId(data, arr, data[from].supersetId);
      } else if (isFromUp) {
        // Переместили упражнение не из суперсета в суперсет с направления верх
        moveExerciseFromUp(to, data, arr, supersetsKeys, supersetsValues);
      } else if (isFromDown) {
        // Переместили упражнение не из суперсета в суперсет с направления низ
        moveExerciseFromDown(to, data, arr, supersetsKeys, supersetsValues);
      }
      setData(clearArray(arr));
    };

    const renderItem = ({
      item,
      drag,
      getIndex,
    }: RenderItemParams<TPropsExercises>) => {
      const { name } = customer.getExerciseById(item.id);
      const isSelected = selected.includes(item.id);
      const index = getIndex() ?? 0;
      const isPrevSuperset = Boolean(data?.[index - 1]?.supersetId);

      return (
        <View style={{ backgroundColor: colors.black6 }}>
          <CheckboxWithSets
            key={item.id}
            placeholder={
              name
              // item.id.slice(0, 3) + ' - ' + item.supersetId?.slice(0, 3)
            }
            isFirst={!index || (isPrevSuperset && Boolean(item.supersetId))}
            handlePress={() => handlePress(item.id)}
            exercise={item}
            errors={errors}
            handleChangeSets={e =>
              handleChangeSets(item.id, e, item.supersetId)
            }
            index={index}
            isSelected={isSelected}
            onDrag={drag}
          />
          {item.supersetId && item.id !== item.supersetId && (
            <Line quantity={Math.ceil(item.sets.length / 4) - 1} />
          )}
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
              quantity: data.length,
            })}
          </Text>
          <Text
            color={colors.black4}
            fontSize={FontSize.S12}
            weight={FontWeight.Regular}
          >
            {t('supersets.editMode')}
          </Text>
        </View>
        <Text
          style={styles.exercisesText}
          color={colors.black4}
          fontSize={FontSize.S10}
          weight={FontWeight.Bold}
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
          isScroll={true}
          isDraggable={true}
          circles={
            <>
              <Circle1
                activeOpacity={isSelectedSuperset ? 0.5 : 1}
                onPress={() => handleSuperset(selected)}
              >
                <SupersetIcon opacity={isSelectedSuperset ? 1 : 0.5} />
              </Circle1>

              <Circle2
                activeOpacity={isSelectedDelete ? 0.5 : 1}
                onPress={() => handleDelete(selected)}
              >
                <TrashIcon opacity={isSelectedDelete ? 1 : 0.5} />
              </Circle2>
            </>
          }
        >
          <NestableDraggableFlatList
            data={data}
            renderItem={renderItem}
            keyExtractor={item => item.id}
            onDragEnd={handleDragEnd}
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

const Line = styled(View)<{ quantity: number }>`
  background-color: ${colors.green};
  width: 1px;
  height: ${({ quantity }) => normVert(64 + quantity * 64)}px;
  position: absolute;
  top: ${({ quantity }) => normVert(-58 - quantity * 66)}px;
  left: ${normHor(11)}px;
`;

const Circle1 = styled(TouchableOpacity)`
  position: absolute;
  z-index: 1;
  right: ${normHor(88)}px;
  bottom: ${normVert(174)}px;
  border-radius: 100px;
  width: ${normHor(52)}px;
  height: ${normVert(52)}px;
  background-color: ${colors.grey};
  justify-content: center;
  align-items: center;
`;

const Circle2 = styled(TouchableOpacity)`
  position: absolute;
  z-index: 1;
  right: ${normHor(24)}px;
  bottom: ${normVert(174)}px;
  border-radius: 100px;
  width: ${normHor(52)}px;
  height: ${normVert(52)}px;
  background-color: ${colors.grey};
  justify-content: center;
  align-items: center;
`;
