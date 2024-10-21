from flask import Flask, render_template, request, jsonify
import speech_recognition as sr
import pyttsx3

app = Flask(__name__)

# 음성 인식 (STT) 세팅
recognizer = sr.Recognizer()
microphone = sr.Microphone()

# 음성 출력 (TTS) 세팅
engine = pyttsx3.init()

def speak_text(text):
    engine.say(text)
    engine.runAndWait()

def recognize_speech():
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio, language="ko-KR")
        return text
    except sr.UnknownValueError:
        return "음성을 인식하지 못했습니다."
    except sr.RequestError:
        return "구글 음성 인식 서비스에 접근할 수 없습니다."

# 웹 페이지 렌더링
@app.route('/')
def index():
    return render_template('index.html')

# 음성 인식 처리 API
@app.route('/speech', methods=['POST'])
def process_speech():
    if request.method == 'POST':
        spoken_text = recognize_speech()
        
        if "안녕" in spoken_text:
            response = "안녕하세요! 무엇을 도와드릴까요?"
        elif "시간" in spoken_text:
            response = "현재 시간을 알려드릴게요."
        elif "김지후" in spoken_text:
            response = "바보"
        else:
            response = "제가 이해하지 못했습니다. 다시 말씀해 주세요."
        
        speak_text(response)
        return jsonify({'response': response})

if __name__ == "__main__":
    app.run(debug=True)
