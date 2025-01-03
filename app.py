import os
import re
from flask import Flask, render_template, request
import language_tool_python

app = Flask(__name__)

# Initialize LanguageTool for grammar and spell checking
tool = language_tool_python.LanguageTool('en-US')

# Folder to save uploaded files (we are not uploading files now, just analyzing from folder)
ALLOWED_EXTENSIONS = {'txt', 'py', 'java', 'js', 'cpp', 'html', 'css', 'php'}

# Check if a file is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# AI Code Detection Functions

def check_perfect_formatting(code):
    lines = code.splitlines()
    indentations = [len(line) - len(line.lstrip()) for line in lines if line.strip()]
    if len(indentations) == 0:
        return False
    consistent_indentations = sum([1 for indentation in indentations if indentation == indentations[0]]) / len(indentations)
    return consistent_indentations >= 0.80  # Check if 80% indentation consistency is met

def check_comment_grammar(code):
    comments = re.findall(r'#.*', code)
    issues = 0
    for comment in comments:
        matches = tool.check(comment)
        issues += len(matches)
    return issues > 2  # If there are more than 2 grammar issues in comments, likely AI-generated

def check_library_usage(code):
    common_ai_libraries = ['numpy', 'pandas', 'matplotlib', 'tensorflow', 'keras', 'sklearn']
    found_libraries = [lib for lib in common_ai_libraries if lib in code]
    return len(found_libraries) > 2

def check_repetitiveness(code):
    function_pattern = re.compile(r'\bdef\b')
    function_definitions = re.findall(function_pattern, code)
    
    variable_pattern = re.compile(r'\b[a-zA-Z_][a-zA-Z0-9_]*\b')
    variable_names = re.findall(variable_pattern, code)
    
    common_variable_names = {'temp', 'result', 'value', 'data', 'item', 'count', 'i', 'j'}
    suspicious_variables = set(common_variable_names) & set(variable_names)
    
    return len(function_definitions) > 5 or len(suspicious_variables) > 2

def check_code_complexity(code):
    complexity_pattern = re.compile(r'\{.*\}', re.DOTALL)
    nested_blocks = re.findall(complexity_pattern, code)
    return len(nested_blocks) > 3

def check_repeated_patterns(code):
    patterns = re.findall(r'(\b\w+\b)(?:\s*\(.*\))?\s*(?:\{.*\}){2,}', code)
    return len(patterns) > 2

def check_magic_numbers(code):
    magic_numbers = re.findall(r'\b\d+\b', code)
    return len(magic_numbers) > 5

# New Functions for Expanded AI Detection

def check_commit_history(file_path):
    # This can analyze commit history in a Git repository, 
    # or inspect version control metadata in files
    # Placeholder function for commit analysis
    return False  # Assume no suspicious commit history

def check_tooling_and_formatting(code):
    # Checks if automated tools like Prettier, Black, or IDE formatting plugins are used
    # Placeholder for automated formatting check
    return False  # Assume no automated tooling detected

def check_file_dependencies(code):
    # Check for clear file dependencies (cross-file references)
    return len(re.findall(r'import', code)) > 2  # Example: Too many imports may indicate AI usage

def check_variable_naming_patterns(code):
    # Check for overly generic variable names or suspicious patterns
    common_patterns = re.findall(r'var[0-9]{3}', code)  # Example: var001, var002...
    return len(common_patterns) > 2

def check_algorithm_patterns(code):
    # Detect algorithmic patterns that are typical in AI-generated code
    return 'for' in code and 'range' in code  # Example: AI often generates for loops with range()

def check_refactoring_patterns(code):
    # AI tends to refactor code consistently across multiple files
    return len(re.findall(r'function|class', code)) > 5

def detect_ai_generated_code(code, file_path=None):
    # Basic checks (indented, comments, complexity, etc.)
    checks = {
        'formatting': check_perfect_formatting(code),
        'comments': check_comment_grammar(code),
        'library_usage': check_library_usage(code),
        'repetitiveness': check_repetitiveness(code),
        'complexity': check_code_complexity(code),
        'patterns': check_repeated_patterns(code),
        'magic_numbers': check_magic_numbers(code),
        'commit_history': check_commit_history(file_path),
        'tooling_and_formatting': check_tooling_and_formatting(code),
        'file_dependencies': check_file_dependencies(code),
        'variable_naming': check_variable_naming_patterns(code),
        'algorithm_patterns': check_algorithm_patterns(code),
        'refactoring_patterns': check_refactoring_patterns(code)
    }

    # Count the checks that passed
    ai_likelihood = sum(checks.values()) / len(checks) * 100

    # Determine if code is AI-generated
    is_ai_generated = ai_likelihood >= 30

    # Create a short analysis report
    analysis_report = f"The code is {'AI-generated' if is_ai_generated else 'human-written'} based on our analysis."
    
    return {
        'is_ai_generated': is_ai_generated,
        'ai_percentage': ai_likelihood,
        'analysis_summary': analysis_report
    }

# File upload and analysis route
@app.route('/analyze_files', methods=['POST'])
def analyze_files():
    if 'files' not in request.files:
        return render_template('index.html', message="No files selected.")
    
    files = request.files.getlist('files')
    if not files:
        return render_template('index.html', message="No files selected.")
    
    analysis_results = []

    for file in files:
        if allowed_file(file.filename):
            file_content = file.read().decode('utf-8')

            # Analyze the code
            analysis = detect_ai_generated_code(file_content, file_path=file.filename)

            result = {
                'filename': file.filename,
                'is_ai_generated': analysis['is_ai_generated'],
                'ai_percentage': analysis['ai_percentage'],
                'analysis_summary': analysis['analysis_summary']
            }
            analysis_results.append(result)
    
    return render_template('analysis_results.html', analysis_results=analysis_results)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
