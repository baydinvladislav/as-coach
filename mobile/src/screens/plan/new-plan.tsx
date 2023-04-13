import React from 'react';
import { StyleSheet, View } from 'react-native';

import { useFormik } from 'formik';
import { observer } from 'mobx-react';
import styled from 'styled-components';

import { TOP_PADDING } from '@constants';
import { useStore } from '@hooks';
import { t } from '@i18n';
import { useNavigation } from '@navigation';
import { colors, normHor, normVert } from '@theme';
import { DatePickerInput, Keyboard, Text, ViewWithButtons } from '@ui';
import { isIOS } from '@utils';

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

    const isDisabled = loading.isLoading;

    return (
      <Keyboard style={{ flex: 1, paddingTop: isIOS ? TOP_PADDING : 0 }}>
        {isIOS && (
          <TopBackground>
            <Line />
          </TopBackground>
        )}
        <Background style={{ paddingTop: isIOS ? 0 : TOP_PADDING }}>
          <Text
            style={styles.title}
            color={colors.white}
            fontSize={FontSize.S24}
          >
            {t('newPlan.title')}
          </Text>
          <ViewWithButtons
            style={{ justifyContent: 'space-between' }}
            onCancel={goBack}
            onConfirm={handleSubmit}
            confirmText={t('buttons.next')}
            isDisabled={isDisabled}
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
        </Background>
      </Keyboard>
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

const Background = styled(View)`
  background-color: ${colors.black6};
  flex: 1;
  padding-top: ${normVert(40)}px;
`;

const TopBackground = styled(View)`
  background-color: ${colors.black6};
  flex: 1;
  position: absolute;
  top: ${normVert(34)}px;
  width: 100%;
  border-top-left-radius: 16px;
  border-top-right-radius: 16px;
  justify-content: center;
  align-items: center;
`;

const Line = styled(View)`
  background-color: ${colors.grey3};
  width: ${normHor(76)}px;
  height: ${normVert(6)}px;
  border-radius: 100px;
  margin-vertical: ${normVert(10)}px;
`;
