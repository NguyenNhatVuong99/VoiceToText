from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
import speech_recognition as sr
import os

def index(request):
    return render(request, "transcription/index.html")

@csrf_exempt
def transcription_audio(request):
    if request.method == "POST" and request.FILES.get("audio"):
        audio_file = request.FILES["audio"]
        print(f"Received audio file: {audio_file.size} bytes")
        file_path = default_storage.save("temp/audio.webm", audio_file)
        recognizer = sr.Recognizer()

        # Attempt to recognize the audio
        try:
            # Convert the audio file to WAV format for processing
            wav_file_path = file_path.replace('.webm', '.wav')
            os.system(f'ffmpeg -i {file_path} {wav_file_path}')  # Using ffmpeg to convert format

            with sr.AudioFile(wav_file_path) as source:
                audio_data = recognizer.record(source)

            transcript = recognizer.recognize_google(audio_data, language='en-US')

        except sr.UnknownValueError:
            print("Speech recognition could not understand the audio.")
            transcript = "Could not understand the audio."
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
            transcript = "Error with the transcription service."
        except Exception as e:
            print(f"An unexpected error occurred: {e}")  # Log the exception message
            transcript = f"An unexpected error occurred: {e}"

        finally:
            # Clean up the temporary files
            if os.path.exists(file_path):
                os.remove(file_path)
            if os.path.exists(wav_file_path):
                os.remove(wav_file_path)

        return JsonResponse({"transcript": transcript})

    return JsonResponse({"transcript": "No audio file provided."})
