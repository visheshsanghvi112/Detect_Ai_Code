import os
from datetime import timedelta

class Config:
    """Application configuration class"""
    
    # Flask Configuration
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-here-change-in-production'
    DEBUG = os.environ.get('FLASK_DEBUG', 'True').lower() == 'true'
    
    # Database Configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///ai_detector.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # File Upload Configuration
    UPLOAD_FOLDER = 'uploads'
    MAX_CONTENT_LENGTH = int(os.environ.get('MAX_FILE_SIZE', 16 * 1024 * 1024))  # 16MB default
    ALLOWED_EXTENSIONS = {
        'txt', 'py', 'java', 'js', 'cpp', 'html', 'css', 'php', 
        'rb', 'go', 'rs', 'swift', 'kt', 'ts', 'jsx', 'tsx'
    }
    
    # AI Detection Configuration
    AI_DETECTION_THRESHOLD = float(os.environ.get('AI_DETECTION_THRESHOLD', 30.0))
    MAX_FILE_SIZE_FOR_ANALYSIS = 1024 * 1024  # 1MB for analysis
    
    # Language Mapping
    LANGUAGE_MAP = {
        'py': 'Python',
        'java': 'Java', 
        'js': 'JavaScript',
        'ts': 'TypeScript',
        'jsx': 'React JSX',
        'tsx': 'React TSX',
        'cpp': 'C++',
        'c': 'C',
        'html': 'HTML',
        'css': 'CSS',
        'php': 'PHP',
        'rb': 'Ruby',
        'go': 'Go',
        'rs': 'Rust',
        'swift': 'Swift',
        'kt': 'Kotlin',
        'txt': 'Text'
    }
    
    # Common AI Libraries (for detection)
    AI_LIBRARIES = [
        'numpy', 'pandas', 'matplotlib', 'tensorflow', 'keras', 
        'sklearn', 'requests', 'beautifulsoup4', 'selenium',
        'opencv', 'pillow', 'scipy', 'plotly', 'dash'
    ]
    
    # AI Variable Patterns
    AI_VARIABLE_PATTERNS = [
        r'\bvar\d+\b',      # var1, var2, etc.
        r'\btemp\d*\b',     # temp, temp1, etc.
        r'\bresult\d*\b',   # result, result1, etc.
        r'\bdata\d*\b',     # data, data1, etc.
        r'\bvalue\d*\b',    # value, value1, etc.
        r'\bitem\d*\b',     # item, item1, etc.
        r'\bcount\d*\b',    # count, count1, etc.
    ]
    
    # AI Code Patterns
    AI_CODE_PATTERNS = [
        r'for\s+\w+\s+in\s+range\s*\(',  # for i in range(
        r'if\s+__name__\s*==\s*[\'"]__main__[\'"]',  # if __name__ == "__main__"
        r'try:\s*\n\s*except\s+Exception',  # try/except patterns
        r'def\s+\w+\s*\([^)]*\):\s*\n\s*"""[^"]*"""',  # function with docstring
        r'import\s+[a-zA-Z_][a-zA-Z0-9_]*\s+as\s+[a-zA-Z_][a-zA-Z0-9_]*',  # import as patterns
    ]
    
    # Scoring Weights
    SCORING_WEIGHTS = {
        'ai_variable_count': 20,      # High weight for generic variables
        'comment_grammar_issues': 15,  # High weight for grammar issues
        'common_library_count': 10,    # Medium-high weight for AI libraries
        'ai_pattern_matches': 15,      # High weight for AI patterns
        'indent_consistency': 8,       # Medium weight for formatting
        'operator_spacing': 8,         # Medium weight for style
        'function_count': 6,           # Medium weight for function density
        'cyclomatic_complexity': 6,    # Medium weight for complexity
        'avg_line_length': 3,          # Low weight for line length
        'max_line_length': 3,          # Low weight for long lines
        'has_docstrings': 2,           # Low weight for documentation
        'has_main_guard': 2,           # Low weight for main guard
    }
    
    # Dashboard Configuration
    DASHBOARD_REFRESH_INTERVAL = 30000  # 30 seconds
    RECENT_ANALYSES_LIMIT = 10
    
    # API Configuration
    API_RATE_LIMIT = '100 per minute'
    API_PAGINATION_DEFAULT = 10
    API_PAGINATION_MAX = 100
    
    # Cache Configuration
    CACHE_TIMEOUT = timedelta(hours=24)  # Cache results for 24 hours
    
    # Security Configuration
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', '*').split(',')
    
    @staticmethod
    def init_app(app):
        """Initialize application with configuration"""
        # Create upload directory if it doesn't exist
        os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
        
        # Set up logging
        if not app.debug:
            import logging
            from logging.handlers import RotatingFileHandler
            
            if not os.path.exists('logs'):
                os.mkdir('logs')
            
            file_handler = RotatingFileHandler(
                'logs/ai_detector.log', 
                maxBytes=10240000, 
                backupCount=10
            )
            file_handler.setFormatter(logging.Formatter(
                '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
            ))
            file_handler.setLevel(logging.INFO)
            app.logger.addHandler(file_handler)
            app.logger.setLevel(logging.INFO)
            app.logger.info('AI Code Detector startup')

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///ai_detector_dev.db'

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///ai_detector.db'
    
    @classmethod
    def init_app(cls, app):
        Config.init_app(app)
        
        # Production-specific logging
        import logging
        from logging.handlers import RotatingFileHandler
        
        if not os.path.exists('logs'):
            os.mkdir('logs')
        
        file_handler = RotatingFileHandler(
            'logs/ai_detector.log', 
            maxBytes=10240000, 
            backupCount=10
        )
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO)
        app.logger.info('AI Code Detector startup')

class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}