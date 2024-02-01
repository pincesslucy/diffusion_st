import torch
from diffusers import DiffusionPipeline
from diffusers import DPMSolverMultistepScheduler
import random
from PIL import Image
from diffusers import AutoencoderKL



#생성 갯수
def get_inputs(prompt, batch_size=1):
    seed = random.randint(0,9999999)
    generator = [torch.Generator("cuda").manual_seed(seed+i) for i in range(batch_size)]
    prompts = batch_size * [prompt]
    num_inference_steps = 10

    return {"prompt": prompts, "generator": generator, "num_inference_steps": num_inference_steps}

#시각화
def image_grid(imgs, rows=1, cols=1):
    w, h = imgs[0].size
    grid = Image.new("RGB", size=(cols * w, rows * h))

    for i, img in enumerate(imgs):
        grid.paste(img, box=(i % cols * w, i // cols * h))
    return grid

#프롬프트
def generate(prompt):
    prompt = prompt
    #추가 프롬프트
    prompt += "best quality, photorealistic, dramatic lighting, raw photo,  ultra realistic details, sharp focus"

    #모델 설정
    model_id = "runwayml/stable-diffusion-v1-5"
    pipeline = DiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float32, safety_checker=None)

    #스케줄러 설정
    pipeline.scheduler = DPMSolverMultistepScheduler.from_config(pipeline.scheduler.config)

    #vae설정
    vae = AutoencoderKL.from_pretrained("stabilityai/sd-vae-ft-mse", torch_dtype=torch.float32).to("cuda")
    pipeline.vae = vae

    #메모리 부족할 때
    pipeline.enable_attention_slicing()

    pipeline = pipeline.to("cuda")

    image = pipeline(**get_inputs(prompt)).images
    print(image)
    image = image_grid(image)

    return image

#테스트
if __name__ == "__main__":
    prompt = "a painting of a cat"
    generate(prompt)