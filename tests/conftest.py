from pytest import fixture


@fixture
def lock_json():
    return {
        "CAT": "01234",
        "SAT": "98765",
        "attributes": {
            "CAT": "01234",
            "SAT": "98765",
            "accessCodeLength": 4,
            "actAlarmBuzzerEnabled": 0,
            "actAlarmState": 0,
            "actuationCurrentMax": 226,
            "alarmSelection": 0,
            "alarmSensitivity": 0,
            "alarmState": 0,
            "autoLockTime": 0,
            "batteryChangeDate": 1669017530,
            "batteryLevel": 95,
            "batteryLowState": 0,
            "batterySaverConfig": {
                "activePeriod": [],
                "enabled": 0,
            },
            "batterySaverState": 0,
            "beeperEnabled": 1,
            "bleFirmwareVersion": "0118.000103.015",
            "diagnostics": {},
            "firmwareUpdate": {
                "status": {"additionalInfo": None, "updateStatus": None}
            },
            "homePosCurrentMax": 153,
            "keypadFirmwareVersion": "03.00.00250052",
            "lockAndLeaveEnabled": 1,
            "lockState": 1,
            "lockStateMetadata": {
                "UUID": None,
                "actionType": "periodicDeepQuery",
                "clientId": None,
                "name": None,
            },
            "macAddress": "AA:BB:CC:00:11:22",
            "mainFirmwareVersion": "10.00.00264232",
            "mode": 2,
            "modelName": "__model_name__",
            "periodicDeepQueryTimeSetting": 60,
            "psPollEnabled": 1,
            "serialNumber": "d34db33f",
            "timezone": -20,
            "wifiFirmwareVersion": "03.15.00.01",
            "wifiRssi": -42,
        },
        "connected": True,
        "connectivityUpdated": "2022-12-04T20:58:22.000Z",
        "created": "2020-04-05T21:53:11.000Z",
        "deviceId": "__device_uuid__",
        "devicetypeId": "be489wifi",
        "lastUpdated": "2022-12-04T20:58:22.000Z",
        "macAddress": "AA:BB:CC:00:11:22",
        "modelName": "__model_name__",
        "name": "Door Lock",
        "physicalId": "serial-number",
        "relatedDevices": [],
        "role": "owner",
        "serialNumber": "serial-number",
        "timezone": -20,
        "users": [
            {
                "email": "asdf@asdf.com",
                "friendlyName": "asdf",
                "identityId": "user-uuid",
                "role": "owner",
            }
        ],
    }


@fixture
def access_code_json():
    return {
        "accessCode": 123,
        "accesscodeId": "__access_code_uuid__",
        "activationSecs": 0,
        "disabled": 0,
        "expirationSecs": 4294967295,
        "friendlyName": "Friendly name",
        "notification": 0,
        "schedule1": {
            "daysOfWeek": "7F",
            "endHour": 23,
            "endMinute": 59,
            "startHour": 0,
            "startMinute": 0,
        },
    }
