import React from 'react';
import { StyleSheet, View } from 'react-native';

import styled from 'styled-components';

import { colors, normVert } from '@theme';

import { FontSize } from '~types';

import { Text } from './text';

type TProps = {
  title: string;
  cells: { title: string; value: string }[];
};

export const RowBorder = ({ title, cells }: TProps) => (
  <View style={styles.rowBorder}>
    <Text color={colors.white} style={styles.title} fontSize={FontSize.S24}>
      {title}
    </Text>
    <Row>
      {cells.map((cell, key) => (
        <React.Fragment key={key}>
          <Cell count={cells.length}>
            <Text
              style={styles.cellTitle}
              color={colors.grey9}
              fontSize={FontSize.S12}
            >
              {cell.title}
            </Text>
            <Text
              style={styles.cellValue}
              color={colors.white}
              fontSize={FontSize.S16}
            >
              {cell.value}
            </Text>
          </Cell>
          {key !== cells.length - 1 && <Line />}
        </React.Fragment>
      ))}
    </Row>
  </View>
);

const styles = StyleSheet.create({
  title: {
    marginBottom: normVert(19),
  },
  cellTitle: {
    textAlign: 'center',
    textTransform: 'lowercase',
    marginBottom: normVert(6),
  },
  cellValue: {
    textAlign: 'center',
  },
  rowBorder: {
    marginBottom: normVert(44),
  },
});

const Cell = styled(View)<{ count: number }>`
  width: ${({ count }) => (count === 1 ? 100 : count === 2 ? 50 : 33.3)}%;
`;

const Row = styled(View)`
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: center;
`;

const Line = styled(View)`
  height: ${normVert(34)}px;
  width: 1px;
  background-color: ${colors.green};
`;
