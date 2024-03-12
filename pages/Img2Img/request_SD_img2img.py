import requests


class ControlnetRequest:
    def __init__(self, b64img, prompt, neg_prompt,selected_room_type = "Kitchen", selected_room_style = "Classic", url="http://localhost:7860"):
        print(f'<lora:{selected_room_type}{selected_room_style}:1>')
        self.url = url + "/sdapi/v1/img2img"
        self.url_opt = url + "/sdapi/v1/options"
        self.body = {
            "init_images": [b64img],
            "prompt": prompt + f"Amazing, {selected_room_style}, {selected_room_type} Cozy, Light, Tranquility, Cleanliness, Natural materials, Plants, Functionality, Minimalism, Comfortable, Coziness,  <lora:{selected_room_type}{selected_room_style}:1>",
            "negative_prompt": neg_prompt + f"Too far, Minimalism, Cold, Uninspiring, Unrealistic, Photorealistic, Lack of warmth, Lack of coziness, Absence of decor, Lacking brightness, Uncomfortable, Impersonal",
            "batch_size": 1,
            "steps": 100,
            "cfg_scale": 7,
            "alwayson_scripts": {
                "controlnet": {
                    "args": [
                        {
                            "input_image": b64img,
                            "input_image": b64img,
                            "module": "canny",
                            "model": "control_v11p_sd15_canny [d14c016b]",
                            "control_mode": "My prompt is more important",
                            "weight": 1,
                        }
                    ]
                }
            }   
        }

    def send_request(self):
        opt = requests.get(url=self.url_opt)
        opt_json = opt.json()
        opt_json['sd_model_checkpoint'] = "Deliberate_v5.safetensors [636fe404e3]"
        print(requests.post(url=self.url_opt, json=opt_json))
        r = requests.post(self.url, json=self.body)
        return r.json()
