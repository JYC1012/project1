import os
import sys
from gtts import gTTS
import argparse
import subprocess
import pdb
import gradio as gr
from os.path import join as pjoin
from fun import *
import random
import shutil
from functools import partial

WEBSITE = """
<div class="embed_hidden">
<h1 style='text-align: center'> Text to Video </h1>
<h2 style='text-align: center'>
<nobr>输入文本生成视频</nobr>
</h2>
<h3> Description </h3>
<p>
🔥🔥🔥 该页面是数字人生成模型的交互式展示, 是一种从文本到说话人视频的方法!!! 它会根据您输入的文本生成特定的说话人视频。 🔥🔥🔥
</p>
<p>
🚀🚀🚀 此外，我们提供了一个链接可以下载生成的说话人视频，格式为 <b>MP4</b> , 可以支持大多数播放器。!!! 🚀🚀🚀
</p>
<p>

</p>
</div>
"""
WEBSITE_bottom = """
<div class="embed_hidden">
<p>
We thanks <a href="https://huggingface.co/spaces/Mathux/TMR" target="_blank">TMR</a> for this cool space template.
</p>
</div>
"""

# <p>
# If you have any issues on this space or feature requests, we warmly welcome you to contact us through our <a href="https://github.com/EricGuo5513/momask-codes/issues" target="_blank">repository</a> or <a href="mailto:ymu3@ualberta.ca?subject =[MoMask]Feedback&body = Message">email</a>.
# </p>

# EXAMPLES = [
#    #例子，文本输入
#    "A person is running on a treadmill.", "The person takes 4 steps backwards.", 
#    "A person jumps up and then lands.", "The person was pushed but did not fall.", 
#    "The person does a salsa dance.", "A figure streches it hands and arms above its head.",
#    "This person kicks with his right leg then jabs several times.",
#    "A person stands for few seconds and picks up his arms and shakes them.",
#    "A person walks in a clockwise circle and stops where he began.",
#    "A man bends down and picks something up with his right hand.",
#    "A person walks with a limp, their left leg gets injured.",
#    "A person repeatedly blocks their face with their right arm.",
#    "The person holds his left foot with his left hand, puts his right foot up and left hand up too.",
#    "A person stands, crosses left leg in front of the right, lowering themselves until they are sitting, both hands on the floor before standing and uncrossing legs.",
#    "The man walked forward, spun right on one foot and walked back to his original position.",
#    "A man is walking forward then steps over an object then continues walking forward.",
# ]

EXAMPLES = [
   #例子，文本输入
   "给我播放一个动力火车唱的歌.", "我这个打字怎么全部都是拼音.", 
   "有谁知道我空间开头动画的音乐来自哪里，有下载地址吗?", "同学们大家好，我是校医院杨医生.", 

]

# css to make videos look nice
# var(--block-border-color); TODO
CSS = """
.generate_video {
    position: relative;
    margin-left: auto;
    margin-right: auto;
    box-shadow: var(--block-shadow);
    border-width: var(--block-border-width);
    border-color: #000000;
    border-radius: var(--block-radius);
    background: var(--block-background-fill);
    width: 25%;
    line-height: var(--line-sm);
}
}
"""
DEFAULT_TEXT = "输入想要生成的文本 "

if not os.path.exists("./data/stats"):
    os.makedirs("./data/stats")
    with open("./data/stats/Prompts.text", 'w') as f: #打开文件，保存提示
        pass

Total_Calls = 4730
def update_total_calls():
    global Total_Calls
    Total_Calls_offset = 4730 ## init number from visit, 01/07
    with open("./data/stats/Prompts.text", 'r') as f:
        Total_Calls = len(f.readlines()) + Total_Calls_offset
    print("Prompts Num:",Total_Calls)

cached_dir = './cached'
uid = 1822
out_video_path = pjoin(cached_dir, f'{uid}') #视频输出路径
os.makedirs(out_video_path, exist_ok=True)


#配置参数
#获取命令行参数，第一个参数是脚本名称，后面的参数是传递给脚本的文本或文本文件的路径

parser = argparse.ArgumentParser(description='Convert text to speech using gTTS.')
parser.add_argument('--text', type=str, help='Text to convert to speech')
parser.add_argument('--output_audio', type=str, default='/data2/jingyc/project1/Wav2Lip/audio/converted_audio.mp3', help='Output path for the audio file')
parser.add_argument('--checkpoint_path', type=str, default='/data2/jingyc/project1/Wav2Lip/checkpoints/wav2lip.pth', help='checkpoint path for model')
parser.add_argument("--face_path", type=str, default='/data2/jingyc/project1/Wav2Lip/video/woman_cut.mp4', help="face path")
parser.add_argument('--outfile', type=str, help='Video path to save result. See default for an e.g.', 
                            default='/data2/jingyc/project1/Wav2Lip/results/debug.mp4')
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

wav2lip_path = '/data2/jingyc/project1/Wav2Lip'
gfpgan_path = '/data2/jingyc/project1/GFPGAN'

#音频路径
audio_path = args.output_audio




# pdb.set_trace()
def generate(
        text, 
        uid = uid,
        repeat_times=1,
        # args = args,
):
    # 输入文本和视频，生成视频。
    print("11111")
    print(text)
    with open("/data2/jingyc/project1/data/stats/Prompts.text", 'a') as f:
        f.write(text+'\n')
    update_total_calls()
    text_list = []
    text_list.append(text)
    # captions = text_list
    datas = []
    # text = text

    for r in range(repeat_times):

        ruid = random.randrange(999999999)

        #文本转音频， 音频生成lip
        if not text:
            print("请提供要转换为语音的文本或文本文件的路径参数。")
        else:
            wav2lip_path = '/data2/jingyc/project1/Wav2Lip'
            # os.chdir(wav2lip_path)
            # current_directory = os.getcwd()
            # print("当前工作目录:", current_directory)
            # target_path = "./audio/converted_audio.mp3"

            args.outfile = pjoin('/data2/jingyc/project1/Wav2Lip/results/', "sample_repeat%d_%d.mp4"%(r, ruid) )
            # 如果 text_argument 是一个文件路径，则读取文件内容
            if os.path.isfile(text):
                with open(text, 'r', encoding='utf-8') as file:
                    text_content = file.read()
                text_to_speech(text_content, audio_path)
                print(f"文本文件 '{text}' 中的内容已转换为语音并保存到 '{audio_path}'。")
                print("生成视频:")
                run_inference1_command(args.checkpoint_path, args.face_path, audio_path, args.outfile, wav2lip_path)
                print(f"语音 '{audio_path}'已驱动并生成视频，保存到 '{args.outfile}'")
            else:
                # 否则，假定 text_argument 是文本内容，直接调用 text_to_speech 函数
                text_to_speech(text, audio_path)
                print(f"文本 '{text}' 已转换为语音并保存到 '{audio_path}'。")
                print("生成视频:")
                run_inference1_command(args.checkpoint_path, args.face_path, audio_path, args.outfile, wav2lip_path)
                print(f"语音 '{audio_path}'已驱动并生成视频，保存到 '{args.outfile}'")
        
        
        video = args.outfile
                
        # 针对上面生成的视频进行超分

        directory_path, filename = os.path.split(args.outfile)
        filename_without_extension, extension = os.path.splitext(filename)
        gfpgan_path = '/data2/jingyc/project1/GFPGAN'
        whole_images = os.path.join(gfpgan_path, 'inputs/whole_imgs', filename_without_extension)
        # print(whole_images)
        if not os.path.exists(whole_images):
            os.makedirs(whole_images)
            print(f"目录 {whole_images} 创建成功。")
        output_images = os.path.join(whole_images, 'output_%04d.png')
        #视频转帧
        video2images(video, output_images)

        #准备超分
        # os.chdir(gfpgan_path)
        # current_directory = os.getcwd()
        # print("当前工作目录:", current_directory)
        #新建输出帧的目录
        out_img_path = os.path.join(gfpgan_path, args.output, filename_without_extension )
        if not os.path.exists(out_img_path):
            os.makedirs(out_img_path)
            print(f"目录 {out_img_path} 创建成功。")

        # 进行超分
        print("进行超分")
        run_inference2_command(whole_images, out_img_path, args.version, args.upscale, gfpgan_path)
        after_FR_images = os.path.join(out_img_path, 'restored_imgs', 'output_%04d.png')
        output_video_path = os.path.join(out_img_path, 'output_video.mp4')

        #帧转视频
        images2video(after_FR_images, audio_path, output_video_path)
        print("超分后视频保存目录", output_video_path)
        data_path = pjoin(cached_dir,f'{uid}',"sample_repeat%d_%d.mp4"%(r, ruid))
        #复制到cached_dir中
        shutil.copy(output_video_path, data_path)
        data_unit = {
            "url": data_path
            }
        datas.append(data_unit)
    return datas


# run_inference1_command(args.checkpoint_path, args.face_path, audio_path, args.outfile, wav2lip_path)
# print(f"语音 '{audio_path}'已驱动并生成视频，保存到 '{args.outfile}'")
# 测试
# output_datas = []
# output_datas = generate("同学们大家好，我是校医院杨老师。")
# HTML component

def get_video_html(data, video_id, width=700, height=700):

    url = data["url"]  # mp4文件路径
    # class="wrap default svelte-gjihhp hide"
    # <div class="contour_video" style="position: absolute; padding: 10px;">
    # width="{width}" height="{height}"
    print(f'url:{url}')
    video_html = f"""
<h2 style='text-align: center'>
<a href="http://localhost:8866/{url}" download="video.mp4"><b>MP4 Download</b></a>
</h2>
<video class="generate_video" width="{width}" height="{height}" style="center" preload="auto" muted playsinline onpause="this.load()"
autoplay loop disablepictureinpicture id="{video_id}">
  <source src="http://localhost:8866/{url}" type="video/mp4">
  Your browser does not support the video tag.
</video>
"""
    return video_html

def generate_component(generate_function, text):
    if text == "" or text is None:
        return [None for _ in range(1)]
    # uid = random.randrange(99999)
    datas = generate_function(text, uid)
    htmls = [get_video_html(data, idx) for idx, data in enumerate(datas)]
    return htmls


# LOADING

# DEMO
port = 8866
# 构建启动 HTTP 服务器的命令
command = f"python3 -m http.server {port}"
try:
    # 使用 subprocess 运行命令
    process = subprocess.Popen(command, shell=True)
except Exception as e:
    print(f"An error occurred: {e}")

theme = gr.themes.Default(primary_hue="blue", secondary_hue="gray")
generate_and_show = partial(generate_component, generate)

with gr.Blocks(css=CSS, theme=theme) as demo:
    gr.Markdown(WEBSITE)
    videos = []

    with gr.Row():
        with gr.Column(scale=3):
            text = gr.Textbox(
                show_label=True,
                label="输入想要生成的文本",
                value=DEFAULT_TEXT,
            )
            # with gr.Row():
            #     with gr.Column(scale=1):
            #         motion_len = gr.Textbox(
            #             show_label=True,
            #             label="Motion length (<10s)",
            #             value=0,
            #             info="Specify the motion length; 0 to use the default auto-setting.",
            #         )
            #     with gr.Column(scale=1):
            #         use_ik = gr.Radio(
            #             ["Raw", "IK"],
            #             label="Post-processing",
            #             value="IK",
            #             info="Use basic inverse kinematic (IK) for foot contact locking",
            #         )
            gen_btn = gr.Button("Generate", variant="primary")
            clear = gr.Button("Clear", variant="secondary")
            gr.Markdown(
                        f"""
                            
                        """
                    )

        with gr.Column(scale=2):

            def generate_example(text):
                return generate_and_show(text)

            examples = gr.Examples(
                examples=[[x] for x in EXAMPLES],
                inputs=[text],
                examples_per_page=10,
                run_on_click=False,
                cache_examples=False,
                fn=generate_example,
                outputs=[],
            )

    i = -1
    # should indent
    for _ in range(1):
        with gr.Row():
            for _ in range(1):
                i += 1
                video = gr.HTML()
                videos.append(video)
    gr.Markdown(WEBSITE_bottom)
    # connect the examples to the output
    # a bit hacky
    examples.outputs = videos

    def load_example(example_id):
        processed_example = examples.non_none_processed_examples[example_id]
        return gr.utils.resolve_singleton(processed_example)

    examples.dataset.click(
        load_example,
        inputs=[examples.dataset],
        outputs=examples.inputs_with_examples,  # type: ignore
        show_progress=False,
        postprocess=False,
        queue=False,
    ).then(fn=generate_example, inputs=examples.inputs, outputs=videos)

    gen_btn.click(  #生成
        fn=generate_and_show,
        inputs=[text],
        outputs=videos,
    )
    text.submit(   #提交文本
        fn=generate_and_show,
        inputs=[text],
        outputs=videos,
    )

    def clear_videos():
        return [None for x in range(1)] + [DEFAULT_TEXT]

    clear.click(fn=clear_videos, outputs=videos + [text])  #清除

demo.launch(debug=True)





