import React from 'react';
import { StyleSheet, View } from 'react-native';

import styled from 'styled-components';

import { LogoIcon } from '@assets';
import { t } from '@i18n';
import { colors, normVert } from '@theme';
import { Button, Input, Layout, Text } from '@ui';

import { ButtonType, FontSize } from '~types';

export const RegistrationScreen = () => (
  <Layout
    backgroundBlurRadius={10}
    backgroundOpacity={0.3}
    style={styles.layout}
  >
    <Logo />
    <Text
      style={styles.title}
      align="center"
      fontSize={FontSize.S24}
      color={colors.white}
    >
      {t('auth.registrationTitle')}
    </Text>
    <InputsContainer>
      <Input style={styles.input} placeholder={t('inputs.firstName')} />
      <Input style={styles.input} placeholder={t('inputs.phone')} />
      <Input placeholder={t('inputs.password')} />
    </InputsContainer>
    <Button
      style={styles.button}
      type={ButtonType.PRIMARY}
      onPress={() => null}
    >
      {t('buttons.continue')}
    </Button>
    <Flex>
      <Text fontSize={FontSize.S17} color={colors.white}>
        {t('auth.hasAccount')}
      </Text>
      <Button
        style={styles.button2}
        type={ButtonType.TEXT}
        onPress={() => null}
      >
        {t('buttons.login')}
      </Button>
    </Flex>
  </Layout>
);

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
});

const InputsContainer = styled(View)`
  margin-bottom: auto;
  height: 100%;
`;

const Flex = styled(View)`
  flex-direction: row;
  align-items: center;
  justify-content: center;
`;

const Logo = styled(LogoIcon)`
  margin-left: auto;
  margin-right: auto;
  margin-bottom: ${normVert(119)}px;
`;
