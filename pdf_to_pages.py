import argparse
import os
from pathlib import Path
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTImage # Corrected import: Use LTImage from pdfminer.layout
from PIL import Image as PILImage
import pytesseract
import io # Keep this import for image handling

# ... (rest of the code remains the same)

def ocr_pdf_to_text(
    pdf_path: Path,
    page_range: tuple[int, int] | None = None,
    output_dir: Path | None = None,
    split_pages: bool = False,
) -> None:
    """
    Performs OCR on a PDF file and extracts text.

    Args:
        pdf_path: Path to the input PDF file.
        page_range: A tuple (start_page, end_page) for specific pages, 1-indexed.
                    If None, all pages are processed.
        output_dir: Directory to save the output text files. If None, a directory
                    named after the PDF (without extension) will be created.
        split_pages: If True, each page is saved to a separate text file.
                     If False, all extracted text is saved to a single file.
    """
    if not pdf_path.is_file():
        print(f"Error: PDF file not found at '{pdf_path}'")
        return

    # Determine output directory
    if output_dir is None:
        output_dir = pdf_path.stem
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    print(f"Processing PDF: '{pdf_path}'")
    print(f"Output directory: '{output_path}'")

    all_text_content: list[str] = []
    page_count = 0

    try:
        # pdfminer.six page indexing starts from 0, adjust for 1-indexed user input
        start_page = page_range[0] - 1 if page_range else 0
        end_page = page_range[1] - 1 if page_range else float('inf')

        for i, page_layout in enumerate(extract_pages(str(pdf_path))):
            if not (start_page <= i <= end_page):
                continue
            
            page_count += 1
            print(f"  Processing page {i + 1}...")
            
            page_text_content: list[str] = []

            for element in page_layout:
                # Corrected check: Use LTImage from pdfminer.layout
                if isinstance(element, LTImage): 
                    # Extract image data
                    image_bytes = element.stream.get_data()
                    try:
                        # Use Pillow to open image from bytes
                        img = PILImage.open(io.BytesIO(image_bytes))
                        # Perform OCR on the image
                        text = pytesseract.image_to_string(img)
                        page_text_content.append(text)
                    except Exception as img_exc:
                        print(f"    Warning: Could not process image on page {i + 1}: {img_exc}")
                else:
                    # Directly extract text from text elements
                    try:
                        text = element.get_text()
                        page_text_content.append(text)
                    except AttributeError:
                        # Element might not have get_text() method (e.g., Line, Rect)
                        pass
            
            page_combined_text = "\n".join(page_text_content).strip()
            all_text_content.append(f"--- Page {i + 1} ---\n{page_combined_text}\n")

            if split_pages:
                page_output_filename = output_path / f"page_{i + 1}.txt"
                with open(page_output_filename, "w", encoding="utf-8") as f:
                    f.write(page_combined_text)
                print(f"    Saved page {i + 1} to '{page_output_filename}'")

    except Exception as e:
        print(f"An error occurred during PDF processing: {e}")
        return
    
    if not split_pages:
        combined_output_filename = output_path / f"{pdf_path.stem}_combined.txt"
        with open(combined_output_filename, "w", encoding="utf-8") as f:
            f.write("\n\n".join(all_text_content))
        print(f"Saved combined text to '{combined_output_filename}'")
    
    if page_count == 0:
        print("No pages processed within the specified range.")
    else:
        print(f"Successfully processed {page_count} page(s).")


def main():
    parser = argparse.ArgumentParser(
        description="Perform OCR on PDF pages using Tesseract."
    )
    parser.add_argument("pdf_file", type=str, help="Path to the input PDF file.")
    parser.add_argument(
        "--page-range",
        type=str,
        help="Page range to process (e.g., '1-5'). Processes all pages if not specified.",
    )
    parser.add_argument(
        "--output",
        "-o",
        type=str,
        help="Output directory for text files. Defaults to a folder named after the PDF.",
    )
    parser.add_argument(
        "--split",
        action="store_true",
        help="Split output into multiple text files (one per page). "
        "By default, all text is combined into a single file.",
    )

    args = parser.parse_args()

    pdf_path = Path(args.pdf_file)
    page_range: tuple[int, int] | None = None
    if args.page_range:
        try:
            start, end = map(int, args.page_range.split("-"))
            if start <= 0 or end <= 0:
                raise ValueError("Page numbers must be positive.")
            if start > end:
                raise ValueError("Start page cannot be greater than end page.")
            page_range = (start, end)
        except ValueError as e:
            print(f"Error: Invalid page range format. Please use 'start-end' (e.g., '1-5'). {e}")
            return

    output_dir: Path | None = Path(args.output) if args.output else None

    ocr_pdf_to_text( # removed the `import io` from here, as it's already at the top
        pdf_path=pdf_path,
        page_range=page_range,
        output_dir=output_dir,
        split_pages=args.split,
    )

if __name__ == "__main__":
    main()
