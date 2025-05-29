import requests
import fitz  # PyMuPDF
import os
import logging
from datetime import datetime

def setup_logger():
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    log_filename = f"output-logs-{timestamp}.log"
    logging.basicConfig(
        filename=log_filename,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )
    return log_filename

def download_pdf(url, output_path):
    try:
        logging.info(f"Starting download from: {url}")
        with requests.get(url, stream=True, timeout=60) as r:
            r.raise_for_status()
            with open(output_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        logging.info(f"Download completed: {output_path}")
        return True
    except requests.exceptions.RequestException as e:
        logging.error(f"Download failed: {e}")
        return False

def extract_text_to_single_file(pdf_path, output_file):
    try:
        logging.info(f"Opening PDF for extraction: {pdf_path}")
        doc = fitz.open(pdf_path)

        with open(output_file, "w", encoding="utf-8") as f_out:
            for page_num in range(len(doc)):
                try:
                    page = doc[page_num]
                    text = page.get_text()
                    f_out.write(f"\n--- Page {page_num + 1} ---\n")
                    f_out.write(text)
                    f_out.write("\n")
                    logging.info(f"Extracted page {page_num + 1}/{len(doc)}")
                except Exception as e:
                    logging.warning(f"Failed to extract page {page_num + 1}: {e}")

        logging.info(f"Extraction complete. Output saved to: {output_file}")
    except Exception as e:
        logging.error(f"Failed to process PDF: {e}")

if __name__ == "__main__":
    from time import time

    # 🔄 Replace this with your actual PDF URL
    PDF_URL = "https://example.com/your_large_file.pdf"
    LOCAL_PDF_PATH = "large_file.pdf"
    OUTPUT_TEXT_FILE = "all_text_output.txt"

    log_file = setup_logger()
    logging.info("=== PDF Processing Started ===")
    start_time = datetime.now()
    t0 = time()

    if download_pdf(PDF_URL, LOCAL_PDF_PATH):
        extract_text_to_single_file(LOCAL_PDF_PATH, OUTPUT_TEXT_FILE)

    end_time = datetime.now()
    elapsed = time() - t0
    logging.info(f"Start time: {start_time}")
    logging.info(f"End time: {end_time}")
    logging.info(f"Elapsed time: {elapsed:.2f} seconds")
    logging.info("=== PDF Processing Finished ===")

    print(f"Processing complete. Log file saved as: {log_file}")