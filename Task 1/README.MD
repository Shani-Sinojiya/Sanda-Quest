# Task 1: Speech Recognition

## Requirements

- Develop an ASR model to recognize Kannada speech from audio files.
- Handle informal and colloquial language.
- Support fine-tuning with the provided dataset and additional Kannada datasets.

## Key Features

- Transcription of Kannada speech to text.
- Noise handling and speech enhancement.
- Accommodation of dialect variations.

## Process Overview

The system processes audio files in the specified directory, transcribes them, and saves the metadata to MongoDB. The steps are as follows:

1. List all files in the specified directory.
2. Iterate through each file and check if it is an MP3 file.
3. Skip files that are not MP3 or have already been processed.
4. Split each MP3 file into chunks of a specified maximum size.
5. Transcribe each chunk using a Kannada transcription service.
6. Merge the transcriptions of all chunks into a single transcription.
7. Collect metadata about the file and the transcription.
8. Save the metadata to a MongoDB database.
9. Handle exceptions and continue processing the next file.
10. Print messages to indicate the progress and status of file processing.
