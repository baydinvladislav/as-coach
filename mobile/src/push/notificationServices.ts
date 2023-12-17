import AsyncStorage from '@react-native-async-storage/async-storage';
import messaging from '@react-native-firebase/messaging';

export async function requestUserPermission() {
  const authStatus = await messaging().requestPermission();
  const enabled =
    authStatus === messaging.AuthorizationStatus.AUTHORIZED ||
    messaging.AuthorizationStatus.PROVISIONAL;

  if (enabled) {
    console.log('authorization.success.status:', authStatus);
    await getFcmToken();
  } else {
    console.log('could.not.authorization.device:', authStatus);
  }
}

export const getFcmToken = async () => {
  let fcmToken = await AsyncStorage.getItem('fcmToken');
  if (!fcmToken) {
    try {
      fcmToken = await messaging().getToken();
      if (fcmToken) {
        console.log('new.fcm.token.generated', fcmToken);
        await AsyncStorage.setItem('fcmToken', fcmToken);
      }
    } catch (error) {
      console.log('error.during.token.generation', error);
    }
  } else {
    console.log('use.old.token', fcmToken);
  }

  return fcmToken;
};

export const notificationListener = async () => {
  // listener for launching the application in the background
  messaging().onNotificationOpenedApp(remoteMessage => {
    console.log('background state message', remoteMessage.notification);
  });

  messaging()
    .getInitialNotification()
    .then(remoteMessage => {
      // check if the app was opened due to a notification
      if (remoteMessage) {
        console.log('remote message', remoteMessage.notification);
      }
    });
};
