import os
import sys
from gtts import gTTS
import argparse
import subprocess
import pdb
import gradio as gr
from os.path import join as pjoin



def text_to_speech(text, target_path):
    # Initialize gTTS with the text to convert
    speech = gTTS(text, lang="zh-CN", slow=False, tld='com.au')
    print("1")

    # Save the audio file to a temporary file
    speech.save(target_path)
    print("2")

def run_inference1_command(checkpoint_path, face_path, audio_path, outfile, working_directory, gpu_id = 1):
    command = f"CUDA_VISIBLE_DEVICES={gpu_id} python inference.py --checkpoint_path {checkpoint_path} --face {face_path} --audio {audio_path} --outfile {outfile}"
    
    try:
        subprocess.run(command, shell=True, check=True, cwd=working_directory)
        print("命令执行成功！")
    except subprocess.CalledProcessError as e:
        print(f"命令执行失败，错误信息：{e}")

def video2images(input_video, output_images, gpu_id = 1):
    command = f"CUDA_VISIBLE_DEVICES={gpu_id} ffmpeg -i {input_video} -vf \"select='gte(n\\,0)'\" -vsync 0 {output_images}"

    try:
        subprocess.run(command, shell=True, check=True)
        print("命令执行成功！")
    except subprocess.CalledProcessError as e:
        print(f"命令执行失败，错误信息：{e}")

def images2video(input_images, imput_wav, output_video, gpu_id = 1):
    command = f"CUDA_VISIBLE_DEVICES={gpu_id} ffmpeg -y -framerate 25 -i {input_images} -i {imput_wav} -c:v libx264 -c:a aac -pix_fmt yuv420p -shortest {output_video}"

    try:
        subprocess.run(command, shell=True, check=True)
        print("命令执行成功！")
    except subprocess.CalledProcessError as e:
        print(f"命令执行失败，错误信息：{e}")

def run_inference2_command(imgs_path, out_img_path, version, upscale, working_directory, gpu_id = 1):
    # command = f"python inference.py --checkpoint_path {checkpoint_path} --face {face_path} --audio {audio_path} --outfile {outfile}"
    command = f"CUDA_VISIBLE_DEVICES={gpu_id} python inference_gfpgan.py -i {imgs_path} -o {out_img_path} -v {version} -s {upscale}"
    try:
        subprocess.run(command, shell=True, check=True, cwd=working_directory)
        print("命令执行成功！")
    except subprocess.CalledProcessError as e:
        print(f"命令执行失败，错误信息：{e}")

