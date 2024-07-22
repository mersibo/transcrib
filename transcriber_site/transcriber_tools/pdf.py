import docx
import sys
import os
from docx import Document

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def txt_to_docx(input_file, output_file):
    # Correctly get the absolute paths
    input_txt_file = resource_path(input_file)
    output_docx_file = resource_path(output_file)

    # Check if input file exists
    if not os.path.exists(input_txt_file):
        print(f"Input file does not exist: {input_txt_file}")
        return

    # Read the content of the input file
    with open(input_txt_file, "r", encoding="utf-8") as f:
        content = f.read()

    # Check if content is empty
    if not content:
        print(f"Input file is empty: {input_txt_file}")
        return

    # Create a new Document
    doc = Document()

    # Add content to the document
    doc.add_paragraph(content)

    # Save the document in DOCX format
    doc.save(output_docx_file)
    print("DOCX file successfully created:", output_docx_file)
