import React from 'react';
import { StyleSheet, View } from 'react-native';

import { observer } from 'mobx-react';

import { SearchInput } from '@components';
import { useStore } from '@hooks';
import { t } from '@i18n';
import { CustomerProps } from '@store';
import { normHor, normVert } from '@theme';
import { ViewWithButtons } from '@ui';

import { TPlan } from '~types';

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
    customer,
    handleNavigate,
    handleSubmit,
    values,
    handleChange,
    errors,
    setValues,
  }: TProps) => {
    const searchValue = '';
    const setSearchValue = '';

    const { loading } = useStore();

    const isLoading = loading.isLoading;

    const handleDifferentTime = () => {
      if (values.different_time) {
        setValues(values => ({
          ...values,
          different_time: !values.different_time,
          diets: values.diets.filter((_, key) => key === 0),
        }));
      } else {
        setValues(values => ({
          ...values,
          different_time: !values.different_time,
          diets: [...values.diets, { proteins: '', fats: '', carbs: '' }],
        }));
      }
    };

    return (
      <ViewWithButtons
        style={{ justifyContent: 'space-between' }}
        onCancel={() => handleNavigate(PlanScreens.CREATE_DATE_SCREEN)}
        onConfirm={handleSubmit}
        confirmText={t('buttons.createPlan')}
        cancelText={t('buttons.prev')}
        isLoading={isLoading}
        isScroll={true}
      >
        <View style={styles.searchInput}>
          <SearchInput value={searchValue} />
        </View>
      </ViewWithButtons>
    );
  },
);

const styles = StyleSheet.create({
  searchInput: {
    marginBottom: normVert(20),
    marginHorizontal: normHor(16),
  },
});
