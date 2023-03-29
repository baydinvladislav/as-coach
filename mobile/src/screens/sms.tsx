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
import { t } from '@i18n';
import { colors, normHor, normVert } from '@theme';
import { Button, Layout, Text } from '@ui';

import { ButtonType, FontSize } from '~types';

const CELL_COUNT = 4;

export const SmsScreen = () => {
  const phone = '+7 (985) 000-00-00';

  const [value, setValue] = useState('');
  const ref = useBlurOnFulfill({ value, cellCount: CELL_COUNT });
  const [props, getCellOnLayoutHandler] = useClearByFocusCell({
    value,
    setValue,
  });

  return (
    <Layout
      backgroundBlurRadius={10}
      backgroundOpacity={0.3}
      style={styles.layout}
    >
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
        {phone}
      </Text>
      <Text
        style={styles.title}
        align="center"
        fontSize={FontSize.S17}
        color={colors.black4}
      >
        {t('auth.smsText2')}
      </Text>
      <InputsContainer>
        <CodeField
          value={value}
          onChangeText={setValue}
          cellCount={CELL_COUNT}
          rootStyle={styles.codeFieldRoot}
          keyboardType="number-pad"
          textContentType="oneTimeCode"
          renderCell={({ index, symbol, isFocused }) => (
            <Cell
              index={index}
              key={index}
              onLayout={getCellOnLayoutHandler(index)}
            >
              <CellText>{symbol || (isFocused ? <Cursor /> : null)}</CellText>
            </Cell>
          )}
        />
      </InputsContainer>
      <Button
        style={styles.button}
        type={ButtonType.PRIMARY}
        onPress={() => null}
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
    </Layout>
  );
};

const styles = StyleSheet.create({
  title: {
    marginBottom: normVert(32),
  },
  layout: { flex: 1 },
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

const Cell = styled(View)<{ index: number }>`
  width: ${normHor(41)}px;
  height: ${normVert(48)}px;
  background-color: ${colors.black3};
  border-radius: 12px;
  margin-left: ${({ index }) => (index !== 0 ? normHor(6) : 0)}px;
  align-items: center;
  justify-content: center;
`;

const CellText = styled(Text)`
  font-size: ${FontSize.S17};
  text-align: center;
  color: ${colors.white};
`;

const InputsContainer = styled(View)`
  margin-bottom: auto;
  height: 100%;
`;

const Logo = styled(LogoIcon)`
  margin-left: auto;
  margin-right: auto;
  margin-bottom: ${normVert(119)}px;
`;
