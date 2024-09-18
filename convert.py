import json
import os
import re
import sys

import PyPDF2

# Function to convert PDF to text and append to vault.txt


def convert_pdf_to_text(file_path):
    if file_path:
        with open(file_path, 'rb') as pdf_file:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            num_pages = len(pdf_reader.pages)
            text = ''
            for page_num in range(num_pages):
                page = pdf_reader.pages[page_num]
                if page.extract_text():
                    text += page.extract_text() + " "

            # Normalize whitespace and clean up text
            text = re.sub(r'\s+', ' ', text).strip()

            # Split text into chunks by sentences, respecting a maximum chunk size
            # split on spaces following sentence-ending punctuation
            sentences = re.split(r'(?<=[.!?]) +', text)
            chunks = []
            current_chunk = ""
            for sentence in sentences:
                # Check if the current sentence plus the current chunk exceeds the limit
                if len(current_chunk) + len(sentence) + 1 < 1000:  # +1 for the space
                    current_chunk += (sentence + " ").strip()
                else:
                    # When the chunk exceeds 1000 characters, store it and start a new one
                    chunks.append(current_chunk)
                    current_chunk = sentence + " "
            if current_chunk:  # Don't forget the last chunk!
                chunks.append(current_chunk)
            with open("vault.txt", "a", encoding="utf-8") as vault_file:
                for chunk in chunks:
                    # Write each chunk to its own line
                    # Two newlines to separate chunks
                    vault_file.write(chunk.strip() + "\n")
            print(
                f"PDF content appended to vault.txt with each chunk on a separate line.")

# Function to upload a text file and append to vault.txt


def upload_txtfile(file_path):
    if file_path:
        with open(file_path, 'r', encoding="utf-8") as txt_file:
            text = txt_file.read()

            # Normalize whitespace and clean up text
            text = re.sub(r'\s+', ' ', text).strip()

            # Split text into chunks by sentences, respecting a maximum chunk size
            # split on spaces following sentence-ending punctuation
            sentences = re.split(r'(?<=[.!?]) +', text)
            chunks = []
            current_chunk = ""
            for sentence in sentences:
                # Check if the current sentence plus the current chunk exceeds the limit
                if len(current_chunk) + len(sentence) + 1 < 1000:  # +1 for the space
                    current_chunk += (sentence + " ").strip()
                else:
                    # When the chunk exceeds 1000 characters, store it and start a new one
                    chunks.append(current_chunk)
                    current_chunk = sentence + " "
            if current_chunk:  # Don't forget the last chunk!
                chunks.append(current_chunk)
            with open("vault.txt", "a", encoding="utf-8") as vault_file:
                for chunk in chunks:
                    # Write each chunk to its own line
                    # Two newlines to separate chunks
                    vault_file.write(chunk.strip() + "\n")
            print(
                f"Text file content appended to vault.txt with each chunk on a separate line.")


if __name__ == "__main__":
    print("This is the main function")
    if len(sys.argv) > 1:
        filename = sys.argv[1]
        if filename.endswith(".txt"):
            print("Text file detected")
            upload_txtfile(filename)
        elif filename.endswith(".pdf"):
            print("PDF file detected")
            convert_pdf_to_text(filename)
