import React from 'react';
import { StyleSheet } from 'react-native';

import { Sets } from '@components';
import { colors, normVert } from '@theme';
import { Checkbox } from '@ui';

import { TPropsExercises } from '~types';

type TProps = {
  isFirst: boolean;
  handlePress: () => void;
  placeholder: string;
  exercise?: TPropsExercises;
  errors: Record<string, any>;
  handleChangeSets: (e: React.ChangeEvent<any>) => void;
  index: number;
  isSelected?: boolean;
  onDrag?: () => void;
};

export const CheckboxWithSets = ({
  isFirst,
  handlePress,
  placeholder,
  exercise,
  errors,
  handleChangeSets,
  index,
  isSelected,
  onDrag,
}: TProps) => (
  <>
    <Checkbox
      style={[styles.checkbox, !isFirst && styles.border]}
      onChangeCheckbox={handlePress}
      placeholder={placeholder}
      value={isSelected !== undefined ? isSelected : Boolean(exercise)}
      onDrag={onDrag}
    />
    {exercise && (
      <Sets
        errors={errors?.exercises?.[index]?.sets}
        val={exercise?.sets}
        onChangeText={handleChangeSets}
      />
    )}
  </>
);

const styles = StyleSheet.create({
  checkbox: {
    paddingVertical: normVert(16),
  },
  border: {
    borderTopColor: colors.black3,
    borderTopWidth: 1,
  },
});
