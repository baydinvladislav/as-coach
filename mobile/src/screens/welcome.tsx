import React from 'react';

import styled from 'styled-components';

import { LogoIcon } from '@assets';
import { normVert } from '@theme';
import { Button, ButtonType, Layout } from '@ui';

export const WelcomeScreen = () => (
  <Layout style={{ flex: 1, justifyContent: 'flex-end' }}>
    <Logo />
    <Button style={styles.button} type={ButtonType.PRIMARY}>
      Войти
    </Button>
    <Button type={ButtonType.SECONDARY}>Зарегистрироваться</Button>
  </Layout>
);

const styles = {
  layout: {},
  button: {
    marginBottom: normVert(20),
  },
};

const Logo = styled(LogoIcon)`
  margin-left: auto;
  margin-right: auto;
  margin-bottom: ${normVert(40)}px;
`;
