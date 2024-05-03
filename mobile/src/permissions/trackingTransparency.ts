import { Platform } from 'react-native';

import { PERMISSIONS, RESULTS, check, request } from 'react-native-permissions';

const requestTrackingPermission = async () => {
  if (Platform.OS === 'ios') {
    const result = await request(PERMISSIONS.IOS.APP_TRACKING_TRANSPARENCY);
    if (result === RESULTS.GRANTED) {
      console.log('Tracking permission granted.');
    } else {
      console.log('Tracking permission denied.');
    }
  }
};

export const checkTrackingPermission = async () => {
  if (Platform.OS === 'ios') {
    const result = await check(PERMISSIONS.IOS.APP_TRACKING_TRANSPARENCY);
    switch (result) {
      case RESULTS.UNAVAILABLE:
        console.log(
          'This feature is not available (on this device / in this context)',
        );
        break;
      case RESULTS.DENIED:
        console.log(
          'The permission has not been requested / is denied but requestable',
        );
        requestTrackingPermission(); // Optionally request permission here
        break;
      case RESULTS.LIMITED:
        console.log('The permission is limited: some actions are possible');
        break;
      case RESULTS.GRANTED:
        console.log('The permission is granted');
        break;
      case RESULTS.BLOCKED:
        console.log('The permission is denied and not requestable anymore');
        break;
    }
  }
};
