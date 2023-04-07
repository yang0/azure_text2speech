import os
from tqdm import tqdm
import azure.cognitiveservices.speech as speechsdk

key = "写你自己的key"
region = "eastasia"
endpoint = "https://eastasia.api.cognitive.microsoft.com/sts/v1.0/issuetoken"

# Read user input
filename = input("Please enter the name of the text file to convert: ")
language = input("Please select a language (1 for Chinese, 2 for English): ")

# Convert language option to language code
language_code = "zh-CN" if language == "1" else "en-US"
voice = "zh-CN-XiaochenNeural" if language == "1" else "en-US-JennyNeural"

audio_format = "Riff24Khz16BitMonoPcm"

speech_config = speechsdk.SpeechConfig(subscription=key, region=region)
speech_config.set_speech_synthesis_output_format(
    speechsdk.SpeechSynthesisOutputFormat[audio_format]
)
synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=None)

# Open the input file and read its contents
with open(filename, "r", encoding="utf-8") as f:
    lines = f.readlines()

# Loop through each line and convert it to an audio file
for i, line in tqdm(enumerate(lines), total=len(lines), desc="Converting text to speech"):
    

    # Ignore empty lines
    if not line.strip():
        continue

    # Truncate line if it exceeds the character limit
    line = line[:5000]


    # 语速不普通的慢20%
    ssml = f"""
        <speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xmlns:mstts="http://www.w3.org/2001/mstts" xml:lang="en-US">
        <voice name="{voice}">
            <mstts:express-as style="chat">
                <prosody rate="0.8">
                {line}
                </prosody>
            </mstts:express-as>
        </voice>
        </speak>
        """

    # 将SSML文本合成为语音
    result = synthesizer.speak_ssml_async(ssml).get()


    # Generate filename for the audio file
    audio_file = f"{os.path.splitext(filename)[0]}_{i}.wav"


    with open(audio_file, "wb") as audio_file:
        audio_file.write(result.audio_data)

