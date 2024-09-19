# VideoTranscriber
VideoTranscriber is a Tkinter-based GUI application that converts audio from MP4 and MOV video files into text. Using moviepy for audio extraction and SpeechRecognition for transcription, it simplifies the process of turning spoken content into written text.

![image](https://github.com/user-attachments/assets/33f392b2-f9ec-459b-95dd-6edc92398790)

![image](https://github.com/user-attachments/assets/dd4c9760-2b6f-4db4-a464-727bbb4c1339)

## Features
Transcribe Audio: Select MP4 or MOV files to extract audio and transcribe it to text.
Stop Transcription: Option to stop the transcription process at any time.

## Prerequisites
Ensure you have the following Python packages installed:

**moviepy**: For handling video files and extracting audio.
**SpeechRecognition**: For transcribing audio to text.

You can install the required packages using pip:
```
pip install moviepy
pip install SpeechRecognition
```

## Usage
Select Video Files:

Click the "Select Video Files" button to open a file dialog and choose MP4 or MOV files.
Transcription Process:

The transcription will start automatically in a background thread.
Click the "Stop Transcription" button if you wish to stop the process.

## Code Overview
- transcribe_audio_in_chunks(audio_file_path): Processes audio in chunks for better recognition, using Google’s speech recognition API.
- transcribe_selected_videos(video_file_paths): Extracts audio from selected video files and performs transcription.
- select_video_files(): Opens a file dialog to select video files.
- stop_transcription(): Stops the transcription process if it's currently running.

## Example
After running the application, you'll see a window where you can:
- Select MP4 or MOV files to transcribe their audio content.
- Stop the transcription process at any time.

Error Handling
The app handles various exceptions, including:
- API request errors: Issues with the speech recognition API.
- General errors: Any unexpected issues during processing. If an error occurs, an appropriate message will be shown in a dialog box.
- Threading is implemented to prevent the Tkinter GUI from becoming unresponsive during transcription. 
- The audio is transcribed in 60-second increments to avoid crashes with large video files.

## Links

Contact @ ullah.muhib095@gmail.com / muhib.ullah@torontomu.ca

Linkedin @ https://www.linkedin.com/in/muhib-ullah095/
