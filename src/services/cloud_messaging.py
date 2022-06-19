from firebase_admin import messaging


def sendPushForTokens(
    title,
    body,
    tokens,
    data=None,
):
    message = messaging.MulticastMessage(
        notification=messaging.Notification(
            title=title,
            body=body,
        ),
        data=data,
        tokens=tokens,
    )
    messaging.send_multicast(message)
