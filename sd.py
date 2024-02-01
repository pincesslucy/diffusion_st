import torch
from diffusers import DiffusionPipeline, StableDiffusionPipeline, AutoPipelineForText2Image, StableDiffusionImg2ImgPipeline
from diffusers import DPMSolverMultistepScheduler
import random
from PIL import Image
from diffusers import AutoencoderKL

import matplotlib.pyplot as plt

#생성 갯수
def get_inputs(prompt, batch_size=1):
    seed = random.randint(0,9999999)
    generator = [torch.Generator("cuda").manual_seed(seed+i) for i in range(batch_size)]
    prompts = batch_size * [prompt]
    num_inference_steps = 10

    return {"prompt": prompts, "generator": generator, "num_inference_steps": num_inference_steps}

def get_image(prompt, image, batch_size=1):
    seed = random.randint(0,9999999)
    generator = [torch.Generator("cuda").manual_seed(seed+i) for i in range(batch_size)]
    prompts = batch_size * [prompt]
    strength=0.7
    guidance_scale=8.5

    return {"prompt": prompts, "image": image, "generator": generator, "strength": strength, "guidance_scale": guidance_scale}

#프롬프트
def generate(prompt):
    prompt = prompt
    #추가 프롬프트
    prompt += "best quality, photorealistic, dramatic lighting, raw photo,  ultra realistic details, sharp focus"

    #모델 설정
    model_id = "Lykon/dreamshaper-xl-turbo"
    pipeline = AutoPipelineForText2Image.from_pretrained(model_id, torch_dtype=torch.float16, variant="fp16")

    #스케줄러 설정
    pipeline.scheduler = DPMSolverMultistepScheduler.from_config(pipeline.scheduler.config)

    # #vae설정
    # vae = DPMSolverMultistepScheduler.from_config(pipeline.scheduler.config)
    # pipeline.vae = vae

    #메모리 부족할 때
    # pipeline.enable_attention_slicing()

    pipeline = pipeline.to("cuda")

    image = pipeline(**get_inputs(prompt)).images[0]
    print(image)

    return image

def generate_i2i(prompt, image):
    prompt = prompt
    #추가 프롬프트
    prompt += "ghibli style, best quality, masterpiece"

    pipeline = StableDiffusionImg2ImgPipeline.from_pretrained("nitrosocke/Ghibli-Diffusion", torch_dtype=torch.float16)
    pipeline = pipeline.to("cuda")

    result = pipeline(**get_image(prompt, image)).images[0]
    print(result)

    return result

# #테스트
# if __name__ == "__main__":
#     prompt = "a painting of a cat"
#     image = generate(prompt)
#     plt.imshow(image)
#     plt.show()