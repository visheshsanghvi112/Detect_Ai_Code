import unittest
import re
import markdown
from pathlib import Path


class TestReadmeValidation(unittest.TestCase):
    """
    Comprehensive unit tests for README.md validation.
    
    Tests cover content structure, formatting, links, code examples,
    and documentation completeness. Using unittest framework.
    """
    
    def setUp(self):
        """Set up test fixtures for README validation."""
        self.readme_path = Path("README.md")
        if self.readme_path.exists():
            with open(self.readme_path, 'r', encoding='utf-8') as f:
                self.readme_content = f.read()
        else:
            self.readme_content = ""
        
        # Expected sections for validation
        self.required_sections = [
            "Features", "Installation", "Detection Methods", 
            "API Usage", "Dashboard Features", "Architecture",
            "Security Features", "Performance Optimizations",
            "Usage Examples", "Configuration", "Contributing"
        ]
        
        # Code block patterns
        self.code_block_pattern = r'```(\w+)?\n(.*?)\n```'
        self.inline_code_pattern = r'`([^`]+)`'
        
    def test_readme_file_exists(self):
        """Test that README.md file exists in the project root."""
        self.assertTrue(
            self.readme_path.exists(),
            "README.md file should exist in the project root"
        )
        
    def test_readme_not_empty(self):
        """Test that README.md is not empty."""
        self.assertTrue(
            len(self.readme_content.strip()) > 0,
            "README.md should not be empty"
        )
        
    def test_readme_has_title(self):
        """Test that README has a proper title."""
        lines = self.readme_content.split('\n')
        title_found = False
        for line in lines[:5]:  # Check first 5 lines
            if line.startswith('# ') and 'AI Code Detector' in line:
                title_found = True
                break
        self.assertTrue(title_found, "README should have a proper title")
        
    def test_required_sections_present(self):
        """Test that all required sections are present in README."""
        for section in self.required_sections:
            with self.subTest(section=section):
                section_pattern = rf'^#+\s*.*{re.escape(section)}'
                self.assertRegex(
                    self.readme_content,
                    section_pattern,
                    f"Section '{section}' should be present in README",
                    flags=re.MULTILINE | re.IGNORECASE
                )
                
    def test_installation_section_completeness(self):
        """Test that installation section has prerequisites and setup steps."""
        installation_section = self._extract_section("Installation")
        
        # Check for prerequisites
        self.assertIn(
            "Prerequisites",
            installation_section,
            "Installation section should include prerequisites"
        )
        
        # Check for Python version requirement
        self.assertRegex(
            installation_section,
            r'Python\s+3\.\d+',
            "Should specify Python version requirement"
        )
        
        # Check for setup commands
        setup_commands = ["git clone", "pip install", "python app.py"]
        for command in setup_commands:
            with self.subTest(command=command):
                self.assertIn(
                    command,
                    installation_section,
                    f"Installation should include '{command}' command"
                )
                
    def test_api_usage_examples_valid(self):
        """Test that API usage examples contain valid curl commands."""
        api_section = self._extract_section("API Usage")
        
        # Extract curl commands
        curl_commands = re.findall(r'curl[^`\n]*(?:\n[^`]*)*', api_section)
        
        self.assertGreater(
            len(curl_commands),
            0,
            "API Usage section should contain curl examples"
        )
        
        for i, command in enumerate(curl_commands):
            with self.subTest(command_index=i):
                # Check for proper HTTP methods
                self.assertTrue(
                    any(method in command for method in ['-X POST', '-X GET', 'GET', 'POST']),
                    f"Curl command {i+1} should specify HTTP method"
                )
                
                # Check for localhost URL
                self.assertIn(
                    "localhost:5000",
                    command,
                    f"Curl command {i+1} should use localhost:5000"
                )
                
    def test_code_blocks_have_language_specification(self):
        """Test that code blocks specify their language for syntax highlighting."""
        code_blocks = re.findall(self.code_block_pattern, self.readme_content, re.DOTALL)
        
        # Filter out empty language specifications
        unspecified_blocks = [block for block in code_blocks if not block[0]]
        
        # Allow some unspecified blocks (like plain text examples)
        self.assertLessEqual(
            len(unspecified_blocks),
            3,
            "Most code blocks should specify their language"
        )
        
    def test_bash_code_blocks_syntax(self):
        """Test that bash code blocks contain valid shell commands."""
        bash_blocks = re.findall(
            r'```bash\n(.*?)\n```',
            self.readme_content,
            re.DOTALL
        )
        
        for i, block in enumerate(bash_blocks):
            with self.subTest(block_index=i):
                # Check for common shell commands
                commands = ['git', 'pip', 'python', 'curl', 'cd']
                has_valid_command = any(cmd in block for cmd in commands)
                
                self.assertTrue(
                    has_valid_command,
                    f"Bash block {i+1} should contain recognizable shell commands"
                )
                
    def test_python_code_blocks_syntax(self):
        """Test that Python code blocks contain valid Python syntax."""
        python_blocks = re.findall(
            r'```python\n(.*?)\n```',
            self.readme_content,
            re.DOTALL
        )
        
        for i, block in enumerate(python_blocks):
            with self.subTest(block_index=i):
                # Basic syntax validation
                try:
                    compile(block, f'<readme_python_block_{i}>', 'exec')
                except SyntaxError as e:
                    self.fail(f"Python block {i+1} has syntax error: {e}")
                    
    def test_feature_list_completeness(self):
        """Test that feature list covers main functionality areas."""
        features_section = self._extract_section("Features")
        
        expected_features = [
            "Machine Learning", "AST", "Semantic Pattern", 
            "Analytics Dashboard", "REST API", "Multi-language"
        ]
        
        for feature in expected_features:
            with self.subTest(feature=feature):
                self.assertIn(
                    feature,
                    features_section,
                    f"Features should mention '{feature}'"
                )
                
    def test_detection_methods_documented(self):
        """Test that detection methods are properly documented."""
        detection_section = self._extract_section("Detection Methods")
        
        # Should have numbered subsections
        numbered_sections = re.findall(r'### \d+\.\s+([^\n]+)', detection_section)
        
        self.assertGreaterEqual(
            len(numbered_sections),
            5,
            "Should document at least 5 detection methods"
        )
        
        # Check for specific method types
        expected_methods = [
            "Code Structure", "Comment Analysis", "Variable", 
            "Complexity", "Style Consistency", "Semantic"
        ]
        
        for method in expected_methods:
            with self.subTest(method=method):
                self.assertIn(
                    method,
                    detection_section,
                    f"Should document '{method}' detection method"
                )
                
    def test_architecture_section_structure(self):
        """Test that architecture section shows project structure."""
        arch_section = self._extract_section("Architecture")
        
        # Should contain file tree structure
        self.assertIn("├──", arch_section, "Should show file tree structure")
        self.assertIn("app.py", arch_section, "Should mention main application file")
        self.assertIn("templates/", arch_section, "Should mention templates directory")
        
    def test_configuration_options_documented(self):
        """Test that configuration options are properly documented."""
        config_section = self._extract_section("Configuration")
        
        # Check for environment variables
        env_vars = ["FLASK_SECRET_KEY", "DATABASE_URL", "MAX_FILE_SIZE"]
        
        for var in env_vars:
            with self.subTest(env_var=var):
                self.assertIn(
                    var,
                    config_section,
                    f"Should document '{var}' environment variable"
                )
                
    def test_security_features_coverage(self):
        """Test that security features are adequately covered."""
        security_section = self._extract_section("Security Features")
        
        security_aspects = [
            "File Size Limits", "File Type Validation", 
            "Input Sanitization", "Rate Limiting"
        ]
        
        for aspect in security_aspects:
            with self.subTest(security_aspect=aspect):
                self.assertIn(
                    aspect,
                    security_section,
                    f"Should document '{aspect}' security feature"
                )
                
    def test_contributing_guidelines_present(self):
        """Test that contributing guidelines are present and complete."""
        contrib_section = self._extract_section("Contributing")
        
        # Should have step-by-step process
        steps = ["Fork", "branch", "changes", "tests", "pull request"]
        
        for step in steps:
            with self.subTest(step=step):
                self.assertIn(
                    step,
                    contrib_section,
                    f"Contributing section should mention '{step}'"
                )
                
    def test_license_information_present(self):
        """Test that license information is present."""
        self.assertIn(
            "License",
            self.readme_content,
            "README should contain license information"
        )
        self.assertIn(
            "MIT",
            self.readme_content,
            "Should specify MIT license"
        )
        
    def test_acknowledgments_section_complete(self):
        """Test that acknowledgments section credits dependencies."""
        ack_section = self._extract_section("Acknowledgments")
        
        dependencies = ["LanguageTool", "scikit-learn", "Plotly", "Bootstrap"]
        
        for dep in dependencies:
            with self.subTest(dependency=dep):
                self.assertIn(
                    dep,
                    ack_section,
                    f"Should acknowledge '{dep}' dependency"
                )
                
    def test_emoji_usage_consistency(self):
        """Test that emojis are used consistently in section headers."""
        headers = re.findall(r'^#+\s*([^\n]+)', self.readme_content, re.MULTILINE)
        
        emoji_headers = [h for h in headers if re.search(r'[\U0001F300-\U0001F9FF]', h)]
        
        # Most headers should have emojis for visual appeal
        emoji_ratio = len(emoji_headers) / len(headers) if headers else 0
        
        self.assertGreater(
            emoji_ratio,
            0.5,
            "Majority of headers should use emojis for visual consistency"
        )
        
    def test_url_placeholders_identified(self):
        """Test that URL placeholders are properly identified."""
        # Find git clone command
        clone_match = re.search(r'git clone ([^\n]+)', self.readme_content)
        
        if clone_match:
            url = clone_match.group(1)
            self.assertTrue(
                '<repository-url>' in url or 'github.com' in url,
                "Git clone URL should be a placeholder or actual URL"
            )
            
    def test_line_length_reasonable(self):
        """Test that most lines are of reasonable length for readability."""
        lines = self.readme_content.split('\n')
        long_lines = [line for line in lines if len(line) > 120]
        
        # Allow some long lines (like URLs or code examples)
        long_line_ratio = len(long_lines) / len(lines) if lines else 0
        
        self.assertLess(
            long_line_ratio,
            0.1,
            "Most lines should be reasonably short for readability"
        )
        
    def test_detection_accuracy_threshold_documented(self):
        """Test that detection accuracy and thresholds are documented."""
        accuracy_section = self._extract_section("Detection Accuracy")
        
        # Should mention threshold percentage
        self.assertRegex(
            accuracy_section,
            r'\d+%.*threshold',
            "Should specify detection threshold percentage",
            flags=re.IGNORECASE
        )
        
        # Should mention weighted scoring
        self.assertIn(
            "weighted",
            accuracy_section,
            "Should explain weighted scoring system"
        )
        
    def test_api_endpoints_documented(self):
        """Test that all API endpoints are documented with examples."""
        api_section = self._extract_section("API Usage")
        
        endpoints = ["/api/analyze", "/api/stats", "/api/history"]
        
        for endpoint in endpoints:
            with self.subTest(endpoint=endpoint):
                self.assertIn(
                    endpoint,
                    api_section,
                    f"Should document '{endpoint}' API endpoint"
                )
                
    def test_dashboard_features_explained(self):
        """Test that dashboard features are properly explained."""
        dashboard_section = self._extract_section("Dashboard Features")
        
        features = ["Real-Time Analytics", "Interactive Charts", "Total Analyses"]
        
        for feature in features:
            with self.subTest(feature=feature):
                self.assertIn(
                    feature,
                    dashboard_section,
                    f"Should explain '{feature}' dashboard feature"
                )
                
    def _extract_section(self, section_name):
        """Helper method to extract content of a specific section."""
        # Find section header
        pattern = rf'^#+\s*.*{re.escape(section_name)}.*$'
        match = re.search(pattern, self.readme_content, re.MULTILINE | re.IGNORECASE)
        
        if not match:
            return ""
            
        start = match.end()
        
        # Find next section header or end of file
        next_section = re.search(r'^#+\s', self.readme_content[start:], re.MULTILINE)
        end = start + next_section.start() if next_section else len(self.readme_content)
        
        return self.readme_content[start:end]


class TestReadmeMarkdownSyntax(unittest.TestCase):
    """Test Markdown syntax validation for README.md."""
    
    def setUp(self):
        """Set up Markdown parser for syntax validation."""
        self.readme_path = Path("README.md")
        if self.readme_path.exists():
            with open(self.readme_path, 'r', encoding='utf-8') as f:
                self.readme_content = f.read()
        else:
            self.readme_content = ""
            
    def test_markdown_syntax_valid(self):
        """Test that README.md has valid Markdown syntax."""
        try:
            # This will raise an exception if markdown is severely malformed
            html = markdown.markdown(self.readme_content)
            self.assertIsInstance(html, str)
            self.assertGreater(len(html), 0, "Markdown should generate HTML output")
        except Exception as e:
            self.fail(f"Markdown syntax error: {e}")
            
    def test_header_hierarchy_valid(self):
        """Test that header hierarchy is logical (no skipping levels)."""
        headers = re.findall(r'^(#+)\s', self.readme_content, re.MULTILINE)
        header_levels = [len(h) for h in headers]
        
        for i in range(1, len(header_levels)):
            level_jump = header_levels[i] - header_levels[i-1]
            self.assertLessEqual(
                level_jump,
                1,
                f"Header level jump too large at position {i}: {header_levels[i-1]} to {header_levels[i]}"
            )
            
    def test_list_formatting_consistent(self):
        """Test that list formatting is consistent throughout."""
        # Find all list items
        list_items = re.findall(r'^(\s*[-*+]\s)', self.readme_content, re.MULTILINE)
        
        if list_items:
            # Most common list marker should be used consistently
            from collections import Counter
            markers = [item.strip() for item in list_items]
            most_common = Counter(markers).most_common(1)[0]
            
            # Allow some variation but encourage consistency
            consistency_ratio = most_common[1] / len(markers)
            
            self.assertGreater(
                consistency_ratio,
                0.8,
                "List formatting should be mostly consistent"
            )


class TestReadmeCodeExamples(unittest.TestCase):
    """Test code examples in README.md for correctness."""
    
    def setUp(self):
        """Set up code example extraction."""
        self.readme_path = Path("README.md") 
        if self.readme_path.exists():
            with open(self.readme_path, 'r', encoding='utf-8') as f:
                self.readme_content = f.read()
        else:
            self.readme_content = ""
            
    def test_json_examples_valid(self):
        """Test that JSON examples in API documentation are valid."""
        import json
        
        # Extract JSON from code blocks
        json_patterns = [
            r'```json\n(.*?)\n```',
            r'-d\s+\'({.*?})\'',
            r'-d\s+"({.*?})"'
        ]
        
        json_examples = []
        for pattern in json_patterns:
            matches = re.findall(pattern, self.readme_content, re.DOTALL)
            json_examples.extend(matches)
            
        for i, json_str in enumerate(json_examples):
            with self.subTest(json_index=i):
                try:
                    json.loads(json_str)
                except json.JSONDecodeError as e:
                    self.fail(f"JSON example {i+1} is invalid: {e}")
                    
    def test_curl_commands_well_formed(self):
        """Test that curl commands are well-formed."""
        curl_commands = re.findall(
            r'curl[^`\n]*(?:\n[^`]*)*',
            self.readme_content
        )
        
        for i, command in enumerate(curl_commands):
            with self.subTest(command_index=i):
                # Should have URL
                self.assertRegex(
                    command,
                    r'https?://\S+',
                    f"Curl command {i+1} should have valid URL"
                )
                
                # If POST, should have data
                if '-X POST' in command or 'POST' in command:
                    self.assertTrue(
                        '-d' in command or '--data' in command,
                        f"POST curl command {i+1} should include data"
                    )


if __name__ == '__main__':
    # Run all tests
    unittest.main(verbosity=2)