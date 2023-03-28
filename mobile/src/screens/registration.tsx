import React from 'react';
import { StyleSheet } from 'react-native';

import { Layout, Text } from '@ui';

export const RegistrationScreen = () => (
  <Layout style={styles.layout}>
    <Text>login</Text>
  </Layout>
);

const styles = StyleSheet.create({
  layout: { flex: 1, justifyContent: 'flex-end' },
});
