import React from 'react';
import { StyleSheet, View } from 'react-native';

import { observer } from 'mobx-react';

import { useStore } from '@hooks';
import { t } from '@i18n';
import { useNavigation } from '@navigation';
import { colors, normVert } from '@theme';
import { DatePickerInput, Text, ViewWithButtons } from '@ui';

import { FontSize } from '~types';

type TProps = {
  handleSubmit: () => void;
  values: any;
  handleChange: (e: string | React.ChangeEvent<any>) => () => void;
};

export const NewPlanScreen = observer(
  ({ handleSubmit, values, handleChange }: TProps) => {
    const { loading } = useStore();
    const { goBack } = useNavigation();

    const isLoading = loading.isLoading;

    return (
      <>
        <Text style={styles.title} color={colors.white} fontSize={FontSize.S24}>
          {t('newPlan.title')}
        </Text>
        <ViewWithButtons
          style={{ justifyContent: 'space-between' }}
          onCancel={goBack}
          onConfirm={handleSubmit}
          confirmText={t('buttons.next')}
          isLoading={isLoading}
        >
          <View>
            <DatePickerInput
              style={styles.input}
              placeholder="Дата начала"
              value={values.start_date}
              onChangeText={handleChange('start_date')}
            />
            <DatePickerInput
              style={styles.input}
              placeholder="Дата окончания"
              value={values.end_date}
              onChangeText={handleChange('end_date')}
            />
          </View>
        </ViewWithButtons>
      </>
    );
  },
);

const styles = StyleSheet.create({
  title: {
    marginTop: normVert(14),
    marginBottom: normVert(20),
    marginLeft: normVert(16),
  },
  input: {
    marginBottom: normVert(20),
  },
});
