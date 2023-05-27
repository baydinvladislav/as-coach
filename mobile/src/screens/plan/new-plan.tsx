import React, { useRef, useState } from 'react';
import { StyleSheet, TouchableOpacity, View } from 'react-native';

import { observer } from 'mobx-react';
import moment from 'moment';
import styled from 'styled-components';

import { useStore } from '@hooks';
import { t } from '@i18n';
import { useNavigation } from '@navigation';
import { colors, normHor, normVert } from '@theme';
import { Calendar, Input, Text, ViewWithButtons } from '@ui';

import { FontSize, TFormProps, TPlan } from '~types';

import { PlanScreens } from './plan';

export const NewPlanScreen = observer(
  ({
    values,
    handleChange,
    handleNavigate,
    errors,
    clearErrors,
    isLoading,
  }: TFormProps) => {
    const calendarRef = useRef<{
      handleChangeDateType: (type: 'start' | 'end') => void;
    }>();

    const { goBack } = useNavigation();

    const handlePress = (type: 'start' | 'end') => {
      clearErrors();
      calendarRef.current?.handleChangeDateType?.(type);
    };

    return (
      <>
        <Text style={styles.title} color={colors.white} fontSize={FontSize.S17}>
          {t('newPlan.title')}
        </Text>
        <Flex>
          <Inputs handlePress={handlePress} values={values} errors={errors} />
        </Flex>
        <ViewWithButtons
          onCancel={goBack}
          onConfirm={() =>
            handleNavigate(PlanScreens.CREATE_PLAN_SCREEN, undefined, true)
          }
          confirmText={t('buttons.next')}
          isLoading={isLoading}
          style={{ justifyContent: 'space-between' }}
          containerStyle={{ flex: 1 }}
        >
          <Calendar
            ref={calendarRef}
            values={{ start: values.start_date, end: values.end_date }}
            onChange={{
              start: handleChange('start_date'),
              end: handleChange('end_date'),
            }}
          />
        </ViewWithButtons>
      </>
    );
  },
);

type InputsProps = {
  handlePress: (type: 'start' | 'end') => void;
  values: TPlan;
  errors: Record<string, any>;
};

// Кнопки вынесены в отдельный компонент, чтобы изменение state не ререндерило календарь
const Inputs = ({ handlePress, values, errors }: InputsProps) => {
  const [dateType, setDateType] = useState<'start' | 'end' | null>('start');

  return (
    <>
      <Wrapper onPress={() => (handlePress('start'), setDateType('start'))}>
        <View pointerEvents="none">
          <Input
            placeholder={t('inputs.startDate')}
            value={
              values.start_date
                ? moment(values.start_date, 'yyyy-M-DD').format('DD MMM ddd')
                : undefined
            }
            isFocused={dateType === 'start'}
            error={errors.start_date}
            showError={false}
          />
        </View>
      </Wrapper>
      <Wrapper onPress={() => (handlePress('end'), setDateType('end'))}>
        <View pointerEvents="none">
          <Input
            placeholder={t('inputs.endDate')}
            isFocused={dateType === 'end'}
            value={
              values.end_date
                ? moment(values.end_date, 'yyyy-M-DD').format('DD MMM ddd')
                : undefined
            }
            error={errors.end_date}
            showError={false}
          />
        </View>
      </Wrapper>
    </>
  );
};

const styles = StyleSheet.create({
  title: {
    marginTop: normVert(14),
    marginBottom: normVert(20),
    marginLeft: normHor(16),
  },
  input: {
    marginBottom: normVert(20),
  },
});

const Flex = styled(View)`
  flex-direction: row;
  width: 100%;
  justify-content: space-between;
  padding-horizontal: ${normHor(16)}px;
  margin-bottom: ${normVert(44)}px;
`;

const Wrapper = styled(TouchableOpacity)`
  width: 48%;
  border-radius: 12px;
`;
