import React from 'react';
import { StyleSheet } from 'react-native';

import { observer } from 'mobx-react';

import { useStore } from '@hooks';
import { t } from '@i18n';
import { useNavigation } from '@navigation';
import { colors, normVert } from '@theme';
import { Input, Text, ViewWithButtons } from '@ui';

import { FontSize } from '~types';

type TProps = {
  onPrev: () => void;
  handleSubmit: () => void;
  values: any;
  handleChange: (e: string | React.ChangeEvent<any>) => () => void;
};

export const NewDayScreen = observer(
  ({ onPrev, handleSubmit, values, handleChange }: TProps) => {
    const { loading } = useStore();
    const { goBack } = useNavigation();

    const isLoading = loading.isLoading;

    return (
      <>
        <Text style={styles.title} color={colors.white} fontSize={FontSize.S24}>
          {t('newDay.title', { day: '1' })}
        </Text>
        <ViewWithButtons
          style={{ justifyContent: 'space-between' }}
          onCancel={onPrev}
          onConfirm={handleSubmit}
          confirmText={t('buttons.next')}
          isLoading={isLoading}
        >
          <Input
            placeholder="Название тренировки"
            value={values.start_date}
            onChangeText={handleChange('start_date')}
          />
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
});
