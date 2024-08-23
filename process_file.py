import os
import argparse
import anthropic
from pathlib import Path

def process_file(file_path, output_dir, prompt):
    client = anthropic.Client(os.environ["ANTHROPIC_API_KEY"])
    
    with open(file_path, 'rb') as file:
        response = client.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=1000,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": "application/octet-stream",
                                "data": file.read().encode("base64")
                            }
                        },
                        {
                            "type": "text",
                            "text": prompt
                        }
                    ]
                }
            ]
        )
    
    output_file = Path(output_dir) / f"{Path(file_path).stem}_summary.txt"
    with open(output_file, 'w') as f:
        f.write(response.content[0].text)
    
    print(f"Processed {file_path}. Summary saved to {output_file}")

def main():
    parser = argparse.ArgumentParser(description="Process files with Claude API and save summaries.")
    parser.add_argument("input", help="Input file or directory")
    parser.add_argument("output", help="Output directory for summaries")
    parser.add_argument("prompt", help="Text prompt to send with each file")
    args = parser.parse_args()

    input_path = Path(args.input)
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    if input_path.is_file():
        process_file(input_path, output_dir, args.prompt)
    elif input_path.is_dir():
        for file in input_path.glob('*'):
            if file.is_file():
                process_file(file, output_dir, args.prompt)
    else:
        print(f"Error: {args.input} is not a valid file or directory")

if __name__ == "__main__":
    main()
