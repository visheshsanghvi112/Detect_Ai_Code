#for normally detetcting the ai code 
import os
import time
import re
import logging
from datetime import datetime
from collections import Counter
from spellchecker import SpellChecker
from tqdm import tqdm
import concurrent.futures
from tkinter import Tk
from tkinter.filedialog import askdirectory
import nltk
import language_tool_python
import matplotlib.pyplot as plt
from fpdf import FPDF

# Set up logging
logging.basicConfig(filename='code_analysis.log', level=logging.INFO, format='%(asctime)s - %(message)s')

# Initialize spell checker and grammar checker
spell = SpellChecker()
tool = language_tool_python.LanguageTool('en-US')

# Global variables for file processing stats
total_files = 0
completed_files = 0
total_ai_lines = 0
total_human_lines = 0
total_generic_count = 0
total_comments = 0
total_misspelled_words = 0
ai_percentages = []
human_percentages = []

# Common generic names found in AI-generated code
generic_variable_names = ['temp', 'data', 'result', 'item', 'value', 'process']

# Download NLTK data for sentence tokenization
nltk.download('punkt')

def analyze_code(file_path):
    global completed_files, total_ai_lines, total_human_lines, total_generic_count, total_comments, total_misspelled_words, ai_percentages, human_percentages
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            code = file.read()

        # Analyzing code
        total_lines = len(code.splitlines())
        human_lines = 0
        ai_lines = 0
        comments = []
        code_structure = {'indentation': 0, 'loops': 0, 'functions': 0}
        generic_variable_count = 0

        lines = code.splitlines()
        for line in lines:
            stripped_line = line.strip()
            if len(stripped_line) == 0:
                continue  # Skip empty lines

            # Check for comments
            if stripped_line.startswith('#'):
                comments.append(stripped_line)
                # Check if comment is human-like
                if len(stripped_line.split()) < 5 or not all(word[0].islower() for word in stripped_line.split()):
                    human_lines += 1
                else:
                    ai_lines += 1

            # Check for loops and functions
            if re.match(r'^\s*for.*|^\s*while.*', stripped_line):
                code_structure['loops'] += 1
                ai_lines += 1
            elif re.match(r'^\s*def ', stripped_line):
                code_structure['functions'] += 1
                ai_lines += 1
            elif re.match(r'^\s*class ', stripped_line):
                code_structure['functions'] += 1
                ai_lines += 1
            else:
                # Check for human-like features in code
                if re.match(r'^\s{4}.*', stripped_line):  # Check for 4-space indentation
                    code_structure['indentation'] += 1
                    human_lines += 1
                else:
                    ai_lines += 1

                # Check for generic variable names
                generic_variable_count += check_generic_variable_names(stripped_line)

        # Spell checking in comments
        misspelled = spell.unknown(re.findall(r'\b\w+\b', ' '.join(comments)))
        ai_like = ai_lines / total_lines * 100
        human_like = human_lines / total_lines * 100

        # Grammar checking in comments
        grammar_errors = sum([len(tool.check(comment)) for comment in comments])

        # Update totals for global analysis
        total_ai_lines += ai_lines
        total_human_lines += human_lines
        total_generic_count += generic_variable_count
        total_comments += len(comments)
        total_misspelled_words += len(misspelled)

        # Store data for visualization
        ai_percentages.append(ai_like)
        human_percentages.append(human_like)

        # Reporting
        logging.info(f"File analyzed: {file_path}")
        logging.info(f"Human-like lines: {human_like:.2f}% ({human_lines} lines)")
        logging.info(f"AI-like lines: {ai_like:.2f}% ({ai_lines} lines)")
        logging.info(f"Generic variable names found: {generic_variable_count}")
        logging.info(f"Detected {code_structure['loops']} loops and {code_structure['functions']} functions.")
        logging.info(f"Misspelled words in comments: {misspelled}")
        logging.info(f"Grammar errors in comments: {grammar_errors}")

        # Updating the progress
        completed_files += 1
        display_progress()

    except Exception as e:
        logging.error(f"Error processing {file_path}: {e}")
        print(f"Error processing {file_path}: {e}")

def check_generic_variable_names(line):
    generic_variable_count = 0
    for word in line.split():
        if word.lower() in generic_variable_names:
            generic_variable_count += 1
    return generic_variable_count

def display_progress():
    global total_files, completed_files
    progress = (completed_files / total_files) * 100
    print(f"Progress: {completed_files}/{total_files} files processed ({progress:.2f}%)")

def display_final_conclusion():
    global total_files, total_ai_lines, total_human_lines
    total_lines_analyzed = total_ai_lines + total_human_lines
    if total_lines_analyzed == 0:
        print("No code to analyze.")
        return

    ai_percentage = (total_ai_lines / total_lines_analyzed) * 100
    human_percentage = (total_human_lines / total_lines_analyzed) * 100

    print(f"\n\n--- Final Conclusion ---")
    print(f"Total Files Analyzed: {total_files}")
    print(f"AI-like code: {ai_percentage:.2f}% ({total_ai_lines} lines)")
    print(f"Human-like code: {human_percentage:.2f}% ({total_human_lines} lines)")
    print(f"Generic variable names detected: {total_generic_count}")
    print(f"Total misspelled words in comments: {total_misspelled_words}")
    
    if ai_percentage > 70:
        print("Conclusion: The code is likely AI-generated with a high percentage of AI-like patterns.")
    elif human_percentage > 70:
        print("Conclusion: The code appears to be mostly human-written.")
    else:
        print("Conclusion: The code contains a mix of both human-written and AI-generated elements.")

def generate_pdf_report():
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, "Code Analysis Report", ln=True, align="C")
    pdf.ln(10)

    # Adding analysis summary
    pdf.set_font("Arial", '', 12)
    pdf.cell(200, 10, f"Total Files Analyzed: {total_files}", ln=True)
    pdf.cell(200, 10, f"AI-like code: {total_ai_lines} lines", ln=True)
    pdf.cell(200, 10, f"Human-like code: {total_human_lines} lines", ln=True)
    pdf.cell(200, 10, f"Generic variable names detected: {total_generic_count}", ln=True)
    pdf.cell(200, 10, f"Total misspelled words in comments: {total_misspelled_words}", ln=True)
    pdf.ln(10)

    # Plotting AI vs Human percentage
    plt.figure(figsize=(6, 4))
    plt.plot(ai_percentages, label="AI-like code")
    plt.plot(human_percentages, label="Human-like code")
    plt.xlabel('File Index')
    plt.ylabel('Percentage')
    plt.title('AI vs Human Code Percentage')
    plt.legend()
    plt.savefig("code_analysis_chart.png")
    plt.close()

    pdf.image("code_analysis_chart.png", x=10, y=pdf.get_y(), w=180)
    pdf.output("code_analysis_report.pdf")
    print("PDF report generated as code_analysis_report.pdf")

def process_folder(folder_path):
    global total_files, completed_files
    files_to_analyze = []

    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.py') or file.endswith('.js') or file.endswith('.java'):
                files_to_analyze.append(os.path.join(root, file))

    total_files = len(files_to_analyze)
    completed_files = 0

    if total_files == 0:
        print("No files to analyze.")
        return

    # Display initial information
    print(f"Total files to analyze: {total_files}")
    
    # Analyze all files with a progress bar
    with concurrent.futures.ThreadPoolExecutor() as executor:
        list(tqdm(executor.map(analyze_code, files_to_analyze), total=total_files, desc="Analyzing Files"))

def select_folder():
    # Use tkinter to open a folder dialog and return the folder path
    Tk().withdraw()  # Hide the root window
    folder_path = askdirectory(title="Select Folder")  # Open folder selection dialog
    return folder_path

def main():
    # Ask user to select a folder
    folder_path = select_folder()

    if not folder_path:
        print("No folder selected. Exiting...")
        return

    # Analyze the folder
    process_folder(folder_path)
    
    # Generate the final conclusion and save the PDF report
    display_final_conclusion()
    generate_pdf_report()

if __name__ == '__main__':
    main()