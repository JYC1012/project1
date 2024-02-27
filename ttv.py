import os
import sys
from gtts import gTTS
import argparse
import subprocess
import pdb
# # 获取当前脚本的绝对路径
# script_path = os.path.abspath(__file__)

# # 获取当前脚本所在的目录
# script_directory = os.path.dirname(script_path)

# # 设置当前工作目录为脚本所在的目录
# os.chdir(script_directory)

# # 现在当前工作目录已经更改为脚本所在的目录，你可以在这里执行其他操作

# print(f"当前工作目录已设置为: {os.getcwd()}")

def text_to_speech(text, target_path):
    # Initialize gTTS with the text to convert
    speech = gTTS(text, lang="en", slow=False, tld='com.au')
    print("1")

    # Save the audio file to a temporary file
    speech.save(target_path)
    print("2")

def run_inference1_command(checkpoint_path, face_path, audio_path, outfile):
    command = f"python inference.py --checkpoint_path {checkpoint_path} --face {face_path} --audio {audio_path} --outfile {outfile}"
    
    try:
        subprocess.run(command, shell=True, check=True)
        print("命令执行成功！")
    except subprocess.CalledProcessError as e:
        print(f"命令执行失败，错误信息：{e}")

def video2images(input_video, output_images):
    command = f"ffmpeg -i {input_video} -vf \"select='gte(n\\,0)'\" -vsync 0 {output_images}"

    try:
        subprocess.run(command, shell=True, check=True)
        print("命令执行成功！")
    except subprocess.CalledProcessError as e:
        print(f"命令执行失败，错误信息：{e}")

def images2video(input_images, imput_wav, output_video):
    command = f"ffmpeg -y -framerate 25 -i {input_images} -i {imput_wav} -c:v libx264 -c:a aac -pix_fmt yuv420p -shortest {output_video}"

    try:
        subprocess.run(command, shell=True, check=True)
        print("命令执行成功！")
    except subprocess.CalledProcessError as e:
        print(f"命令执行失败，错误信息：{e}")

def run_inference2_command(imgs_path, out_img_path, version, upscale):
    # command = f"python inference.py --checkpoint_path {checkpoint_path} --face {face_path} --audio {audio_path} --outfile {outfile}"
    command = f"python inference_gfpgan.py -i {imgs_path} -o {out_img_path} -v {version} -s {upscale}"
    try:
        subprocess.run(command, shell=True, check=True)
        print("命令执行成功！")
    except subprocess.CalledProcessError as e:
        print(f"命令执行失败，错误信息：{e}")

if __name__ == '__main__':

    # 获取命令行参数，第一个参数是脚本名称，后面的参数是传递给脚本的文本或文本文件的路径
    
    parser = argparse.ArgumentParser(description='Convert text to speech using gTTS.')
    parser.add_argument('--text', type=str, help='Text to convert to speech')
    parser.add_argument('--output_audio', type=str, default='/data2/jingyc/project1/Wav2Lip/audio/converted_audio.mp3', help='Output path for the audio file')
    parser.add_argument('--checkpoint_path', type=str, default='/data2/jingyc/project1/Wav2Lip/checkpoints/wav2lip.pth', help='checkpoint path for model')
    parser.add_argument("--face_path", type=str, default='/data2/jingyc/project1/Wav2Lip/video/woman_cut.mp4', help="face path")
    parser.add_argument('--outfile', type=str, help='Video path to save result. See default for an e.g.', 
								default='results/result_voice.mp4')
    parser.add_argument(        
        '-i',
        '--input',
        type=str,
        default='inputs/whole_imgs',
        help='Input image or folder. Default: inputs/whole_imgs')
    parser.add_argument('-o', '--output', type=str, default='results', help='Output folder. Default: results')    
    parser.add_argument(
        '-v', '--version', type=str, default='1.3', help='GFPGAN model version. Option: 1 | 1.2 | 1.3. Default: 1.3')
    parser.add_argument(
        '-s', '--upscale', type=int, default=2, help='The final upsampling scale of the image. Default: 2')
    
    args = parser.parse_args()
    # checkpoint_path = "./checkpoints/wav2lip.pth"
    # face_path = "./video/man_cut.mp4"
    audio_path = args.output_audio
    # pdb.set_trace()



    if not args.text:
        print("请提供要转换为语音的文本或文本文件的路径参数。")
    else:
        # # 设置当前工作目录为脚本所在的目录
        # script_path = os.path.abspath(__file__)
        # script_directory = os.path.dirname(script_path)
        # os.chdir(script_directory)

        # print(f"当前工作目录已设置为: {os.getcwd()}")

        wav2lip_path = '/data2/jingyc/project1/Wav2Lip'
        os.chdir(wav2lip_path)
        current_directory = os.getcwd()
        print("当前工作目录:", current_directory)
        # target_path = "./audio/converted_audio.mp3"


        # 如果 text_argument 是一个文件路径，则读取文件内容
        if os.path.isfile(args.text):
            with open(args.text, 'r', encoding='utf-8') as file:
                text_content = file.read()
            text_to_speech(text_content, args.output_audio)
            print(f"文本文件 '{args.text}' 中的内容已转换为语音并保存到 '{args.output_audio}'。")
            print("生成视频:")
            # run_inference1_command(args.checkpoint_path, args.face_path, audio_path, args.outfile)
            print(f"语音 '{args.output_audio}'已驱动并生成视频，保存到 '{args.outfile}'")
        else:
            # 否则，假定 text_argument 是文本内容，直接调用 text_to_speech 函数
            text_to_speech(args.text, args.output_audio)
            print(f"文本 '{args.text}' 已转换为语音并保存到 '{args.output_audio}'。")
            print("生成视频:")
            # run_inference1_command(args.checkpoint_path, args.face_path, audio_path, args.outfile)
            print(f"语音 '{args.output_audio}'已驱动并生成视频，保存到 '{args.outfile}'")

        video = args.outfile
        directory_path, filename = os.path.split(args.outfile)
        filename_without_extension, extension = os.path.splitext(filename)
        gfpgan_path = '/data2/jingyc/project1/GFPGAN'
        whole_images = os.path.join(gfpgan_path, 'inputs/whole_imgs', filename_without_extension)
        # print(whole_images)
        if not os.path.exists(whole_images):
            os.makedirs(whole_images)
            print(f"目录 {whole_images} 创建成功。")
        # run_ffmpeg_command(video, output_images)
        output_images = os.path.join(whole_images, 'output_%04d.png')
        # video2images(video, output_images)
        
        #准备超分
        os.chdir(gfpgan_path)
        current_directory = os.getcwd()
        print("当前工作目录:", current_directory)
        #新建输出帧的目录
        out_img_path = os.path.join(gfpgan_path, args.output, filename_without_extension )
        if not os.path.exists(out_img_path):
            os.makedirs(out_img_path)
            print(f"目录 {out_img_path} 创建成功。")

        # 进行超分
        run_inference2_command(whole_images, out_img_path, args.version, args.upscale)
        after_FR_images = os.path.join(out_img_path, 'restored_imgs', 'output_%04d.png')
        output_video_path = os.path.join(out_img_path, 'output_video.mp4')

        #帧转视频
        images2video(after_FR_images, audio_path, output_video_path)
        print(output_video_path)
        print('运行结束')
        



        
        

    
