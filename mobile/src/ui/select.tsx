import React, { useState } from 'react';
import { StyleSheet, View } from 'react-native';

import SelectDropdown from 'react-native-select-dropdown';
import styled from 'styled-components';

import { ArrowDownIcon } from '@assets';
import { colors, normHor, normVert } from '@theme';

import { FontSize } from '~types';

import { TInputProps } from './input';
import { Placeholder } from './placeholder';
import { Text } from './text';

type TProps = TInputProps & {
  data: { keys: string[]; values: string[] };
};

export const Select = ({ placeholder, style, ...props }: TProps) => {
  const [selected, setSelected] = useState<string | undefined>(props.value);

  const data = {
    keys: ['Не выбрано', ...props.data.keys],
    values: ['', ...props.data.values],
  };

  return (
    <View>
      {placeholder && <Placeholder isActive={!!selected} text={placeholder} />}
      <SelectDropdown
        data={data.keys}
        onSelect={(selectedItem, index) => {
          data.values[index]
            ? setSelected(selectedItem)
            : setSelected(undefined);
          data.values[index]
            ? props.onChangeText?.(data.values[index])
            : props.onChangeText?.('');
        }}
        defaultValueByIndex={data.values.findIndex(
          value => value === props?.value,
        )}
        defaultButtonText={' '}
        buttonTextAfterSelection={(selectedItem, key) => {
          if (key === 0) return '';
          return selectedItem;
        }}
        renderDropdownIcon={() => <ArrowDownIcon />}
        renderCustomizedRowChild={(selectedItem, key, isSelect) => (
          <RowContainer isLast={key === data.keys.length}>
            <Row
              selected={isSelect}
              color={colors.white}
              fontSize={FontSize.S17}
            >
              {selectedItem}
            </Row>
          </RowContainer>
        )}
        buttonStyle={[styles.input, style]}
        defaultValue={''}
        buttonTextStyle={styles.text}
        dropdownStyle={styles.dropdown}
        selectedRowTextStyle={styles.selectedText}
        rowStyle={styles.row}
        dropdownOverlayColor={colors.transparent}
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
    marginTop: normVert(6),
    backgroundColor: colors.black6,
    borderRadius: 14,
  },
  selectedText: {
    color: colors.green,
  },
  row: {
    borderBottomColor: colors.transparent,
    borderBottomWidth: 0,
    height: normVert(56),
  },
});

const Row = styled(Text)<{ selected?: boolean }>`
  margin-left: auto;
  margin-right: auto;

  ${({ selected }) => selected && `color: ${colors.green}`}
`;

const RowContainer = styled(View)<{ isLast: boolean }>`
  width: 100%;
  height: 100%;

  align-items: center;
  justify-content: center;

  border-bottom-style: solid;
  border-bottom-color: ${colors.grey6};
  border-bottom-width: ${({ isLast }) => (isLast ? 0 : 1)}px;
`;
