{
    "ver": 2,
    "captureDir": "/app/capture",
    "logFile": true,
    "logDir": "/app/logs",
    "logLevel": "debug",
    "sources": [
        {
            "center": 935834375,
            "rate": 2048000,
            "error": 0,
            "gain": 40.2,
            "debugRecorders": 0,
            "digitalRecoders": 4,
            "driver": "osmosdr",
            "device": "rtl=0"
        }
    ],
    "systems": [
        {
            "shortName": "ICE",
            "type": "DMR",
            "control_channels": [
                935812500, 
                935837500,
                935862500
            ],
            "audioArchive": true,
            "callLog": true,
            "squelch": -27,
            "decodeMDC": true,
            "enabled": true
        }
    ],
    "plugins": [
        {
            "name": "rdioscanner_uploader",
            "library": "librdioscanner_uploader.so",
            "server": "http://rdio-scanner:3000",
            "systems": [
                {
                    "shortName": "ICE",
                    "apiKey": "b11b1880-471b-4550-b8d7-84bdf2a3a0eb",
                    "systemId": 99
                }
            ]
        },
        {
            "name": "MQTTStatus",
            "library": "libmqtt_status_plugin.so",
            "broker": "tcp://mosquitto:1883",
            "topic": "trunkrecorder/status",
            "message_topic": "trunkrecorder/msg",
            "unit_topic": "trunkrecorder/unit",
            "username": "trunkrecorder",
            "password": "TrunkRecorder",
            "console_logs": false
        }
    ]
}
