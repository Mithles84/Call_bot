import assemblyai as aai
from openai import OpenAI
# If 'elevenlabs' doesn't have generate and stream, you might need to call their API directly.

class AIAssistant:
    def __init__(self):
        aai.settings.api_key = "ASSEMBLYAI-API-KEY"
        self.openai_client = OpenAI(api_key="OPENAI-API-KEY")
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
        response = self.openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=self.full_transcript
        )
        ai_response = response.choices[0].message.content
        self.generate_audio(ai_response)
        self.start_transcription()
        print(f"\nReal-time transcription: ", end="\r\n")

    def generate_audio(self, text):
        self.full_transcript.append({"role": "assistant", "content": text})
        print(f"\nAI Receptionist: {text}")
        # Replace this section with a direct API call if `generate` and `stream` are not available
        audio_stream = self.call_elevenlabs_api(text)
        self.stream_audio(audio_stream)

    def call_elevenlabs_api(self, text):
        # Replace with actual API call to Eleven Labs if generate and stream are not available
        return "audio_stream"

    def stream_audio(self, audio_stream):
        # Replace with actual streaming logic
        pass

# Instantiate the assistant and start
ai_assistant = AIAssistant()
greeting = "Thank you for calling Vancouver dental clinic. My name is Sandy, how may I assist you?"
ai_assistant.generate_audio(greeting)
ai_assistant.start_transcription()
