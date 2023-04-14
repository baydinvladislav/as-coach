import React from 'react';
import { View, Text, StyleSheet } from 'react-native';
import { TouchableOpacity } from 'react-native-gesture-handler';
import ArrowRightIcon from 'src/assets/icons/arrow-right'
import { normVert, normHor } from '@theme';
import { colors } from '@theme';

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
        <Text style={styles.lastName}>{lastName}</Text>
        <Text style={styles.firstName}>{firstName}</Text>
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
    borderWidth: 1,
    borderColor: 'white',
    flexDirection: 'row',
    marginLeft: '5%',
    borderRadius: 10,
  },

  lastName: {
    fontSize: 17,
    color: colors.white,
    marginLeft: 5,
    alignSelf: 'flex-end',
  },

  firstName: {
    fontSize: 17,
    color: colors.white,
    alignSelf: 'flex-end',
    marginLeft: 5,
  },

  arrowContainer: {
    flexDirection: 'row',
    justifyContent: 'center',
    alignItems: 'center',
    flex: 0.2,
    height: '60%',
  },
});

export default ClientCard;
