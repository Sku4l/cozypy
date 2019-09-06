import unittest
from unittest import mock
from unittest.mock import patch

from requests import Session

from cozypy.client import CozytouchClient


def mock_response(status, content, json_data = False):
    mock_resp = mock.Mock()
    mock_resp.status_code = status
    mock_resp.content = content
    if json_data:
        mock_resp.json = mock.Mock(
            return_value=content
        )
    return mock_resp


setup_response = {
    "creationTime": 1541529744000,
    "lastUpdateTime": 1541529744000,
    "id": "SETUP-0812-9894-4518",
    "location": {
        "creationTime": 1541529744000,
        "lastUpdateTime": 1541529744000,
        "city": "Paris",
        "country": "Paris",
        "postalCode": "75000",
        "addressLine1": "Paris",
        "timezone": "Europe/Paris",
        "longitude": 2.343,
        "latitude": 47.939,
        "twilightMode": 2,
        "twilightAngle": "CIVIL",
        "twilightCity": "paris",
        "summerSolsticeDuskMinutes": 1290,
        "winterSolsticeDuskMinutes": 990,
        "twilightOffsetEnabled": False,
        "dawnOffset": 0,
        "duskOffset": 0
    },
    "devices": [
        {
            "creationTime": 1541532294000,
            "lastUpdateTime": 1541532294000,
            "label": "IO (19071767#3)",
            "deviceURL": "io://0832-9894-4518/10071767#2",
            "shortcut": False,
            "controllableName": "io:TemperatureInCelciusIOSystemDeviceSensor",
            "definition":{"commands":[], "states":[]},
            "states":[
                {"name": "core:StatusState", "type": 3, "value": "available" },
                {"name": "core:TemperatureState", "type": 2, "value": 14}
            ],
            "attributes":[],
            "available": True,
            "enabled": True,
            "placeOID": "aff4857b-18be-4201-b14c-d8233b439931",
            "widget": "TemperatureSensor",
            "type": 2,
            "oid": "ed053def-0e93-4a1f-9f52-9450afada98b",
            "uiClass": "TemperatureSensor"
        },
        {
            "creationTime": 1541532294000,
            "lastUpdateTime": 1541532294000,
            "label": "IO (19071767#2)",
            "deviceURL": "io://0832-9894-4518/10071767#2",
            "shortcut": False,
            "controllableName": "io:TemperatureInCelciusIOSystemDeviceSensor",
            "definition":{"commands":[], "states":[]},
            "states":[
                {"name": "core:StatusState", "type": 3, "value": "available" },
                {"name": "core:TemperatureState", "type": 2, "value": 20}
            ],
            "attributes":[],
            "available": True,
            "enabled": True,
            "placeOID": "aff4857b-18be-4201-b14c-d8233b439931",
            "widget": "TemperatureSensor",
            "type": 2,
            "oid": "fd053def-0e93-4a1f-9f52-9450afada98b",
            "uiClass": "TemperatureSensor"
        },
        {
            'creationTime': 1541532294000,
            'lastUpdateTime': 1541532294000,
            'label': 'I2G_Actuator',
            'deviceURL': 'io://0812-9894-4518/10071767#1',
            'shortcut': False,
            'controllableName': 'io:AtlanticElectricalHeaterWithAdjustableTemperatureSetpointIOComponent',
            'definition': {},
            'attributes': [],
            'available': True,
            'enabled': True,
            'placeOID': 'aff4857b-18be-4201-b14c-d8233b439931',
            'widget': 'AtlanticElectricalHeaterWithAdjustableTemperatureSetpoint',
            'type': 1,
            'oid': 'aff4857b-18be-4201-b14c-d8233b439931',
            'uiClass': 'HeatingSystem',
            'states':[
                {'name': 'core:ComfortRoomTemperatureState', 'type': 1, 'value': 20},
                {'name': 'core:EcoRoomTemperatureState', 'type': 1, 'value': 2},
                {'name': 'core:OnOffState', 'type': 3, 'value': 'off'}
            ]
        },
        {
            'creationTime': 1541532294000,
            'lastUpdateTime': 1541532294000,
            'label': 'I2G_Actuator',
            'deviceURL': 'io://0812-9894-4518/10071767#1',
            'shortcut': False,
            'controllableName': 'io:AtlanticElectricalHeaterWithAdjustableTemperatureSetpointIOComponent',
            'definition': {},
            'attributes': [],
            'available': True,
            'enabled': True,
            'placeOID': 'aff4857b-18be-4201-b14c-d8233b439931',
            'widget': 'AtlanticElectricalHeaterWithAdjustableTemperatureSetpoint',
            'type': 1,
            'oid': 'aff4857b-18be-4201-b14c-d8233b439931',
            'uiClass': 'HeatingSystem',
            'states':[
                {'name': 'core:ComfortRoomTemperatureState', 'type': 1, 'value': 20},
                {'name': 'core:EcoRoomTemperatureState', 'type': 1, 'value': 2},
                {'name': 'core:OnOffState', 'type': 3, 'value': 'on'}
            ]
        },
        {
            'creationTime': 1541532294000,
            'lastUpdateTime': 1541532294000,
            'label': 'I2G_Actuator',
            'deviceURL': 'io://0812-9894-4518/10071768#1',
            'shortcut': False,
            'controllableName': 'io:AtlanticElectricalHeaterWithAdjustableTemperatureSetpointIOComponent',
            'definition': {},
            'attributes': [],
            'available': True,
            'enabled': True,
            'placeOID': 'aff4857b-18be-4201-b14c-d8233b439931',
            'widget': 'AtlanticElectricalHeaterWithAdjustableTemperatureSetpoint',
            'type': 1,
            'oid': 'bff4857b-18be-4201-b14c-d8233b439931',
            'uiClass': 'HeatingSystem',
            'states':[
                {'name': 'core:ComfortRoomTemperatureState', 'type': 1, 'value': 20},
                {'name': 'core:EcoRoomTemperatureState', 'type': 1, 'value': 2},
                {'name': 'core:OnOffState', 'type': 3, 'value': 'on'}
            ]
        }
    ],
    "rootPlace": {
        "creationTime": 1541529744000,
        "lastUpdateTime": 1541529744000,
        "label": "All House",
        "type": 0,
        "oid": "aff4857b-18be-4201-b14c-d8233b439931",
        "subPlaces":[]
    }
}


class TestClient(unittest.TestCase):

    def test_setup(self):
        with patch.object(Session, 'post') as mock_post:
            mock_post.return_value = mock_response(200, {})
            client = CozytouchClient("test", "test")

            with patch.object(Session, 'get') as mock_get:
                mock_get.return_value = mock_response(200, setup_response, True)
                setup = client.get_setup()

                self.assertIsNotNone(setup)
                self.assertEqual(len(setup.places), 1)
                self.assertEqual(len(setup.heaters), 3)



if __name__ == '__main__':
    unittest.main()