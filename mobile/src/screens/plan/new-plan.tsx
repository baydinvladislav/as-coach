import React, { useState } from 'react';
import { StyleSheet, TouchableOpacity, View } from 'react-native';

import { observer } from 'mobx-react';
import moment from 'moment';
import styled from 'styled-components';

import { useStore } from '@hooks';
import { t } from '@i18n';
import { useNavigation } from '@navigation';
import { colors, normHor, normVert } from '@theme';
import { Calendar, Input, Text, ViewWithButtons } from '@ui';

import { FontSize, TPlan } from '~types';

import { PlanScreens } from './plan';

type TProps = {
  values: TPlan;
  handleChange: (e: string | React.ChangeEvent<any>) => () => void;
  handleNavigate: (nextScreen: PlanScreens) => void;
};

export const NewPlanScreen = observer(
  ({ values, handleChange, handleNavigate }: TProps) => {
    const [dateType, setDateType] = useState<'start' | 'end' | null>(null);

    const handleChangeDateType = (type: 'start' | 'end') => {
      setDateType(type);
    };
    const { loading } = useStore();
    const { goBack } = useNavigation();

    const isLoading = loading.isLoading;

    const handlePress = (type: 'start' | 'end') => {
      handleChangeDateType(type);
    };

    return (
      <>
        <Text style={styles.title} color={colors.white} fontSize={FontSize.S17}>
          {t('newPlan.title')}
        </Text>
        <Flex>
          <Wrapper
            isFocused={dateType === 'start'}
            onPress={() => handlePress('start')}
          >
            <View pointerEvents="none">
              <Input
                placeholder={t('inputs.startDate')}
                value={
                  values.start_date
                    ? moment(values.start_date, 'yyyy-mm-DD').format(
                        'DD MMM ddd',
                      )
                    : undefined
                }
              />
            </View>
          </Wrapper>
          <Wrapper
            isFocused={dateType === 'end'}
            onPress={() => handlePress('end')}
          >
            <View pointerEvents="none">
              <Input
                placeholder={t('inputs.endDate')}
                value={
                  values.end_date
                    ? moment(values.end_date, 'yyyy-mm-DD').format('DD MMM ddd')
                    : undefined
                }
              />
            </View>
          </Wrapper>
        </Flex>
        <ViewWithButtons
          onCancel={goBack}
          onConfirm={() => handleNavigate(PlanScreens.CREATE_PLAN_SCREEN)}
          confirmText={t('buttons.next')}
          isLoading={isLoading}
          style={{ justifyContent: 'space-between' }}
          containerStyle={{ flex: 1 }}
        >
          <Calendar
            dateType={dateType}
            values={{ start: values.start_date, end: values.end_date }}
            onChange={{
              start: handleChange('start_date'),
              end: handleChange('end_date'),
            }}
          />
          {/* <DatePickerInput
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
            /> */}
        </ViewWithButtons>
      </>
    );
  },
);

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

const Wrapper = styled(TouchableOpacity)<{ isFocused: boolean }>`
  width: 48%;
  ${({ isFocused }) =>
    `border: 1px solid ${isFocused ? colors.green : colors.transparent};`}
  border-radius: 12px;
`;
