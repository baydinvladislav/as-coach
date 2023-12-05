import messaging from '@react-native-firebase/messaging';

export async function requestUserPermission() {
    const authStatus = await messaging().requestPermission();
    const enabled = 
        authStatus === messaging.AuthorizationStatus.AUTHORIZED || 
        messaging.AuthorizationStatus.PROVISIONAL;

    if (enabled) {
        console.log('Authorization status:', authStatus);
        getFcmToken()
    }
}


const getFcmToken = async () => {
    try {
        const fcmToken = await messaging().getToken()
        console.log('FCM token generated', fcmToken)
    } catch (error) {
        console.log('FCM token generated', error)
    }
}
