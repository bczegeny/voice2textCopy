import os
import pyaudio
import wave
import threading
import queue
from faster_whisper import WhisperModel
from playsound import playsound
import pyperclip
from pynput import keyboard

# Transcribe audio
def transcribe_audio(filename):
    segments, info = model.transcribe(filename, beam_size=5)
    transcription = " ".join([segment.text for segment in segments])
    return transcription

# Initialize the WhisperModel
model_size = "small"
model = WhisperModel(model_size, device="cpu", compute_type="int8")

# Play audio file
def play_audio_file(filename):
    playsound(filename)

# Record audio
def record_audio(filename, stop_event, audio_queue):
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000
    CHUNK = 1024
    play_audio_file("./listen.wav")
    audio = pyaudio.PyAudio()
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)

    print("Recording... Press the trigger key to stop.")

    while not stop_event.is_set():
        data = stream.read(CHUNK, exception_on_overflow=False)
        audio_queue.put(data)

    print("Finished recording")

    stream.stop_stream()
    stream.close()
    audio.terminate()

    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(audio.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(list(audio_queue.queue)))

# Define the trigger key or key combination
trigger_key = {keyboard.Key.alt, keyboard.KeyCode.from_char('a')}
current_keys = set()

recording = False
stop_event = threading.Event()
audio_queue = queue.Queue()
audio_filename = "recorded_audio.wav"

def on_press(key):
    global recording, stop_event, audio_queue, audio_filename
    if key in trigger_key:
        current_keys.add(key)
        if current_keys == trigger_key:
            if not recording:
                recording = True
                stop_event.clear()
                main()
            else:
                recording = False
                stop_event.set()

                # Wait for the recording thread to finish
                record_thread.join()

                # Transcribe the audio
                transcription = transcribe_audio(audio_filename)
                print("Transcription:", transcription)

                # Copy transcription to clipboard
                pyperclip.copy(transcription)

                # Play stop-listening.wav
                play_audio_file("./stop-listening.wav")
    elif key == keyboard.Key.esc:
        return False

def on_release(key):
    if key in current_keys:
        current_keys.remove(key)

# Main function
def main():
    global record_thread
    record_thread = threading.Thread(target=record_audio, args=(audio_filename, stop_event, audio_queue))
    record_thread.start()

if __name__ == "__main__":
    print(f"Press {'+'.join([str(k) for k in trigger_key])} to start/stop recording...")
    print("Press 'esc' to exit the application.")
    try:
        with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
            listener.join()
    finally:
        # Clean up any old recordings
        if os.path.exists(audio_filename):
            os.remove(audio_filename)
