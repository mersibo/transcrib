import transformers
import sys
import os
from transformers import T5Tokenizer, T5ForConditionalGeneration

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def summarize_russian_text_with_mT5(text, min_length=500, max_length=1650):
    model_name = 'csebuetnlp/mT5_multilingual_XLSum'
    tokenizer = T5Tokenizer.from_pretrained(model_name)
    model = T5ForConditionalGeneration.from_pretrained(model_name)

    inputs = tokenizer.encode("summarize: " + text, return_tensors="pt", max_length=512, truncation=True)

    summary_ids = model.generate(
        inputs, 
        min_length=min_length, 
        max_length=max_length, 
        num_beams=4, 
        length_penalty=2.0, 
        early_stopping=True
    )

    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    return summary

def summarize_russian_text_from_file(input_file_path, output_file_path, min_length=500, max_length=1650):
    input_file = resource_path(input_file_path)
    output_file = resource_path(output_file_path)

    if not os.path.exists(input_file):
        print(f"Input file does not exist: {input_file}")
        return

    with open(input_file, 'r', encoding='utf-8') as file:
        text = file.read()

    if not text:
        print(f"Input file is empty: {input_file}")
        return

    summary = summarize_russian_text_with_mT5(text, min_length=min_length, max_length=max_length)

    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(summary)
    print(f"Summary written to: {output_file}")
