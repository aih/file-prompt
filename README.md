The process_file.py script uses the Anthropic library to interact with the Claude API. It handles uploading a single file along with the text prompt to the Claude API and saves the response to a specified path.
The main function sets up argument parsing and can handle both single files and directories.
If a directory is provided, it processes all files in that directory.
The summary for each file is saved in the specified output directory with the naming convention original_filename_summary.txt.

To use this script, you'll need to:

Install the required libraries: pip install -r requirements.txt 
Create a .env file and set your Anthropic API key as an environment variable there: ANTHROPIC_API_KEY='your-api-key-here'

You can run the script like this:
python script_name.py input_file_or_directory output_directory "Your prompt here"
If you leave the prompt blank, the script will use the default prompt in `prompts/bill_summary_prompts.py` 
For example:
python claude_summarizer.py /path/to/input /path/to/output "Summarize the contents of this file"
This script provides a flexible solution that can handle both single files and entire directories. It also uses argparse for better command-line interaction.
