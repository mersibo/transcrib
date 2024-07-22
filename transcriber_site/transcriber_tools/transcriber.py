import whisper
import os
from pydub import AudioSegment
from pydub.silence import split_on_silence
import moviepy.editor as mp
from pydub import AudioSegment
import zipfile

from .pdf import txt_to_docx
from .summ import summarize_russian_text_from_file

def zip_directory(directory_path, zip_filename):
        with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(directory_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    zipf.write(file_path, os.path.relpath(file_path, directory_path))

def unzip_archive(zip_filename, extract_to):
        if not os.path.isfile(zip_filename):
            print(f"Файл '{zip_filename}' не найден.")
            return
        
        if not os.path.exists(extract_to):
            os.makedirs(extract_to)
        
        with zipfile.ZipFile(zip_filename, 'r') as zipf:
            zipf.extractall(extract_to)
            print(f"Архив '{zip_filename}' успешно извлечен в '{extract_to}'.")


def transcribation(zipname):
    input_directory = 'uploads'

    def video_to_audio(in_path, out_path):
        
        video = mp.VideoFileClip(in_path)
        video.audio.write_audiofile(out_path)
        

    
    FRAME_RATE = 16000
    CHANNELS=1

    for filename in os.listdir(input_directory):
        if filename.endswith('.zip'):
            zipfile = os.path.join(input_directory, filename)
            unzip_archive(zipfile, 'uploads')
        else:
            pass

    for filename in os.listdir(input_directory):
        if filename.endswith(('.mp4', '.mov', '.webp', '.webm', '.avi')):
            input_file_path = os.path.join(input_directory, filename)
            print(input_file_path)
            
            video_to_audio(input_file_path, 'audio.mp3')

            
            mp3 = AudioSegment.from_mp3('audio.mp3')
            mp3 = mp3.set_channels(CHANNELS)
            mp3 = mp3.set_frame_rate(FRAME_RATE)

            
            model = whisper.load_model("large-v3")

            
            result = model.transcribe('audio.mp3')

            with open('data.txt', 'w', encoding='utf-8') as file:
                file.write(result['text'])
            
        elif filename.endswith(('.mp3', '.wav', '.m4a', '.dvf')):
            input_file_path = os.path.join(input_directory, filename)
            print(input_file_path)

           
            mp3 = AudioSegment.from_mp3(input_file_path)
            mp3 = mp3.set_channels(CHANNELS)
            mp3 = mp3.set_frame_rate(FRAME_RATE)

            
            model = whisper.load_model("large-v3")

            
            result = model.transcribe('audio.mp3')

            with open('data.txt', 'w', encoding='utf-8') as file:
                file.write(result['text'])

    input_file = "data.txt"
    summarize_russian_text_from_file(input_file, 'summary.txt')
    input_file_2 = "summary.txt"
    txt_to_docx(input_file_2, 'final/summary.docx')
    txt_to_docx(input_file, 'final/data.docx')

    directory_to_zip = 'final'
    zip_filename = 'result.zip'
    zip_directory(directory_to_zip, zip_filename)

    processed_file_path = "processed_" + zip_filename  
    return processed_file_path
