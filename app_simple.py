import os
import re
import ast
import json
import hashlib
from datetime import datetime
from flask import Flask, render_template, request, jsonify
import numpy as np

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Simple in-memory storage for demo purposes
analysis_results = []

# Enhanced AI Detection Class
class AdvancedAIDetector:
    def __init__(self):
        pass
        
    def extract_features(self, code):
        """Extract comprehensive features from code"""
        features = {}
        
        # Basic metrics
        features['lines_of_code'] = len(code.splitlines())
        features['characters'] = len(code)
        features['words'] = len(code.split())
        
        # Code structure analysis
        features.update(self._analyze_code_structure(code))
        
        # Comment analysis
        features.update(self._analyze_comments(code))
        
        # Variable and function analysis
        features.update(self._analyze_naming_patterns(code))
        
        # Complexity analysis
        features.update(self._analyze_complexity(code))
        
        # Style consistency
        features.update(self._analyze_style_consistency(code))
        
        # Semantic patterns
        features.update(self._analyze_semantic_patterns(code))
        
        return features
    
    def _analyze_code_structure(self, code):
        """Analyze code structure and formatting"""
        lines = code.splitlines()
        non_empty_lines = [line for line in lines if line.strip()]
        
        # Indentation analysis
        indentations = [len(line) - len(line.lstrip()) for line in non_empty_lines]
        avg_indentation = np.mean(indentations) if indentations else 0
        indent_consistency = np.std(indentations) if len(indentations) > 1 else 0
        
        # Line length analysis
        line_lengths = [len(line) for line in non_empty_lines]
        avg_line_length = np.mean(line_lengths) if line_lengths else 0
        max_line_length = max(line_lengths) if line_lengths else 0
        
        return {
            'avg_indentation': avg_indentation,
            'indent_consistency': indent_consistency,
            'avg_line_length': avg_line_length,
            'max_line_length': max_line_length,
            'empty_lines_ratio': (len(lines) - len(non_empty_lines)) / len(lines) if lines else 0
        }
    
    def _analyze_comments(self, code):
        """Analyze comment patterns and quality"""
        # Extract comments
        python_comments = re.findall(r'#.*', code)
        docstring_comments = re.findall(r'""".*?"""', code, re.DOTALL)
        all_comments = python_comments + docstring_comments
        
        # Simple grammar check (count common grammar issues)
        comment_issues = 0
        for comment in python_comments:
            # Check for common grammar issues
            if re.search(r'\b(a\s+[aeiou]|an\s+[^aeiou])', comment, re.IGNORECASE):
                comment_issues += 1
            if re.search(r'\b(are|is)\s+\w+ing\b', comment, re.IGNORECASE):
                comment_issues += 1
        
        return {
            'comment_count': len(all_comments),
            'comment_ratio': len(all_comments) / len(code.splitlines()) if code.splitlines() else 0,
            'comment_grammar_issues': comment_issues,
            'has_docstrings': len(docstring_comments) > 0
        }
    
    def _analyze_naming_patterns(self, code):
        """Analyze variable and function naming patterns"""
        # Variable patterns
        variable_pattern = re.compile(r'\b[a-zA-Z_][a-zA-Z0-9_]*\b')
        variables = re.findall(variable_pattern, code)
        
        # Common AI-generated variable names
        ai_variable_patterns = [
            r'\bvar\d+\b',  # var1, var2, etc.
            r'\btemp\d*\b',  # temp, temp1, etc.
            r'\bresult\d*\b',  # result, result1, etc.
            r'\bdata\d*\b',   # data, data1, etc.
            r'\bvalue\d*\b',  # value, value1, etc.
        ]
        
        ai_variable_count = 0
        for pattern in ai_variable_patterns:
            ai_variable_count += len(re.findall(pattern, code, re.IGNORECASE))
        
        # Function patterns
        function_pattern = re.compile(r'\bdef\s+([a-zA-Z_][a-zA-Z0-9_]*)\b')
        functions = re.findall(function_pattern, code)
        
        return {
            'variable_count': len(set(variables)),
            'ai_variable_count': ai_variable_count,
            'function_count': len(functions),
            'avg_variable_length': np.mean([len(v) for v in variables]) if variables else 0,
            'avg_function_length': np.mean([len(f) for f in functions]) if functions else 0
        }
    
    def _analyze_complexity(self, code):
        """Analyze code complexity"""
        try:
            tree = ast.parse(code)
            complexity_metrics = self._calculate_cyclomatic_complexity(tree)
            return complexity_metrics
        except:
            return {
                'cyclomatic_complexity': 1,
                'nesting_depth': 1,
                'branch_count': 0
            }
    
    def _calculate_cyclomatic_complexity(self, tree):
        """Calculate cyclomatic complexity"""
        complexity = 1  # Base complexity
        
        for node in ast.walk(tree):
            if isinstance(node, (ast.If, ast.While, ast.For, ast.AsyncFor)):
                complexity += 1
            elif isinstance(node, ast.ExceptHandler):
                complexity += 1
            elif isinstance(node, ast.With):
                complexity += 1
        
        return {
            'cyclomatic_complexity': complexity,
            'nesting_depth': self._calculate_max_nesting(tree),
            'branch_count': complexity - 1
        }
    
    def _calculate_max_nesting(self, tree, current_depth=0, max_depth=0):
        """Calculate maximum nesting depth"""
        max_depth = max(max_depth, current_depth)
        
        for child in ast.iter_child_nodes(tree):
            if isinstance(child, (ast.If, ast.While, ast.For, ast.AsyncFor, ast.With)):
                max_depth = self._calculate_max_nesting(child, current_depth + 1, max_depth)
            else:
                max_depth = self._calculate_max_nesting(child, current_depth, max_depth)
        
        return max_depth
    
    def _analyze_style_consistency(self, code):
        """Analyze coding style consistency"""
        lines = code.splitlines()
        
        # Check for consistent spacing around operators
        operator_spacing = 0
        total_operators = 0
        
        for line in lines:
            operators = re.findall(r'[+\-*/=<>!&|]', line)
            total_operators += len(operators)
            
            for op in operators:
                if f' {op} ' in line or f'{op} ' in line or f' {op}' in line:
                    operator_spacing += 1
        
        spacing_consistency = operator_spacing / total_operators if total_operators > 0 else 1
        
        return {
            'operator_spacing_consistency': spacing_consistency,
            'consistent_indentation': self._check_indentation_consistency(lines)
        }
    
    def _check_indentation_consistency(self, lines):
        """Check if indentation is consistent"""
        indentations = []
        for line in lines:
            if line.strip():
                indentations.append(len(line) - len(line.lstrip()))
        
        if not indentations:
            return 1.0
        
        # Check if all indentations are multiples of a common factor
        min_indent = min(indentations)
        if min_indent == 0:
            return 0.5
        
        consistent_count = sum(1 for indent in indentations if indent % min_indent == 0)
        return consistent_count / len(indentations)
    
    def _analyze_semantic_patterns(self, code):
        """Analyze semantic patterns in code"""
        # Check for common AI-generated patterns
        ai_patterns = [
            r'for\s+\w+\s+in\s+range\s*\(',  # for i in range(
            r'if\s+__name__\s*==\s*[\'"]__main__[\'"]',  # if __name__ == "__main__"
            r'try:\s*\n\s*except\s+Exception',  # try/except patterns
            r'def\s+\w+\s*\([^)]*\):\s*\n\s*"""[^"]*"""',  # function with docstring
        ]
        
        pattern_matches = 0
        for pattern in ai_patterns:
            pattern_matches += len(re.findall(pattern, code, re.MULTILINE))
        
        # Check for library usage patterns
        common_libraries = ['numpy', 'pandas', 'matplotlib', 'tensorflow', 'sklearn', 'requests']
        library_count = sum(1 for lib in common_libraries if lib in code.lower())
        
        return {
            'ai_pattern_matches': pattern_matches,
            'common_library_count': library_count,
            'has_main_guard': bool(re.search(r'if\s+__name__\s*==\s*[\'"]__main__[\'"]', code))
        }
    
    def detect_ai_generated(self, code, filename=None):
        """Main detection method"""
        features = self.extract_features(code)
        
        # Calculate AI likelihood based on features
        ai_score = 0
        max_score = 0
        
        # Weighted scoring system
        scoring_rules = [
            # High weight indicators
            (features.get('ai_variable_count', 0) > 3, 20),
            (features.get('comment_grammar_issues', 0) > 2, 15),
            (features.get('common_library_count', 0) > 2, 10),
            (features.get('ai_pattern_matches', 0) > 2, 15),
            
            # Medium weight indicators
            (features.get('indent_consistency', 1) < 0.8, 8),
            (features.get('operator_spacing_consistency', 1) < 0.7, 8),
            (features.get('function_count', 0) > 5, 6),
            (features.get('cyclomatic_complexity', 1) > 5, 6),
            
            # Low weight indicators
            (features.get('avg_line_length', 0) > 100, 3),
            (features.get('max_line_length', 0) > 120, 3),
            (features.get('has_docstrings', False), 2),
            (features.get('has_main_guard', False), 2),
        ]
        
        for condition, weight in scoring_rules:
            max_score += weight
            if condition:
                ai_score += weight
        
        ai_percentage = (ai_score / max_score * 100) if max_score > 0 else 0
        is_ai_generated = ai_percentage >= 30
        
        return {
            'is_ai_generated': is_ai_generated,
            'ai_percentage': round(ai_percentage, 2),
            'features': features,
            'analysis_summary': self._generate_analysis_summary(features, ai_percentage)
        }
    
    def _generate_analysis_summary(self, features, ai_percentage):
        """Generate human-readable analysis summary"""
        summary_parts = []
        
        if features.get('ai_variable_count', 0) > 3:
            summary_parts.append("Uses generic variable naming patterns")
        
        if features.get('comment_grammar_issues', 0) > 2:
            summary_parts.append("Contains grammar issues in comments")
        
        if features.get('common_library_count', 0) > 2:
            summary_parts.append("Heavy use of common AI libraries")
        
        if features.get('indent_consistency', 1) < 0.8:
            summary_parts.append("Inconsistent indentation patterns")
        
        if features.get('function_count', 0) > 5:
            summary_parts.append("High function density")
        
        if ai_percentage >= 50:
            summary_parts.append("Strong indicators of AI generation")
        elif ai_percentage >= 30:
            summary_parts.append("Moderate indicators of AI generation")
        else:
            summary_parts.append("Appears to be human-written")
        
        return "; ".join(summary_parts) if summary_parts else "No significant patterns detected"

# Initialize detector
detector = AdvancedAIDetector()

# File handling
ALLOWED_EXTENSIONS = {'txt', 'py', 'java', 'js', 'cpp', 'html', 'css', 'php', 'rb', 'go', 'rs', 'swift', 'kt'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_language_from_extension(filename):
    ext = filename.rsplit('.', 1)[1].lower()
    language_map = {
        'py': 'Python', 'java': 'Java', 'js': 'JavaScript', 'cpp': 'C++',
        'html': 'HTML', 'css': 'CSS', 'php': 'PHP', 'rb': 'Ruby',
        'go': 'Go', 'rs': 'Rust', 'swift': 'Swift', 'kt': 'Kotlin'
    }
    return language_map.get(ext, 'Unknown')

def calculate_file_hash(content):
    return hashlib.sha256(content.encode('utf-8')).hexdigest()

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/analyze', methods=['POST'])
def api_analyze():
    """API endpoint for code analysis"""
    try:
        data = request.get_json()
        if not data or 'code' not in data:
            return jsonify({'error': 'No code provided'}), 400
        
        code = data['code']
        filename = data.get('filename', 'unknown')
        
        # Perform analysis
        result = detector.detect_ai_generated(code, filename)
        
        # Create result object
        analysis_result = {
            'id': len(analysis_results) + 1,
            'filename': filename,
            'file_hash': calculate_file_hash(code),
            'file_size': len(code),
            'language': get_language_from_extension(filename),
            'ai_percentage': result['ai_percentage'],
            'is_ai_generated': result['is_ai_generated'],
            'analysis_details': result,
            'created_at': datetime.utcnow().isoformat()
        }
        
        # Store result
        analysis_results.append(analysis_result)
        
        return jsonify(analysis_result)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/analyze_files', methods=['POST'])
def analyze_files():
    """Web interface file analysis"""
    if 'files' not in request.files:
        return render_template('index.html', message="No files selected.")
    
    files = request.files.getlist('files')
    if not files:
        return render_template('index.html', message="No files selected.")
    
    results = []
    
    for file in files:
        if file and allowed_file(file.filename):
            try:
                content = file.read().decode('utf-8')
                
                # Perform analysis
                analysis = detector.detect_ai_generated(content, file.filename)
                
                # Create result object
                result = {
                    'filename': file.filename,
                    'file_hash': calculate_file_hash(content),
                    'file_size': len(content),
                    'language': get_language_from_extension(file.filename),
                    'ai_percentage': analysis['ai_percentage'],
                    'is_ai_generated': analysis['is_ai_generated'],
                    'analysis_details': analysis
                }
                
                results.append(result)
                
            except Exception as e:
                results.append({
                    'filename': file.filename,
                    'error': str(e)
                })
    
    return render_template('analysis_results.html', analysis_results=results)

@app.route('/api/history')
def api_history():
    """Get analysis history"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    start_idx = (page - 1) * per_page
    end_idx = start_idx + per_page
    page_results = analysis_results[start_idx:end_idx]
    
    return jsonify({
        'results': page_results,
        'total': len(analysis_results),
        'pages': (len(analysis_results) + per_page - 1) // per_page,
        'current_page': page
    })

@app.route('/dashboard')
def dashboard():
    """Analytics dashboard"""
    # Get statistics
    total_analyses = len(analysis_results)
    ai_generated_count = sum(1 for r in analysis_results if r.get('is_ai_generated', False))
    human_written_count = total_analyses - ai_generated_count
    
    # Language distribution
    language_stats = {}
    for result in analysis_results:
        lang = result.get('language', 'Unknown')
        language_stats[lang] = language_stats.get(lang, 0) + 1
    
    # Recent analyses
    recent_analyses = sorted(analysis_results, key=lambda x: x.get('created_at', ''), reverse=True)[:10]
    
    return render_template('dashboard.html',
                         total_analyses=total_analyses,
                         ai_generated_count=ai_generated_count,
                         human_written_count=human_written_count,
                         language_stats=language_stats.items(),
                         recent_analyses=recent_analyses)

@app.route('/api/stats')
def api_stats():
    """API endpoint for statistics"""
    total_analyses = len(analysis_results)
    ai_generated_count = sum(1 for r in analysis_results if r.get('is_ai_generated', False))
    
    # Average AI percentage
    avg_ai_percentage = 0
    if analysis_results:
        avg_ai_percentage = sum(r.get('ai_percentage', 0) for r in analysis_results) / len(analysis_results)
    
    # Language distribution
    language_stats = {}
    for result in analysis_results:
        lang = result.get('language', 'Unknown')
        language_stats[lang] = language_stats.get(lang, 0) + 1
    
    return jsonify({
        'total_analyses': total_analyses,
        'ai_generated_count': ai_generated_count,
        'human_written_count': total_analyses - ai_generated_count,
        'avg_ai_percentage': round(avg_ai_percentage, 2),
        'language_distribution': language_stats
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)