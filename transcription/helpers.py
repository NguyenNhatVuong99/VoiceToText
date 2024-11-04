import speech_recognition as sr

def transcribe_audio(file_path):
    recognizer = sr.Recognizer()
    audio_file = sr.AudioFile(file_path)
    with audio_file as source:
        audio_data = recognizer.record(source)
    try:
        # Transcribe using Google's speech recognition API
        text = recognizer.recognize_google(audio_data)
        return text
    except sr.UnknownValueError:
        return "Audio unintelligible"
    except sr.RequestError:
        return "Could not request results; check network connection"