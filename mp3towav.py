import os
import tempfile
import zipfile
import numpy as np
import soundfile as sf
import streamlit as st
from typing import List

# Set up the Streamlit page
st.title("MP3 to WAV Converter")
st.write("Upload MP3 files and convert them to WAV format with a 22,050 sample rate.")

# Allow multiple files to be uploaded
uploaded_files = st.file_uploader(
    "Upload MP3 files", type="mp3", accept_multiple_files=True)


def process_mp3(file) -> bytes:
    # Read MP3 file
    audio_data, sample_rate = sf.read(file, dtype="float32")

    # Downsample audio to 22050 sample rate
    audio_data = audio_data[::sample_rate // 22050, :]

    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp:
        # Save audio data as WAV file
        sf.write(temp.name, audio_data, 22050, subtype="FLOAT")

        wav_data = temp.read()

    return wav_data


if uploaded_files:
    # Start converting the files
    st.write(f"You've uploaded {len(uploaded_files)} files.")
    st.write("Converting files...")

    # Iterate over and convert all files
    converted_files = []
    for file in uploaded_files:
        wav_data = process_mp3(file)
        converted_files.append((file.name, wav_data))
        st.write(f"Converted {file.name} successfully.")

    #Zip all converted files together
    with tempfile.NamedTemporaryFile(delete=False, suffix=".zip") as temp:
        with zipfile.ZipFile(temp.name, 'w') as zipf:
            for i, (file_name, file_data) in enumerate(converted_files):
                wav_name = f"converted_{i + 1}.wav"
                zipf.writestr(wav_name, file_data)

        temp.seek(0)
        zip_data = temp.read()

    st.download_button(
        "Download All Converted Files",
        zip_data,
        "converted_files.zip",
        "application/zip"
    )
