import React from 'react';
import { View, StyleSheet } from 'react-native';
import { TouchableOpacity } from 'react-native-gesture-handler';
import ArrowRightIcon from 'src/assets/icons/arrow-right'
import { normVert, normHor } from '@theme';
import { colors } from '@theme';
import { Text } from '@ui';

import { FontSize } from '~types';

type ClientCardProps = {
  firstName: string;
  lastName: string;
  onPress: () => void;
};

const ClientCard: React.FC<ClientCardProps> = ({ firstName, lastName, onPress }) => {
  return (
    <TouchableOpacity onPress={onPress} style={styles.card}>
      <View style={styles.line}></View>
      <View style={styles.userInfo}>
        <Text
          style={styles.lastName}
          color={colors.white}
          fontSize={FontSize.S17}
        >
          {lastName}
        </Text>
        <Text
          style={styles.firstName}
          color={colors.white}
          fontSize={FontSize.S17}
        >
          {firstName}
        </Text>
      </View>
      <View style={styles.arrowContainer}><ArrowRightIcon /></View>
    </TouchableOpacity>
  );
};


const styles = StyleSheet.create({
  card: {
    flexDirection: 'row',
    justifyContent: 'flex-start',
    alignItems: 'center',
    backgroundColor: colors.grey5,
    width: normHor(343),
    height: normVert(84),
    borderRadius: 12,
    marginVertical: normVert(10),
  },

  line: {
    backgroundColor: colors.green,
    height: '80%',
    width: normHor(4),
    borderRadius: 10,
  },

  userInfo: {
    flex: 0.8,
    height: normVert(50),
    flexDirection: 'row',
    marginLeft: normVert(22),
    borderRadius: 10,
  },

  lastName: {
    alignSelf: 'flex-end',
  },

  firstName: {
    alignSelf: 'flex-end',
    marginLeft: normHor(4),
  },

  arrowContainer: {
    flexDirection: 'column',
    justifyContent: 'center',
    alignItems: 'flex-end',
    flex: 0.2,
    marginRight: normVert(32)
  },
});

export default ClientCard;
