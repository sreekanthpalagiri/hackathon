from unstructured.documents import document

def process_pdf_pages(pdf_path):
    """
    Processes a PDF file page by page using the Unstructured library.

    Args:
        pdf_path: Path to the PDF file.

    Returns:
        A list of dictionaries, where each dictionary represents the processed data 
        from a single page of the PDF.
    """

    try:
        pdf_doc = Document.from_file(pdf_path)
        pages = pdf_doc.pages

        processed_pages = []
        for page in pages:
            page_data = page.process()
            processed_pages.append(page_data)

        return processed_pages

    except Exception as e:
        print(f"An error occurred while processing the PDF: {e}")
        return []

# Example usage
pdf_file_path = "Saraswathi - Application Summary.pdf" 
processed_data = process_pdf_pages(pdf_file_path)

# Process and print data from each page
for page_num, page_data in enumerate(processed_data):
    print(f"Page {page_num + 1}:")
    print(page_data)