# 🤖 AI Code Detector - Advanced Analysis Tool

A sophisticated machine learning-powered tool for detecting AI-generated code with high accuracy and detailed analysis.

## ✨ Features

### 🧠 Advanced AI Detection
- **Machine Learning Algorithms**: Uses scikit-learn with Random Forest classifiers
- **Multi-Factor Analysis**: 15+ detection methods working together
- **AST (Abstract Syntax Tree) Analysis**: Deep code structure parsing
- **Semantic Pattern Recognition**: Identifies AI-generated coding patterns
- **Style Consistency Analysis**: Detects automated formatting vs human inconsistencies

### 📊 Real-Time Analytics Dashboard
- **Interactive Charts**: Plotly-powered visualizations
- **Live Statistics**: Real-time updates of analysis data
- **Language Distribution**: Track patterns across programming languages
- **Historical Data**: View analysis trends over time
- **Auto-refresh**: Updates every 30 seconds

### 🚀 Modern User Interface
- **Drag & Drop Upload**: Intuitive file handling
- **Code Paste Interface**: Direct code input with syntax highlighting
- **Real-time Progress**: Animated progress indicators
- **Responsive Design**: Works on all devices
- **Dark Theme**: Modern, eye-friendly interface

### 🔧 Technical Features
- **REST API**: Programmatic access to analysis engine
- **Database Integration**: SQLite with SQLAlchemy ORM
- **Caching System**: Avoids re-analyzing identical files
- **Multi-language Support**: Python, Java, JavaScript, C++, HTML, CSS, PHP, Ruby, Go, Rust, Swift, Kotlin
- **File Hash Tracking**: Prevents duplicate analysis

## 🛠️ Installation

### Prerequisites
- Python 3.8+
- pip

### Setup
```bash
# Clone the repository
git clone <repository-url>
cd ai-code-detector

# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py
```

The application will be available at `http://localhost:5000`

## 📈 Detection Methods

### 1. Code Structure Analysis
- **Indentation Consistency**: Measures formatting uniformity
- **Line Length Patterns**: Analyzes code layout
- **Empty Line Ratios**: Checks spacing patterns

### 2. Comment Analysis
- **Grammar Checking**: Uses LanguageTool for comment quality
- **Docstring Detection**: Identifies documentation patterns
- **Comment Density**: Measures documentation frequency

### 3. Variable & Function Analysis
- **Naming Patterns**: Detects generic variable names (var1, temp, result)
- **Function Density**: Analyzes code organization
- **Variable Length**: Checks naming complexity

### 4. Complexity Metrics
- **Cyclomatic Complexity**: Measures code complexity
- **Nesting Depth**: Analyzes code structure
- **Branch Count**: Counts decision points

### 5. Style Consistency
- **Operator Spacing**: Checks formatting consistency
- **Indentation Patterns**: Analyzes code alignment
- **Formatting Tools**: Detects automated formatting

### 6. Semantic Patterns
- **AI-Generated Patterns**: Recognizes common AI code structures
- **Library Usage**: Identifies typical AI library combinations
- **Code Templates**: Detects boilerplate patterns

## 🔌 API Usage

### Analyze Code
```bash
curl -X POST http://localhost:5000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "code": "def hello_world():\n    print(\"Hello, World!\")",
    "filename": "test.py"
  }'
```

### Get Statistics
```bash
curl http://localhost:5000/api/stats
```

### Get Analysis History
```bash
curl "http://localhost:5000/api/history?page=1&per_page=10"
```

## 📊 Dashboard Features

### Real-Time Analytics
- **Total Analyses**: Count of all processed files
- **AI Detection Rate**: Percentage of AI-generated code
- **Language Distribution**: Breakdown by programming language
- **Recent Analyses**: Latest 10 analysis results

### Interactive Charts
- **Pie Chart**: AI vs Human code distribution
- **Bar Chart**: Language usage statistics
- **Auto-updating**: Real-time data refresh

## 🎯 Detection Accuracy

The tool uses a weighted scoring system with the following factors:

### High Weight Indicators (15-20 points)
- Generic variable naming patterns
- Grammar issues in comments
- Heavy use of common AI libraries
- Multiple AI pattern matches

### Medium Weight Indicators (6-8 points)
- Inconsistent indentation
- Poor operator spacing
- High function density
- High cyclomatic complexity

### Low Weight Indicators (2-3 points)
- Long line lengths
- Presence of docstrings
- Main guard patterns

**Threshold**: 30% AI likelihood triggers "AI Generated" classification

## 🏗️ Architecture

```
├── app.py                 # Main Flask application
├── templates/            # HTML templates
│   ├── index.html       # Main upload interface
│   ├── dashboard.html   # Analytics dashboard
│   └── analysis_results.html # Results display
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

### Key Components

1. **AdvancedAIDetector Class**: Core detection engine
2. **AnalysisResult Model**: Database schema for results
3. **Flask Routes**: Web interface and API endpoints
4. **Frontend JavaScript**: Interactive UI components

## 🔒 Security Features

- **File Size Limits**: 16MB maximum file size
- **File Type Validation**: Restricted to code files only
- **Input Sanitization**: Prevents malicious uploads
- **Rate Limiting**: Prevents abuse (configurable)

## 🚀 Performance Optimizations

- **Database Caching**: Avoids re-analyzing identical files
- **Async Processing**: Non-blocking analysis
- **Memory Management**: Efficient file handling
- **Connection Pooling**: Database optimization

## 🎨 UI/UX Features

### Modern Design
- **Dark Theme**: Eye-friendly interface
- **Gradient Backgrounds**: Visual appeal
- **Smooth Animations**: Enhanced user experience
- **Responsive Layout**: Mobile-friendly design

### Interactive Elements
- **Drag & Drop**: Intuitive file upload
- **Progress Indicators**: Real-time feedback
- **Hover Effects**: Enhanced interactivity
- **Loading States**: Clear user feedback

## 📝 Usage Examples

### Web Interface
1. Visit `http://localhost:5000`
2. Upload files or paste code directly
3. View detailed analysis results
4. Check dashboard for statistics

### API Integration
```python
import requests

# Analyze code
response = requests.post('http://localhost:5000/api/analyze', json={
    'code': 'your_code_here',
    'filename': 'test.py'
})

result = response.json()
print(f"AI Percentage: {result['ai_percentage']}%")
print(f"Is AI Generated: {result['is_ai_generated']}")
```

## 🔧 Configuration

### Environment Variables
```bash
FLASK_SECRET_KEY=your-secret-key
DATABASE_URL=sqlite:///ai_detector.db
MAX_FILE_SIZE=16777216  # 16MB in bytes
```

### Customization
- **Detection Thresholds**: Adjust in `AdvancedAIDetector` class
- **Supported Languages**: Modify `ALLOWED_EXTENSIONS`
- **UI Theme**: Customize CSS variables in templates

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **LanguageTool**: Grammar checking capabilities
- **scikit-learn**: Machine learning algorithms
- **Plotly**: Interactive visualizations
- **Bootstrap**: UI framework
- **Font Awesome**: Icons

## 📞 Support

For questions, issues, or feature requests:
- Create an issue on GitHub
- Check the documentation
- Review the API examples

---

**Made with ❤️ for the developer community**