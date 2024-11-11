# SandalQuest - AI/ML Hackathon Project

### ML-Fiesta: AI/ML Hackathon

##### International Institute of Information Technology (IIIT), Bangalore

## Project Overview​

The goal is to utilize AI and machine learning to develop a pipeline that processes and understands audio content related to sandalwood cultivation. We are focusing on creating:

- An Automatic Speech Recognition (ASR) model for the Kannada language.
- A speech-based question-answering system to help users access information from the audio data.​

### Project Objectives:​

- Develop an ASR model that accurately recognizes colloquial Kannada speech.
- Create a searchable audio database using the ASR output.
- Implement a question-answering system allowing users to ask questions via speech input.

## Problem Statement​

Karnataka is a key region for sandalwood, which holds significant cultural, religious, and economic value in India. However, much of the traditional knowledge around sandalwood cultivation is conveyed informally and captured in audio recordings. These resources are not easily accessible, and there's a need to digitize and preserve this indigenous knowledge. The main challenge is handling colloquial Kannada speech with background noise, as it differs from standard formal language.​

### Challenges:​

- Limited digital information on sandalwood cultivation.​
- Audio recordings often contain noise and informal language.​
- Standard ASR models struggle with colloquial language.​

## Scope

The project includes:​

- Building a Kannada ASR model for colloquial language recognition.​
- Creating a searchable database by transcribing audio files.​
- Developing a speech-based question-answering system to query the audio corpus.​
- Fine-tuning the ASR model using both provided and publicly available Kannada datasets.​

### Out of Scope:​

- Processing audio in languages other than Kannada.​
- Real-time transcription of live streams.​
- Handling complex multi-turn dialogues.​

## Dataset Description​

The dataset consists of Kannada audio files focused on sandalwood cultivation:

- Source: Audio files scraped from YouTube.
- Content Type: Informal Kannada speech, possibly with background noise.
- Format: Common audio formats like MP3.

### Dataset Challenges:

- Noisy recordings made in public spaces.
- Informal and colloquial language use.
- Variations in pronunciation and dialects.

## Functional Requirements

### Task 1: Speech Recognition

- Develop an ASR model for Kannada speech from audio files.
- Handle informal and colloquial speech.
- Support model fine-tuning with additional datasets.

#### Key Features:

- Kannada speech transcription to text.
- Noise reduction and speech enhancement.
- Accommodate dialect variations.

#### Code:

[Task 1 Folder](./Task%201/)

#### More Details:

[Task 1 Details](./Task%201/README.MD)

### Task 2: Speech-based Question-Answering System

- Allow users to ask questions via speech input.
- Convert the spoken question to text using the ASR model.
- Search the transcribed audio data for relevant answers.
- Return the most relevant audio segment as the answer.

#### Key Features:

- Accurate answer retrieval from speech queries.
- Efficient search and indexing of the transcribed corpus.
- User-friendly query and response interface.

#### Code:

[Task 2 Folder](./Task%202/)

#### More Details:

[Task 2 Details](./Task%202/README.MD)

## Pipeline Architecture

<div align="center" style="background:white">
  <img src="./assets/Pipeline_Architecture.png" alt="Architecture Diagram" width="100%">
</div>

## Technical Requirements

- **Languages**: Python.
- **Libraries & Frameworks**: PyTorch, Whisper (ASR), Hugging Face Transformers.
- **Database**: MongoDB.
- **Deployment**: Google Cloud Platform (GCP) or AWS for scalable processing.
- **Hardware**: GPU servers for training, cloud instances for deployment.
- **Tools**: Google Colab, Jupyter Notebooks, GitHub.

## Risks & Mitigation

| **Risk**                               | **Mitigation**                                  |
| -------------------------------------- | ----------------------------------------------- |
| Low-quality audio data                 | Use noise reduction and data augmentation       |
| Poor ASR accuracy on colloquial speech | Fine-tune model with additional colloquial data |
| High query processing latency          | Optimize search algorithms and indexing         |

## Conclusion

This project aims to document and provide access to indigenous knowledge of sandalwood cultivation through advanced ASR and NLP technologies. By building a robust pipeline, we will not only aid conservation but also provide valuable insights for users interested in sandalwood cultivation.

## Team Details

### Team Name: Code Wizards

### Team Members:

- [Shani Sinojiya](https://www.shanisinojiya.tech) (Team Lead / AI/ML & Backend Developer)
- [Mohammad Anas Africawala](https://linkedin.com/in/mohammad-anas-africawala/) (AI/ML Engineer)
- [Tisha Patel](https://www.linkedin.com/in/tiisha13/) (Full Stack Developer)

## Project Links

- [GitHub Repository](https://github.com/Shani-Sinojiya/SandalQuest.git)

## References

- [Whisper: A Speech Recognition Framework](https://openai.com/index/whisper/) by OpenAI.
- [Hugging Face Transformers](https://huggingface.co/transformers/) for NLP models.
- [Google Colab](https://colab.research.google.com/) for collaborative coding.
- [MongoDB](https://www.mongodb.com/) for database management.
- [PyTorch](https://pytorch.org/) for deep learning models.
- [GitHub](https://www.github.com/) for version control and collaboration.
