import React, { useState } from 'react';
import { StyleSheet, TouchableOpacity, View } from 'react-native';

import { CrossIcon, SearchIcon } from '@assets';
import { t } from '@i18n';
import { normHor } from '@theme';
import { Button, Input, TInputProps } from '@ui';

import { ButtonType } from '~types';

export const SearchInput = (props: TInputProps) => {
  const [key, setKey] = useState(0);
  const [isFocused, setIsFocused] = useState(false);

  const handleFocus = () => {
    setIsFocused(() => true);
  };

  const handleBlur = () => {
    setIsFocused(() => false);
  };

  const handleChangeText = (text: string) => {
    props?.onChangeText?.(text);
  };

  return (
    <View style={styles.container}>
      <Input
        {...props}
        key={key}
        onChangeText={handleChangeText}
        onFocus={handleFocus}
        onBlur={handleBlur}
        width={isFocused ? `${normHor(245)}px` : undefined}
        leftIcon={<SearchIcon />}
        rightIcon={
          isFocused ? (
            <TouchableOpacity onPress={() => handleChangeText('')}>
              <CrossIcon />
            </TouchableOpacity>
          ) : undefined
        }
      />
      {isFocused && (
        <Button
          type={ButtonType.TEXT}
          onPress={() => {
            handleBlur();
            handleChangeText('');
            setKey(key => key + 1);
          }}
        >
          {t('buttons.cancel')}
        </Button>
      )}
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
  },
});
