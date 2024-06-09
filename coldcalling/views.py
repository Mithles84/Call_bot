# from django.shortcuts import render
# from .models import Business
# from django.shortcuts import render, redirect
# from django.contrib.auth.forms import UserCreationForm


# def index(request):
#     businesses = Business.objects.all()
#     return render(request, 'index.html', {'businesses': businesses})

# from django.shortcuts import render, redirect
# from django.contrib.auth import authenticate, login, logout
# from .forms import BusinessRegistrationForm, LoginForm
# from .models import Business

# def register(request):
#     if request.method == 'POST':
#         form = BusinessRegistrationForm(request.POST)
#         if form.is_valid():
#             business = form.save(commit=False)
#             business.set_password(form.cleaned_data['password'])
#             business.save()
#             return redirect('login')
#     else:
#         form = BusinessRegistrationForm()
#     return render(request, 'register.html', {'form': form})

# def login_view(request):
#     if request.method == 'POST':
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             email = form.cleaned_data['email']
#             password = form.cleaned_data['password']
#             user = authenticate(email=email, password=password)
#             if user is not None:
#                 login(request, user)
#                 return redirect('home')  # Replace 'home' with your home page URL name
#     else:
#         form = LoginForm()
#     return render(request, 'login.html', {'form': form})



# +-------------------+        +-----------------------+        +------------------+        +------------------------+
# |   Step 1: Install |        |  Step 2: Real-Time    |        |  Step 3: Pass    |        |  Step 4: Live Audio    |
# |   Python Libraries|        |  Transcription with   |        |  Real-Time       |        |  Stream from ElevenLabs|
# +-------------------+        |       AssemblyAI      |        |  Transcript to   |        |                        |
# |                   |        +-----------------------+        |      OpenAI      |        +------------------------+
# | - assemblyai      |                    |                    +------------------+                    |
# | - openai          |                    |                             |                              |
# | - elevenlabs      |                    v                             v                              v
# | - mpv             |        +-----------------------+        +------------------+        +------------------------+
# | - portaudio       |        |                       |        |                  |        |                        |
# +-------------------+        |  AssemblyAI performs  |-------->  OpenAI generates|-------->  ElevenLabs streams   |
#                              |  real-time speech-to- |        |  response based  |        |  response as live      |
#                              |  text transcription   |        |  on transcription|        |  audio to the user     |
#                              |                       |        |                  |        |                        |
#                              +-----------------------+        +------------------+        +------------------------+




from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import  LoginForm
from .models import Business, ColdCallingModel

import assemblyai as aai
#from elevenlabs import generate, stream
from openai import OpenAI
from .forms import BusinessRegistrationForm, LoginForm

cold_calling_model = ColdCallingModel()
def index(request):
    businesses = Business.objects.all()
    return render(request, 'index.html', {'businesses': businesses})


def register_view(request):
    if request.method == 'POST':
        form = BusinessRegistrationForm(request.POST)
        if form.is_valid():
            business = form.save(commit=False)
            business.set_password(form.cleaned_data['password'])
            business.save()
            return redirect('login')
    else:
        form = BusinessRegistrationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Replace 'home' with your home page URL name
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def train_model_view(request):
    if request.method == 'POST':
        businesses = Business.objects.all()
        texts = [business.name for business in businesses]
        labels = [1 if 'positive' in business.name else 0 for business in businesses]  # Example labels
        cold_calling_model.train(texts, labels)
        return render(request, 'cold_calling.html', {'message': 'Model trained successfully!'})
    return render(request, 'cold_calling.html', {'message': 'Training model...'})

def predict_view(request):
    if request.method == 'POST':
        text = request.POST.get('text')
        prediction = cold_calling_model.predict(text)
        return render(request, 'predict.html', {'prediction': prediction})
    return render(request, 'predict.html')
import assemblyai as aai
import openai
import requests

class AIAssistant:
    def __init__(self):
        aai.settings.api_key = "ASSEMBLYAI-API-KEY"
        self.openai_client = openai.OpenAI(api_key="OPENAI-API-KEY")
        self.elevenlabs_api_key = "ELEVENLABS-API-KEY"
        self.transcriber = None
        self.full_transcript = [
            {"role": "system", "content": "You are a receptionist at a dental clinic. Be resourceful and efficient."},
        ]

    def start_transcription(self):
        self.transcriber = aai.RealtimeTranscriber(
            sample_rate=16000,
            on_data=self.on_data,
            on_error=self.on_error,
            on_open=self.on_open,
            on_close=self.on_close,
            end_utterance_silence_threshold=1000
        )
        self.transcriber.connect()
        microphone_stream = aai.extras.MicrophoneStream(sample_rate=16000)
        self.transcriber.stream(microphone_stream)

    def stop_transcription(self):
        if self.transcriber:
            self.transcriber.close()
            self.transcriber = None

    def on_open(self, session_opened: aai.RealtimeSessionOpened):
        print("Session ID:", session_opened.session_id)

    def on_data(self, transcript: aai.RealtimeTranscript):
        if not transcript.text:
            return
        if isinstance(transcript, aai.RealtimeFinalTranscript):
            self.generate_ai_response(transcript)
        else:
            print(transcript.text, end="\r")

    def on_error(self, error: aai.RealtimeError):
        print("An error occurred:", error)

    def on_close(self):
        print("Closing session")

    def generate_ai_response(self, transcript):
        self.stop_transcription()
        self.full_transcript.append({"role": "user", "content": transcript.text})
        print(f"\nPatient: {transcript.text}", end="\r\n")
        response = self.openai_client.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=self.full_transcript
        )
        ai_response = response['choices'][0]['message']['content']
        self.generate_audio(ai_response)
        self.start_transcription()
        print(f"\nReal-time transcription: ", end="\r\n")

    def generate_audio(self, text):
        self.full_transcript.append({"role": "assistant", "content": text})
        print(f"\nAI Receptionist: {text}")
        audio_stream = self.call_elevenlabs_api(text)
        self.stream_audio(audio_stream)

    def call_elevenlabs_api(self, text):
        # Make a POST request to Eleven Labs API to generate audio
        url = "https://api.elevenlabs.io/v1/text-to-speech"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.elevenlabs_api_key}"
        }
        data = {
            "text": text,
            "voice": "Joeroot"
        }
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        return response.content

    def stream_audio(self, audio_stream):
        # Stream the audio response (implementation will depend on how you want to handle the audio)
        # For example, you might save it to a file and play it, or stream directly to a client
        with open("output_audio.mp3", "wb") as f:
            f.write(audio_stream)
        # Code to play the audio or stream it to a client goes here

# Instantiate the assistant and start
ai_assistant = AIAssistant()
greeting = "Thank you for calling Vancouver dental clinic. My name is Sandy, how may I assist you?"
ai_assistant.generate_audio(greeting)
ai_assistant.start_transcription()