import requests
import sys
import logging
import json
import paho.mqtt.client as mqtt

logger = logging.getLogger('uploader')
icaddata = {}
icaddata['icad_url'] = "http://tone-detector:8002/tone_detect"
def upload_to_icad(icad_data, mp3_path, call_data):
    r = None
    logger.info(f'Uploading To iCAD Tone Detect API: {str(icad_data["icad_url"])}')

    if not call_data:
        logger.critical(f'Failed Uploading To iCAD API: Empty JSON')
        return False

    try:
        with open(mp3_path, 'rb') as audio_file:
            files = {'file': audio_file}
            data = call_data
            r = requests.post(icad_data['icad_url'], files=files, data=data)
            r.raise_for_status()

            logger.info(f'Successfully uploaded to iCAD API: {r.status_code}, {r.text}')
            client = mqtt.Client()
            client.connect("mosquitto")
            logger.info(client.publish("trunkrecorder/tones",json.dumps(r.json())))
            
            client.disconnect()

    except requests.exceptions.RequestException as e:
        if r:
            logger.critical(f'Failed Uploading To iCAD API: {str(e)} {r.status_code} {r.text}')
        else:
            logger.critical(f'Failed Uploading To iCAD API: {str(e)}')
        return False
    except (FileNotFoundError, IOError) as e:
        logger.critical(f'Failed Uploading To iCAD API: {str(e)}')
        return False


    return True

def main():
    logging.basicConfig(level=logging.INFO, format='[%(asctime)s] - %(name)s - %(levelname)s - %(message)s')
    args = sys.argv
    filepath = args[4]
    system = args[1]
    json_path = args[3]
    logger.debug(f"System: {system} \t File: {filepath}")
    with open(json_path, 'r') as fj:
        call_data = json.load(fj)
    logger.info(call_data)
    r = upload_to_icad(icad_data=icaddata, mp3_path=filepath, call_data=call_data)

if __name__ == "__main__":
    main()
