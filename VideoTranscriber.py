# Project Name : VideoTranscriber
# Date : 2024-09-09 -> 2024-09-19
# Author : Muhib Ullah 

import moviepy.editor as mp  # Import moviepy for handling video files
import speech_recognition as sr  # Import speech recognition for audio transcription
import os  # Import os for file handling
import tkinter as tk  # Import tkinter for GUI
from tkinter import filedialog, messagebox  # Import file dialog and message box from tkinter
import threading  # Import threading for running transcription in a background thread

# Ensure these packages are installed via pip
# pip install moviepy
# pip install SpeechRecognition

# Initialize the speech recognizer
recognizer = sr.Recognizer()

# Global flag to control the transcription process
transcription_in_progress = False

# Function to process the audio in chunks for better recognition
def transcribe_audio_in_chunks(audio_file_path, chunk_duration=60):
    global transcription_in_progress
    # To store the entire transcription
    full_transcription = ""  

    # Load the audio file
    with sr.AudioFile(audio_file_path) as audio_source:
        total_audio_duration = int(audio_source.DURATION)  # Get the total length of the audio
        
        # Loop through the audio in chunks
        for start_time in range(0, total_audio_duration, chunk_duration):
            # Check if the stop button was pressed
            if not transcription_in_progress:
                print("Transcription stopped.")
                break

            print(f"Processing audio chunk from {start_time} to {start_time + chunk_duration} seconds...")
            
            # Set the starting point of the audio chunk
            audio_source.audio_position = start_time
            # Record a chunk of the audio
            audio_chunk = recognizer.record(audio_source, duration=chunk_duration)
            
            try:
                # Try to recognize the speech in the chunk using Google's speech recognition API
                chunk_text = recognizer.recognize_google(audio_chunk)
                # Append the chunk's transcription to the full transcription
                full_transcription += chunk_text + " "
            except sr.RequestError as request_error:
                # Handle errors related to the API request
                print(f"API request failed: {request_error}")
            except sr.UnknownValueError:
                # Handle cases where the speech recognition could not understand the audio
                print("Speech recognition could not understand the audio")
    
    return full_transcription

# Function to transcribe audio from video files
def transcribe_selected_videos(video_file_paths):
    global transcription_in_progress
    # Set flag to True when starting transcription
    transcription_in_progress = True  
    # List to store all transcriptions
    all_transcriptions = []  
    
    if not video_file_paths:
        # If no video files are selected, show an error message
        print("No video files selected.")
        return

    # Loop through the selected video files
    for video_file_path in video_file_paths:
        if not transcription_in_progress:
            break
        
        print(f"Processing video: {video_file_path}")
        
        # Load the video file
        video_clip = mp.VideoFileClip(video_file_path)

        # Extract audio from the video and save it as a WAV file
        audio_file_name = f"{os.path.splitext(os.path.basename(video_file_path))[0]}.wav"
        video_clip.audio.write_audiofile(audio_file_name, codec='pcm_s16le', fps=16000)

        # Transcribe the extracted audio
        video_transcription = transcribe_audio_in_chunks(audio_file_name)

        # Add the transcription to the list with a header for each video
        all_transcriptions.append(f"--- Transcription for {video_file_path} ---\n{video_transcription}\n")
        
        # Delete the temporary audio file to save space
        os.remove(audio_file_name)

    # Combine all transcriptions into one large string
    combined_transcriptions = "\n".join(all_transcriptions)
    print("\nThe transcription from all videos is: \n")
    print(combined_transcriptions)

    # Save the combined transcription to a text file
    with open("transcription.txt", "w") as transcription_file:
        transcription_file.write(combined_transcriptions)

    # Show a message box to indicate that transcription is complete
    messagebox.showinfo("Transcription Complete", "Transcriptions have been saved to transcription.txt")

# Function to stop the transcription process
def stop_transcription():
    global transcription_in_progress
    transcription_in_progress = False

# Function to open a file dialog and let the user select video files
def select_video_files():
    # Open a dialog to select video files (MP4 or MOV format)
    video_file_paths = filedialog.askopenfilenames(title="Select MP4 or MOV files", 
                                                   filetypes=[("Video files", "*.mp4 *.mov")])
    
    # If video files are selected, start the transcription process
    if video_file_paths:
        # Run the transcription process in a separate thread
        transcription_thread = threading.Thread(target=transcribe_selected_videos, args=(video_file_paths,))
        transcription_thread.start()
    else:
        # Show a warning if no files are selected
        messagebox.showwarning("No File Selected", "Please select at least one video file.")

# Set up the Tkinter GUI
root_window = tk.Tk()
root_window.title("Video to Text Transcription")
# Set the size of the window
root_window.geometry("500x300")
# Set the background color of the window
root_window.config(bg="#2c3e50")  

# Header Frame for the title
header_frame = tk.Frame(root_window, bg="#34495e", bd=5)
header_frame.place(relx=0.5, rely=0.15, relwidth=0.75, relheight=0.15, anchor='n')

# Label for the header
header_label = tk.Label(header_frame, text="Select MP4 or MOV Files", font=("Helvetica", 16, "bold"), bg="#34495e", fg="white")
header_label.pack(padx=10, pady=10)

# Frame for the file selection button
button_frame = tk.Frame(root_window, bg="#2c3e50")
button_frame.place(relx=0.5, rely=0.45, anchor='n')

# Button for file selection 
select_button = tk.Button(button_frame, text="Select Video Files", command=select_video_files, font=("Helvetica", 14), bg="#1abc9c", fg="white", activebackground="#16a085", activeforeground="white", padx=20, pady=10)
select_button.pack()

# Stop Transcription button
stop_button = tk.Button(button_frame, text="Stop Transcription", command=stop_transcription, font=("Helvetica", 14), bg="#e74c3c", fg="white", activebackground="#c0392b", activeforeground="white", padx=20, pady=10)
stop_button.pack(pady=20)

# Start the Tkinter main loop 
root_window.mainloop()
