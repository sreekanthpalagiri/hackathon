import os
import requests
from PyPDF2 import PdfReader

def extract_pdf_sections(pdf_path):
    """
    Extracts sections from the PDF. In this example, each page is treated as a section.
    
    :param pdf_path: Path to the PDF file.
    :return: List of sections' text.
    """
    reader = PdfReader(pdf_path)
    sections = []
    for page_num, page in enumerate(reader.pages, start=1):
        text = page.extract_text()
        if text:
            sections.append((page_num, text))
        else:
            sections.append((page_num, ""))
    return sections

def upload_section(section_number, text, upload_url):
    """
    Uploads a section to the specified server endpoint.
    
    :param section_number: The section or page number.
    :param text: The text content of the section.
    :param upload_url: The URL of the server endpoint that accepts the upload.
    :return: The server's response object.
    """
    # Prepare a payload. You can modify the payload structure as required by your server.
    payload = {
        "section_number": section_number,
        "content": text
    }
    try:
        #response = requests.post(upload_url, json=payload)
        #response.raise_for_status()  # Raise an exception for HTTP errors.
        response='H'
        print(payload)
        print('------------------------')
        return response
    except requests.exceptions.RequestException as e:
        print(f"Error uploading section {section_number}: {e}")
        return None

if __name__ == "__main__":
    # Path to your PDF file
    pdf_file_path = "generative-ai-insurance-use-cases-writer-com.pdf"
    
    # URL of the remote server where the section should be uploaded.
    # Replace this with your actual endpoint.
    UPLOAD_URL = "https://example.com/api/upload_section"
    
    # Extract sections from the PDF.
    sections = extract_pdf_sections(pdf_file_path)
    
    for section_number, text in sections:
        print(f"Uploading section {section_number}...")
        response = upload_section(section_number, text, UPLOAD_URL)
        if response is not None:
            print(f"Section {section_number} uploaded successfully. Server responded with: {response}")
        else:
            print(f"Failed to upload section {section_number}.")
