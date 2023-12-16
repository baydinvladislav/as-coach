import messaging from '@react-native-firebase/messaging';
import AsyncStorage from '@react-native-async-storage/async-storage';

export async function requestUserPermission() {
    const authStatus = await messaging().requestPermission();
    const enabled =
        authStatus === messaging.AuthorizationStatus.AUTHORIZED ||
        messaging.AuthorizationStatus.PROVISIONAL;

    if (enabled) {
        console.log('authorization.status:', authStatus);
        getFcmToken()
    }
}


export const getFcmToken = async () => {
    let fcmToken = await AsyncStorage.getItem('fcmToken')
    if (!fcmToken) {
        try {
            fcmToken = await messaging().getToken()
            if (!!fcmToken) {
                console.log('fcm.token.generated', fcmToken)
                await AsyncStorage.setItem('fcmToken', fcmToken)
            }
        } catch (error) {
            console.log('eror.during.token.generation', error)
        }
    } else {
        console.log('use.old.token', fcmToken)
    }

    return fcmToken;
}


export const notificationListener = async () => {
    messaging().onNotificationOpenedApp(remoteMessage => {
        console.log(
            'Notification caused app to open from background state:',
            remoteMessage.notification,
        );
        console.log('background state', remoteMessage.notification)
    });

    // Check whether an initial notification is available
    messaging()
        .getInitialNotification()
        .then(remoteMessage => {
            if (remoteMessage) {
                console.log(
                    'Notification caused app to open from quit state:',
                    remoteMessage.notification,
                );
                console.log('remote message', remoteMessage.notification)
            }
        });
}
