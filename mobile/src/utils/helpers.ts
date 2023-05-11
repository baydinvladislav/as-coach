import { TPlan, TPropsExercises } from '~types';

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
            exercises: value.reduce(
              (acc: TPropsExercises[], item, key, arr) => {
                const index = acc.findIndex(el => el.id === item.supersetId);
                delete item.supersetId;

                if (index >= 0) {
                  if (acc[index]?.supersets) {
                    acc?.[index]?.supersets?.push(item.id);
                  } else {
                    acc[index].supersets = [item.id];
                  }
                } else {
                  acc.push(item);
                }

                return acc;
              },
              [],
            ),
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
      item.supersetId &&
      (arr[key - 1]?.supersetId === item.supersetId ||
        arr[key + 1]?.supersetId === item.supersetId)
        ? item
        : { ...item, supersetId: undefined },
  );
