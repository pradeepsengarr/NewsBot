import requests
import json
import time

class VideoGenerator:
    def __init__(self, api_key):
        self.api_key = api_key

    def generate_video(self, input_text, source_url):
        url = "https://api.d-id.com/talks"

        payload = {
            "script": {
                "type": "text",
                "subtitles": "false",
                "provider": {
                    "type": "microsoft",
                    "voice_id": "en-US-JennyNeural"
                },
                "ssml": "false",
                "input": input_text
            },
            "config": {
                "fluent": "false",
                "pad_audio": "0.0"
            },
            "source_url": source_url
        }

        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "authorization": f"Bearer {self.api_key}"
        }

        # Make the initial POST request to create the video
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code != 200:
            raise Exception(f"Failed to create video. Status code: {response.status_code}, Response: {response.text}")

        _response = response.json()
        print("Initial Response:", _response)

        if "id" not in _response:
            raise Exception("Response does not contain 'id' field.")

        talk_id = _response['id']
        talk_url = f"{url}/{talk_id}"

        # Polling for status until it's created
        while True:
            response = requests.get(talk_url, headers=headers)
            if response.status_code != 200:
                raise Exception(f"Failed to get video status. Status code: {response.status_code}, Response: {response.text}")
            _response = response.json()
            print("Polling Response:", _response)

            if "status" not in _response:
                raise Exception(f"Polling response does not contain 'status' field: {_response}")

            if _response["status"] == "created":
                break

            time.sleep(5)  # Wait for a few seconds before polling again

        # Polling for video processing to complete
        while True:
            response = requests.get(talk_url, headers=headers)
            if response.status_code != 200:
                raise Exception(f"Failed to get video status. Status code: {response.status_code}, Response: {response.text}")
            _response = response.json()
            print("Final Response:", _response)

            if "status" not in _response:
                raise Exception(f"Final response does not contain 'status' field: {_response}")

            if _response["status"] == "done":
                break

            time.sleep(5)  # Wait for a few seconds before polling again

        if "result_url" not in _response:
            raise Exception(f"Response does not contain 'result_url' field: {_response}")

        video_url = _response["result_url"]
        return video_url
