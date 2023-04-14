import React from 'react';
import { StyleSheet, View } from 'react-native';

import { observer } from 'mobx-react';

import { AddIcon } from '@assets';
import { CheckboxGroup, SearchInput } from '@components';
import { useStore } from '@hooks';
import { t } from '@i18n';
import { useNavigation } from '@navigation';
import { colors, normHor, normVert } from '@theme';
import { Button, Text, ViewWithButtons } from '@ui';

import { ButtonType, FontSize } from '~types';

type TProps = {
  onPrev: () => void;
  handleSubmit: () => void;
  values: any;
  handleChange: (e: string | React.ChangeEvent<any>) => () => void;
};

const CHECKBOX_DATA = [
  {
    id: 1,
    title: 'Бицепс',
    items: [
      { id: 1, value: false, placeholder: 'Подъем штанги на бицепс' },
      { id: 2, value: false, placeholder: 'Молот' },
      { id: 3, value: false, placeholder: 'Подъем штанги на бицепс' },
      { id: 4, value: false, placeholder: 'Сгибания гантелями стоя' },
      { id: 5, value: false, placeholder: 'Паучьи сгибания' },
    ],
  },
  {
    id: 2,
    title: 'Ноги',
    items: [
      { id: 1, value: false, placeholder: 'Жим ногами' },
      { id: 2, value: false, placeholder: 'Выпады в смите' },
      { id: 3, value: false, placeholder: 'Сгибания ног' },
      { id: 4, value: false, placeholder: 'Разведение ног' },
    ],
  },
  {
    id: 3,
    title: 'Кардио',
    items: [
      { id: 1, value: false, placeholder: 'Беговая дорожка' },
      { id: 2, value: false, placeholder: 'Велосипед' },
      { id: 3, value: false, placeholder: 'Эллипс' },
    ],
  },
];

export const DayExercisesScreen = observer(
  ({ onPrev, handleSubmit, values, handleChange }: TProps) => {
    const { loading } = useStore();
    const { goBack } = useNavigation();

    const isLoading = loading.isLoading;

    return (
      <>
        <Text style={styles.title} color={colors.white} fontSize={FontSize.S24}>
          {t('newDay.exercisesTitle', { day: '1', exercises: 'Бицепс' })}
        </Text>
        <View style={styles.searchInput}>
          <SearchInput />
        </View>
        <Button
          style={styles.addExercisesButton}
          type={ButtonType.TEXT}
          onPress={() => console.log(123)}
          leftIcon={<AddIcon stroke={colors.green} />}
        >
          {t('buttons.createExercises')}
        </Button>
        <ViewWithButtons
          style={{ justifyContent: 'space-between' }}
          onCancel={onPrev}
          onConfirm={handleSubmit}
          confirmText={t('buttons.next')}
          isLoading={isLoading}
          isScroll={true}
        >
          {CHECKBOX_DATA.map(item => (
            <CheckboxGroup
              style={styles.checkboxGroup}
              key={item.id}
              data={item.items}
              title={'Бицепс'}
            />
          ))}
        </ViewWithButtons>
      </>
    );
  },
);

const styles = StyleSheet.create({
  checkboxGroup: {
    marginTop: normVert(20),
  },
  title: {
    marginTop: normVert(14),
    marginBottom: normVert(16),
    marginLeft: normHor(16),
  },
  addExercisesButton: {
    marginRight: 'auto',
    marginLeft: normHor(16),
    marginBottom: normVert(20),
  },
  searchInput: {
    marginBottom: normVert(20),
    marginHorizontal: normHor(16),
  },
});
