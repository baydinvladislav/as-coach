import React, { useState } from 'react';
import { StyleSheet, View } from 'react-native';

import { observer } from 'mobx-react';

import { CheckboxGroup, SearchInput } from '@components';
import { useStore } from '@hooks';
import { t } from '@i18n';
import { CustomerProps } from '@store';
import { colors, normHor, normVert } from '@theme';
import { Text, ViewWithButtons } from '@ui';

import { FontSize, TMuscleGroups, TPlan } from '~types';

import { PlanScreens } from './plan';

type TProps = {
  customer: CustomerProps;
  handleSubmit: () => void;
  values: TPlan;
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
    setValues,
  }: TProps) => {
    const [searchValue, setSearchValue] = useState<string | undefined>();
    const { loading, user } = useStore();
    const isLoading = loading.isLoading;
    const data = user.muscleGroups;
    
    return (
      <>
        <Text style={styles.title} color={colors.white} fontSize={FontSize.S20}>
          {t('newExercise.title')}
        </Text>
        <View style={styles.searchInput}>
          <SearchInput value={searchValue} onChangeText={setSearchValue} />
        </View>
        <ViewWithButtons
          style={{ justifyContent: 'space-between' }}
          onCancel={() => handleNavigate(PlanScreens.CREATE_DATE_SCREEN)}
          onConfirm={handleSubmit}
          confirmText={t('buttons.create')}
          cancelText={t('buttons.cancel')}
          isLoading={isLoading}
          isScroll={true}
          // eslint-disable-next-line react/no-children-prop
          children={undefined}
        />
        <CheckboxGroup data={data} />
      </>
    );
  },
);

const styles = StyleSheet.create({
  title: {
    marginTop: normVert(14),
    marginBottom: normVert(16),
    marginLeft: normHor(16),
  },

  searchInput: {
    marginBottom: normVert(20),
    marginHorizontal: normHor(16),
  },
});
