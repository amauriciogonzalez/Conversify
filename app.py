import speech_recognition as sr
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from pydub import AudioSegment
import pyttsx3
from characterai import PyCAI
from sadtalker import *
import cv2
from ffpyplayer.player import MediaPlayer
import requests
import io
import json

# Installing FFmpeg: https://phoenixnap.com/kb/ffmpeg-windows

def initVar():
    global CAI
    global CAI_client
    global EL

    try:
        with open("config.json", "r") as json_file:
            data = json.load(json_file)
    except:
        print("Unable to open JSON file.")
        exit()

    class CAI:
        token = data["CAI_data"][0]["token"]
        character = data["CAI_data"][0]["character"]

    if CAI.token:
        CAI_client = PyCAI(CAI.token)

    class EL:
        key = data["EL_data"][0]["EL_key"]
        voice = data["EL_data"][0]["voice"]


def speech_to_text():

    r = sr.Recognizer()

    with sr.Microphone() as source:
        print("Recording voice...")
        audio_text = r.listen(source)
        print("------------------------------------------------------")
        
        try:
            user_statement = r.recognize_google(audio_text)
            print("User: " + user_statement)
            print("")
            return user_statement
        except:
            print("Sorry, I did not get that")
            return "..."



def text_to_personality_text_GPT(user_statement):
    class ChromeDriverSingleton:
        _instance = None

        @classmethod
        def get_instance(cls):
            if cls._instance is None:
                cls._instance = cls._create_instance()
            return cls._instance

        @classmethod
        def _create_instance(cls):
            options = webdriver.ChromeOptions()
            options.add_argument('--headless')  # Run Chrome in headless mode
            #options.add_argument('--disable-gpu')  # Disable GPU acceleration
            options.add_argument('--no-sandbox')  # Bypass OS security model
            options.add_argument('--disable-dev-shm-usage')  # Disable "DevShmUsage" flag
            options.add_experimental_option('excludeSwitches', ['enable-logging'])
            
            return webdriver.Chrome(options=options)

    driver = ChromeDriverSingleton.get_instance()
    driver.get("https://chat.chatgptdemo.net/")
    time.sleep(2) 
    textarea = driver.find_element(By.ID, "input-chat")
    personality_AJ = "(You have the personality of a skeptical conspiracy theorist, akin to Alex Jones. Respond to the following statement in 50 words or less.)"
    personality_IM = "(You have a personality of someone who believes that the ends always justify the means. As such, you are pragmatic and utterly ruthless. You are also incredibly stubborn and dogmatic, always convinced that you're right and never considering for a second that there's anything wrong with your methods. Respond to the following statement by responding in 50 words or less.)"
    personality_H = "(You have the personality of someone who is self-assured and optimistic, and can be described as affectionate, supportive, and confident. Respond to the following statement in 50 words or less.)"
    textarea.send_keys(personality_H + " " + user_statement) 
    time.sleep(1.5)
    textarea.send_keys(Keys.RETURN)
    time.sleep(4)

    try:
        response = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "pre")))
        print("Response: " + response.text)
        print("")
        return response.text
    finally:
        driver.quit()



def text_to_personality_text_CAI(user_statement):
    chat = CAI_client.chat.get_chat(CAI.character)

    history_id = chat['external_id']
    participants = chat['participants']

    if not participants[0]['is_human']:
        tgt = participants[0]['user']['username']
    else:
        tgt = participants[1]['user']['username']
    
    data = CAI_client.chat.send_message(
        CAI.character,
        user_statement,
        history_external_id=history_id,
        tgt=tgt
    )

    name = data['src_char']['participant']['name']
    text = data['replies'][0]['text']

    print(f"{name}: {text}")
    print("")

    return text
        


def text_to_speech_EL(text):
    url = f'https://api.elevenlabs.io/v1/text-to-speech/{EL.voice}'
    headers = {
        'accept': 'audio/mpeg',
        'xi-api-key': EL.key,
        'Content-Type': 'application/json'
    }
    data = {
        'text': text,
        'voice_settings': {
            'stability': 0.75,
            'similarity_boost': 0.75
        }
    }

    response = requests.post(url, headers=headers, json=data, stream=True)
    audio_content = AudioSegment.from_file(io.BytesIO(response.content), format="mp3")
    audio_content.export(out_f="./driven_audio/audio.wav", format='wav')


def text_to_speech_PYTTS(text):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices') 
    engine.setProperty('voice', voices[0].id) # voices[1].id for female, voices[0].id for male

    engine.save_to_file(text, './driven_audio/audio.wav')
    engine.runAndWait()


def play_video(vid_path):
    print("Playing " + vid_path)

    video = cv2.VideoCapture(vid_path)
    player = MediaPlayer(vid_path)

    fps = video.get(cv2.CAP_PROP_FPS)

    while video.isOpened():
        success, frame = video.read()
        audio_frame, val = player.get_frame()
        if not success:
            print("End of video")
            break
        quitButton = cv2.waitKey(38) & 0xFF == ord('q')
        cv2.imshow("Video", frame)
        if quitButton:
            break
        if cv2.getWindowProperty("Video", cv2.WND_PROP_VISIBLE) < 1:
            break
        if val != 'eof' and audio_frame is not None:
            frame, t = audio_frame
    video.release()
    cv2.destroyAllWindows()


def main(args):
    text_to_text_method = args.ttt
    text_to_speech_method = args.tts
    
    user_statement = speech_to_text()
    character_response = "..."

    if text_to_text_method == 'gpt':
        character_response = text_to_personality_text_GPT(user_statement)
    else:
        character_response = text_to_personality_text_CAI(user_statement)
    
    if text_to_speech_method == 'pyttsx3':
        text_to_speech_PYTTS(character_response)
    else:
        text_to_speech_EL(character_response)

    vid_path = sadtalker(args)
    play_video(vid_path)


if __name__ == '__main__':
    parser = ArgumentParser()  

    # pipeline methods
    parser.add_argument("--ttt", default="gpt", choices=['gpt', 'cai'], help="text-to-text method, [gpt, cai]")
    parser.add_argument("--tts", default="pyttsx3", choices=['pyttsx3', 'el'], help="text-to-speech method, [pytts, el]")
    parser.add_argument("--repeat", action="store_true", help="the app only terminates on command")

    # sadtalker
    parser.add_argument("--driven_audio", default='./driven_audio/audio.wav', help="path to driven audio")
    parser.add_argument("--source_image", default='./source_image/img_1.PNG', help="path to source image")
    parser.add_argument("--ref_eyeblink", default=None, help="path to reference video providing eye blinking")
    parser.add_argument("--ref_pose", default=None, help="path to reference video providing pose")
    parser.add_argument("--checkpoint_dir", default='./checkpoints', help="path to output")
    parser.add_argument("--result_dir", default='./results', help="path to output")
    parser.add_argument("--pose_style", type=int, default=0,  help="input pose style from [0, 46)")
    parser.add_argument("--batch_size", type=int, default=2,  help="the batch size of facerender")
    parser.add_argument("--size", type=int, default=256,  help="the image size of the facerender")
    parser.add_argument("--expression_scale", type=float, default=1.,  help="the batch size of facerender")
    parser.add_argument('--input_yaw', nargs='+', type=int, default=None, help="the input yaw degree of the user ")
    parser.add_argument('--input_pitch', nargs='+', type=int, default=None, help="the input pitch degree of the user")
    parser.add_argument('--input_roll', nargs='+', type=int, default=None, help="the input roll degree of the user")
    parser.add_argument('--enhancer',  type=str, default=None, help="Face enhancer, [gfpgan, RestoreFormer]")
    parser.add_argument('--background_enhancer',  type=str, default=None, help="background enhancer, [realesrgan]")
    parser.add_argument("--cpu", dest="cpu", action="store_true") 
    parser.add_argument("--face3dvis", action="store_true", help="generate 3d face and 3d landmarks") 
    parser.add_argument("--still", action="store_true", help="can crop back to the original videos for the full body aniamtion") 
    parser.add_argument("--preprocess", default='crop', choices=['crop', 'extcrop', 'resize', 'full', 'extfull'], help="how to preprocess the images" ) 
    parser.add_argument("--verbose",action="store_true", help="saving the intermedia output or not" ) 
    parser.add_argument("--old_version",action="store_true", help="use the pth other than safetensor version" ) 


    # net structure and parameters
    parser.add_argument('--net_recon', type=str, default='resnet50', choices=['resnet18', 'resnet34', 'resnet50'], help='useless')
    parser.add_argument('--init_path', type=str, default=None, help='Useless')
    parser.add_argument('--use_last_fc',default=False, help='zero initialize the last fc')
    parser.add_argument('--bfm_folder', type=str, default='./checkpoints/BFM_Fitting/')
    parser.add_argument('--bfm_model', type=str, default='BFM_model_front.mat', help='bfm model')

    # default renderer parameters
    parser.add_argument('--focal', type=float, default=1015.)
    parser.add_argument('--center', type=float, default=112.)
    parser.add_argument('--camera_d', type=float, default=10.)
    parser.add_argument('--z_near', type=float, default=5.)
    parser.add_argument('--z_far', type=float, default=15.)

    args = parser.parse_args()

    if torch.cuda.is_available() and not args.cpu:
        args.device = "cuda"
    else:
        args.device = "cpu"

    initVar()
    
    if args.repeat:
        while True:
            main(args)
    else:
        main(args)
