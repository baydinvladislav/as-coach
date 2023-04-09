import React from 'react';
import { StyleSheet, View } from 'react-native';

import { AddIcon } from '@assets';
import { t } from '@i18n';
import { Screens, useNavigation } from '@navigation';
import { colors, normVert } from '@theme';
import { Button, Text } from '@ui';

import { ButtonType, FontSize } from '~types';

type TProps = {
  title: string;
  description: string;
  buttonText: string;
  onPress: () => void;
};

export const LkEmpty = ({
  title,
  description,
  buttonText,
  onPress,
}: TProps) => {
  const { navigate } = useNavigation();
  return (
    <>
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
          style={{ lineHeight: 24 }}
          fontSize={FontSize.S17}
          color={colors.black4}
        >
          {description}
        </Text>
      </View>

      <Button
        type={ButtonType.TEXT}
        onPress={onPress}
        leftIcon={<AddIcon stroke={colors.green} />}
      >
        {buttonText}
      </Button>
    </>
  );
};

const styles = StyleSheet.create({
  text: { marginTop: normVert(213), marginBottom: normVert(24) },
});
