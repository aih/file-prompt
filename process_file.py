import os
import argparse
import anthropic
from pathlib import Path
import PyPDF2
from prompts.bill_summary_prompts import bill_synopsis
from dotenv import load_dotenv

load_dotenv()

def extract_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfFileReader(file)
        pages = reader.pages
        pdftext = "".join([page.extractText() for page in pages])
    return pdftext

def process_file(file_path, output_dir, prompt=bill_synopsis):
    client = anthropic.Client(api_key=os.environ["ANTHROPIC_API_KEY"])
    
    try:
        pdf_content = extract_text_from_pdf(file_path)
    except Exception as e:
        print(f"Error processing {file_path}: {str(e)}")
        return

    response = client.messages.create(
        model="claude-3-opus-20240229",
        max_tokens=1000,
        messages=[
            {
                "role": "user",
                "content": f"{prompt}\n\nPDF content:\n{pdf_content[:10000]}"
            }
        ]
    )
    
    output_file = Path(output_dir) / f"{Path(file_path).stem}_summary.txt"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(response.content[0].text)
    
    print(f"Processed {file_path}. Summary saved to {output_file}")

def main():
    parser = argparse.ArgumentParser(description="Process PDF files with Claude API and save summaries.")
    parser.add_argument("input", help="Input PDF file or directory containing PDF files")
    parser.add_argument("output", help="Output directory for summaries")
    parser.add_argument("--prompt", required=False, help="Text prompt to send with each file")
    args = parser.parse_args()

    input_path = Path(args.input)
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    if input_path.is_file():
        if input_path.suffix.lower() == '.pdf':
            if args.prompt:
                process_file(input_path, output_dir, args.prompt)
            else:
                process_file(input_path, output_dir)
                
        else:
            print(f"Error: {args.input} is not a PDF file")
    elif input_path.is_dir():
        for file in input_path.glob('*.pdf'):
            process_file(file, output_dir, args.prompt)
    else:
        print(f"Error: {args.input} is not a valid file or directory")

if __name__ == "__main__":
    main()