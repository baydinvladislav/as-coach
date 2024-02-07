import React from 'react';
import { StyleSheet, View } from 'react-native';

import { observer } from 'mobx-react';

import { AddIcon } from '@assets';
import { useStore } from '@hooks';
import { colors, normVert } from '@theme';
import { Button, Loader, Text } from '@ui';

import { ButtonType, FontSize, FontWeight } from '~types';

type TProps = {
  title: string;
  description: string;
  buttonText?: string;
  onPress: () => void;
};

export const LkEmpty = observer(
  ({ title, description, buttonText, onPress }: TProps) => {
    const { loading } = useStore();
    const isLoading = loading.isLoading;

    if (isLoading) {
      return (
        <View style={styles.text}>
          <Loader />
        </View>
      );
    }

    return (
      <View style={styles.text}>
        <Text
          align="center"
          style={{ lineHeight: 24, marginBottom: normVert(16) }}
          fontSize={FontSize.S24}
          color={colors.black5}
        >
          {title}
        </Text>
        <Text
          align="center"
          style={{ lineHeight: 24, marginBottom: normVert(24) }}
          fontSize={FontSize.S17}
          color={colors.black4}
          weight={FontWeight.Regular}
        >
          {description}
        </Text>
        {buttonText && (
          <Button
            type={ButtonType.TEXT}
            onPress={onPress}
            leftIcon={<AddIcon fill={colors.green} />}
          >
            {buttonText}
          </Button>
        )}
      </View>
    );
  },
);

const styles = StyleSheet.create({
  text: {
    flex: 1,
    justifyContent: 'center',
  },
});
