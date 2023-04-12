import React from 'react';
import { View, Text, StyleSheet } from 'react-native';
import { TouchableOpacity } from 'react-native-gesture-handler';
import ArrowRightIcon from 'src/assets/icons/arrow-right'

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
    backgroundColor: '#FFFFFF33',
    width: '100%',
    height: '45%',
    borderRadius: 12,
    marginVertical: 10,
  },

  line: {
    backgroundColor: '#B8FF5F',
    height: '80%',
    flex: 0.008,
    borderRadius: 10,
  },

  userInfo: {
    flex: 0.8,
    height: '60%',
    flexDirection: 'row',
    marginLeft: '5%',
    borderRadius: 10,
  },

  lastName: {
    fontSize: 17,
    color: 'white',
    marginLeft: 5,
    alignSelf: 'flex-end',
  },

  firstName: {
    fontSize: 17,
    color: 'white',
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
