# Conversify
Conversify is an application that when given an input image of a face and a statement, a video is generated with the person in the image responding to the input statement, depending on the declared personality and voice.

When launching Conversify, you have the option to enhance your experience by leveraging the power of character.ai personalities and elevenlabs voices. This allows you to customize the chatbot's personality and choose from a variety of engaging and lifelike voices to give your animated face a truly unique character.

Here's how Conversify works:

Input an image: Begin by providing an image of a person you want to animate. This can be a photo or any still image that captures the person's face.

  1. Choose personality and voice options: Take advantage of the character.ai personalities and elevenlabs voices to shape the behavior and voice of the chatbot that will interact with you.

  2. Speak your statement: Conversify listens and records your spoken statement. Express your thoughts, ask questions, or engage in a conversation with the chatbot. Your statement sets the context for the chatbot's response.

  3. Chatbot interaction: The recorded statement is then processed by a chatbot that analyzes the input and generates a tailored response based on the selected personality.

  4. Synthesized speech: The chatbot's response is transformed into synthesized speech. The selected voice from elevenlabs adds a human-like quality to the generated speech, making the interaction even more realistic and immersive.

  5. Talking face generation: The synthesized speech is seamlessly integrated with the input image using SadTalker, a talking face generation model.

Note: Conversify requires an internet connection to access character.ai personalities and elevenlabs voices.

#

### Cloning the repository

--> Clone the repository using the command below :
```bash
git clone https://github.com/amauriciogonzalez/Conversify.git

```

--> Move into the directory where we have the project files : 
```bash
cd Conversify

```

--> Create a virtual environment :
```bash
# If you are on Windows
virtualenv env
# If you are on Linux or Mac
python -m venv env
```

--> Activate the virtual environment :
```bash
# If you are on Windows
.\env\Scripts\activate
# If you are on Linux or Mac
source env/bin/activate
```

--> Install the requirements :
```bash
pip install -r requirements.txt

pip3 install --pre torch torchvision torchaudio --index-url https://download.pytorch.org/whl/nightly/cu121

bash .\scripts\download_models.sh

```

--> Create a config.json file :
```bash
{
    "CAI_data": [
        {
            "token": "",
            "character": ""
        }
    ],
    "EL_data": [
        {
            "EL_key":  "",
            "voice": ""
        }

    ]
}
```

--> Access config.json to add ElevenLabs and CharacterAI keys :

Obtaining an ElevenLabs key:
  1. Access the ElevenLabs website: https://beta.elevenlabs.io/
  2. Click on Profile Settings on the top-right side of the page
  3. Copy the ElevenLabs api key

Obtaining a CharacterAI key (token):
  1. Log in on character.ai: https://beta.character.ai/
  2. Go to Network tab in DevTools and refresh page
  3. Search /dj-rest-auth/auth0/
  4. Copy the key value under Network

#

### Running the App

--> To run the App, we use :
```bash
python app.py
# Running the app with CharacterAI and ElevenLabs 
python app.py --ttt cai --tts el
```

#

### SadTalker Citation
```bash
@article{zhang2022sadtalker,
  title={SadTalker: Learning Realistic 3D Motion Coefficients for Stylized Audio-Driven Single Image Talking Face Animation},
  author={Zhang, Wenxuan and Cun, Xiaodong and Wang, Xuan and Zhang, Yong and Shen, Xi and Guo, Yu and Shan, Ying and Wang, Fei},
  journal={arXiv preprint arXiv:2211.12194},
  year={2022}
}
```


## App Preview :

### Demo

https://github.com/amauriciogonzalez/Conversify/assets/88101535/55019afe-ff35-4904-9f77-e9a53d7b35a5


### Result

https://github.com/amauriciogonzalez/Conversify/assets/88101535/ddd54aef-39fc-43c1-b1b0-382f3041c188



#
