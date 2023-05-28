import { Asset } from 'react-native-image-picker';

import { URL_ANDROID, URL_IOS } from '@constants';

import { TPlan, TPropsExercises } from '~types';

import { isIOS } from './constants';

export const modifyPlan = (
  values: TPlan,
  dayName: string,
  value: TPropsExercises[],
) =>
  ({
    ...values,
    trainings: [
      ...values.trainings.map(training => {
        if (training?.name === dayName) {
          return {
            ...training,
            exercises: value.reduce((acc: TPropsExercises[], item, _, arr) => {
              if (item.superset_id) {
                item.supersets = [item.superset_id];

                for (let i = 0; i <= arr.length; i++) {
                  const el = arr[i];
                  if (
                    el?.superset_id === item.superset_id &&
                    el.id !== item.superset_id
                  ) {
                    item.supersets?.push(el.id);
                  }
                }
              }
              acc.push(item);
              return acc;
            }, []),
          };
        } else {
          return training;
        }
      }),
    ],
  } as TPlan);

export const addExerciseToPlan = (
  values: TPlan,
  dayName: string,
  id: string,
  value?: string[],
) =>
  ({
    ...values,
    trainings: [
      ...values.trainings.map(training => {
        if (training?.name === dayName) {
          return {
            ...training,
            exercises: (() => {
              const exercises = training?.exercises;
              if (exercises?.length) {
                const isExists = !!exercises.find(item => item.id === id);
                const arr = exercises
                  .map(exercise => {
                    if (exercise.id === id) {
                      return value ? { ...exercise, sets: value } : undefined;
                    } else {
                      return exercise;
                    }
                  })
                  .filter(item => item);
                if (isExists) {
                  return arr;
                } else {
                  return [...arr, { id, sets: ['12', '12', '12'] }];
                }
              } else {
                return [{ id, sets: ['12', '12', '12'] }];
              }
            })(),
          };
        } else {
          return training;
        }
      }),
    ],
  } as TPlan);

export const clearArray = (arr: TPropsExercises[]) =>
  arr.map(
    (
      item,
      key,
      arr, // Очищаем массив с упражнениями от значений суперсетов, если упражнение не в суперсете
    ) =>
      item.superset_id &&
      (arr[key - 1]?.superset_id === item.superset_id ||
        arr[key + 1]?.superset_id === item.superset_id)
        ? item
        : { ...item, superset_id: undefined },
  );

export const changeFirstSupersetId = (
  data: TPropsExercises[],
  arr: TPropsExercises[],
  superset_id?: string,
) =>
  // Если первая позиция пропадает, то у упражнений суперсета меняем superset_id на тот id, который стал первым в суперсете
  arr.map(item => {
    if (item.superset_id === superset_id && item.id !== superset_id) {
      const id = data.find(
        item => item.superset_id === superset_id && item.id !== superset_id,
      )?.id;
      return { ...item, superset_id: id };
    }

    return item;
  });

export const moveExerciseFromUp = (
  to: number,
  data: TPropsExercises[],
  arr: TPropsExercises[],
  supersetsKeys: string[],
  supersetsValues: any[],
) => {
  for (let i = 0; i < supersetsValues.length; i++) {
    if (to >= supersetsValues[i][0] && to < supersetsValues[i][1]) {
      const superset_id = arr[to].superset_id;
      arr[to].superset_id = supersetsKeys[i];
      changeFirstSupersetId(data, arr, superset_id);
    }
  }
};

export const moveExerciseFromDown = (
  to: number,
  data: TPropsExercises[],
  arr: TPropsExercises[],
  supersetsKeys: string[],
  supersetsValues: any[],
) => {
  for (let i = 0; i < supersetsValues.length; i++) {
    if (to > supersetsValues[i][0] && to <= supersetsValues[i][1]) {
      const superset_id = arr[to].superset_id;
      arr[to].superset_id = supersetsKeys[i];
      changeFirstSupersetId(data, arr, superset_id);
    }
  }
};

export const createFormData = (photo?: Asset, body = {}) => {
  const data = new FormData();
  if (photo) {
    data.append('photo', {
      name: photo.fileName,
      type: photo.type,
      uri: isIOS ? photo?.uri?.replace('file://', '') : photo.uri,
    });
  }
  Object.keys(body).forEach(key => {
    if (key !== 'photo') {
      data.append(key, (body as any)[key]);
    }
  });

  return data;
};

export const makeAvatarLink = (link: string | null) => {
  const api = isIOS ? URL_IOS : URL_ANDROID;
  return link ? api + link : '';
};

export const getWeek = (date: Date) => {
  const firstWeekday = new Date(
    date.getFullYear(),
    date.getMonth(),
    1,
  ).getDay();
  const offsetDate = date.getDate() + firstWeekday - 1;
  return Math.floor(offsetDate / 7);
};

export const renderNumber = (number: string, join: string) => {
  const arr = number.split('/');

  return arr.join(join) + ' гр';
};
