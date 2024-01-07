import requests


class ControlnetRequest:
    def __init__(self, b64img, prompt, neg_prompt, url="http://localhost:7860"):
        self.url = url + "/sdapi/v1/img2img"
        self.body = {
    "init_images": [b64img],
    "prompt": prompt,
    "negative_prompt": neg_prompt,
    "batch_size": 1,
    "steps": 20,
    "cfg_scale": 7,
    "alwayson_scripts": {
        "controlnet": {
            "args": [
                {
                    "input_image": b64img,
                    "module": "canny",
                    "model": "control_v11p_sd15_canny [d14c016b]",
                }
            ]
        }
    }
}

    def send_request(self):
        r = requests.post(self.url, json=self.body)
        return r.json()
