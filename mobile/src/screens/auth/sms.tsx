import React, { useState } from 'react';
import { StyleSheet, View } from 'react-native';

import {
  CodeField,
  Cursor,
  useBlurOnFulfill,
  useClearByFocusCell,
} from 'react-native-confirmation-code-field';
import styled from 'styled-components';

import { LogoIcon } from '@assets';
import { TOP_PADDING } from '@constants';
import { t } from '@i18n';
import { RoutesProps, Screens, useNavigation } from '@navigation';
import { colors, normHor, normVert } from '@theme';
import { Button, Keyboard, Text } from '@ui';

import { ButtonType, FontSize } from '~types';

const CELL_COUNT = 4;
const PHONE = '+7 (985) 000-00-00';

export const SmsScreen = ({ route }: RoutesProps) => {
  const { navigate } = useNavigation();
  const currentScreen = (route.params as { from: Screens })?.from;

  const [value, setValue] = useState('');
  const ref = useBlurOnFulfill({ value, cellCount: CELL_COUNT });
  const [props, getCellOnLayoutHandler] = useClearByFocusCell({
    value,
    setValue,
  });

  return (
    <Keyboard style={{ flex: 1, paddingTop: TOP_PADDING }}>
      <Logo />
      <Text
        style={styles.title}
        align="center"
        fontSize={FontSize.S20}
        color={colors.white}
      >
        {t('auth.smsTitle')}
      </Text>
      <Text
        align="center"
        style={{ lineHeight: 22 }}
        fontSize={FontSize.S17}
        color={colors.black4}
      >
        {t('auth.smsText1')}
      </Text>
      <Text
        align="center"
        style={{ lineHeight: 22 }}
        fontSize={FontSize.S17}
        color={colors.black5}
      >
        {PHONE}
      </Text>
      <Text
        style={styles.title}
        align="center"
        fontSize={FontSize.S17}
        color={colors.black4}
      >
        {t('auth.smsText2')}
      </Text>
      <Inputs>
        <CodeField
          value={value}
          onChangeText={setValue}
          cellCount={CELL_COUNT}
          rootStyle={styles.codeFieldRoot}
          keyboardType="number-pad"
          textContentType="oneTimeCode"
          renderCell={({ index, symbol, isFocused }) => (
            <Cell
              isError={true}
              index={index}
              key={index}
              onLayout={getCellOnLayoutHandler(index)}
            >
              <CellText>{symbol || (isFocused ? <Cursor /> : null)}</CellText>
            </Cell>
          )}
        />
        <ErrorText fontSize={FontSize.S12} color={colors.red}>
          Неправильный код, попробуйте ещё раз
        </ErrorText>
      </Inputs>
      <Button
        style={styles.button}
        type={ButtonType.PRIMARY}
        onPress={() =>
          currentScreen === Screens.RegistrationScreen
            ? navigate(Screens.LoginScreen)
            : navigate(Screens.ChangePasswordScreen)
        }
      >
        {t('buttons.confirm')}
      </Button>
      <Button
        style={styles.button2}
        type={ButtonType.TEXT}
        onPress={() => null}
      >
        {t('buttons.getCode')}
      </Button>
    </Keyboard>
  );
};

const styles = StyleSheet.create({
  title: {
    marginBottom: normVert(32),
  },
  button: {
    marginBottom: normVert(20),
  },
  button2: {
    marginLeft: 5,
  },
  input: {
    marginBottom: normVert(20),
  },
  codeFieldRoot: { marginTop: 20, justifyContent: 'center' },
});

const Cell = styled(View)<{ index: number; isError?: boolean }>`
  width: ${normHor(41)}px;
  height: ${normVert(48)}px;
  background-color: ${({ isError }) => (isError ? colors.red2 : colors.black3)};
  border-radius: 12px;
  margin-left: ${({ index }) => (index !== 0 ? normHor(6) : 0)}px;
  align-items: center;
  justify-content: center;
  ${({ isError }) =>
    isError &&
    `border-width: 1px;
     border-color: ${colors.red};`}
`;

const CellText = styled(Text)`
  font-size: ${FontSize.S17};
  text-align: center;
  color: ${colors.white};
`;

const Inputs = styled(View)`
  flex: 1;
`;

const Logo = styled(LogoIcon)`
  margin-left: auto;
  margin-right: auto;
  margin-bottom: ${normVert(119)}px;
`;

const ErrorText = styled(Text)`
  margin-top: ${normVert(4)}px;
  margin-left: auto;
  margin-right: auto;
`;
