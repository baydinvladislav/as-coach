import React, { useState } from 'react';
import { StyleSheet, View } from 'react-native';

import SelectDropdown from 'react-native-select-dropdown';

import { ArrowDownIcon } from '@assets';
import { colors, normHor, normVert } from '@theme';
import { Placeholder, TInputProps } from '@ui';

type TProps = TInputProps & {
  data: { keys: string[]; values: string[] };
};

export const Select = ({ placeholder, style, data, ...props }: TProps) => {
  const [selected, setSelected] = useState<string | undefined>(props.value);

  return (
    <View>
      {placeholder && <Placeholder isActive={!!selected} text={placeholder} />}
      <SelectDropdown
        data={data.keys}
        onSelect={(selectedItem, index) => {
          setSelected(selectedItem);
          props.onChangeText?.(data.values[index]);
        }}
        defaultValueByIndex={data.values.findIndex(
          value => value === props?.value,
        )}
        defaultButtonText={' '}
        buttonTextAfterSelection={selectedItem => selectedItem}
        renderDropdownIcon={() => <ArrowDownIcon />}
        buttonStyle={[styles.input, style]}
        defaultValue={''}
        buttonTextStyle={styles.text}
        dropdownStyle={styles.dropdown}
        rowTextStyle={styles.dropdownText}
        rowStyle={styles.row}
      />
    </View>
  );
};

const styles = StyleSheet.create({
  input: {
    backgroundColor: colors.black3,
    textAlign: 'left',
    paddingHorizontal: normHor(10),
    width: '100%',
    borderRadius: 12,
  },
  text: {
    color: colors.white,
    textAlign: 'left',
    fontSize: 16,
    paddingTop: normVert(18),
  },
  dropdown: {
    backgroundColor: colors.black2,
  },
  dropdownText: {
    color: colors.white,
    fontSize: 16,
  },
  row: { borderBottomColor: colors.transparent, borderBottomWidth: 0 },
});
