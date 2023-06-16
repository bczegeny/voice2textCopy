# Audio Transcription for M1 Mac

This is a Python script that records audio, transcribes it using the [Faster Whisper](https://github.com/guillaumekln/faster-whisper) ASR model, and copies the transcription to the clipboard. It is designed to run natively on M1 Apple Silicon chips.

## Dependencies

- pyaudio
- wave
- threading
- queue
- faster_whisper
- playsound
- pyperclip
- pynput

## Installation

1. Install Miniforge for macOS with ARM support:

```bash
curl -L -O https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-MacOSX-arm64.sh
chmod +x Miniforge3-MacOSX-arm64.sh
./Miniforge3-MacOSX-arm64.sh
```

Follow the prompts during the installation process.

2. Restart your terminal or open a new terminal window to activate the conda environment.

3. Create a new conda environment with Python 3.9:

```bash
conda create -n audio_transcription python=3.9
```

4. Activate the new environment:

```bash
conda activate audio_transcription
```

5. Install the required dependencies:

```bash
pip install pyaudio wave playsound pyperclip pynput
```

6. Install the Faster Whisper ASR model:

```bash
pip install faster_whisper
```

## Usage

1. Ensure the `audio_transcription` conda environment is active:

```bash
conda activate audio_transcription
```

2. Run the script:

```bash
python voice2textwait.py
```

3. Press the trigger key combination (Alt + A) to start recording. Press the same key combination again to stop recording.

4. The script will transcribe the audio and copy the transcription to the clipboard.

5. Press 'esc' to exit the application.

Remember to activate the `audio_transcription` conda environment whenever you want to run the script.
