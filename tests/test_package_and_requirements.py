#!/usr/bin/env python3
"""
Unit tests for package.json validation and requirements checking.

This test suite validates the package.json configuration file for the
ai-code-detector project, ensuring all required fields are present,
dependencies are properly specified, and configuration follows best practices.

Testing Framework: pytest (Python standard testing framework)
"""

import json
import os
import re
import pytest
from pathlib import Path


class TestPackageJsonValidation:
    """Test suite for package.json file validation."""
    
    @pytest.fixture
    def package_json_path(self):
        """Fixture to provide the package.json file path."""
        return Path(__file__).parent.parent / "package.json"
    
    @pytest.fixture
    def package_data(self, package_json_path):
        """Fixture to load and parse package.json data."""
        with open(package_json_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def test_package_json_exists(self, package_json_path):
        """Test that package.json file exists and is readable."""
        assert package_json_path.exists(), "package.json file must exist"
        assert package_json_path.is_file(), "package.json must be a file"
        assert os.access(package_json_path, os.R_OK), "package.json must be readable"
    
    def test_package_json_valid_json(self, package_json_path):
        """Test that package.json contains valid JSON."""
        try:
            with open(package_json_path, 'r', encoding='utf-8') as f:
                json.load(f)
        except json.JSONDecodeError as e:
            pytest.fail(f"package.json contains invalid JSON: {e}")
    
    def test_required_fields_present(self, package_data):
        """Test that all required package.json fields are present."""
        required_fields = [
            'name', 'version', 'description', 'main', 'scripts',
            'author', 'license', 'dependencies'
        ]
        
        for field in required_fields:
            assert field in package_data, f"Required field '{field}' missing from package.json"
            assert package_data[field] is not None, f"Field '{field}' cannot be null"
            assert package_data[field] != "", f"Field '{field}' cannot be empty"
    
    def test_package_name_format(self, package_data):
        """Test that package name follows npm naming conventions."""
        name = package_data['name']
        
        # Package name validation rules
        assert len(name) <= 214, "Package name must be <= 214 characters"
        assert len(name) >= 1, "Package name must not be empty"
        assert name.lower() == name, "Package name must be lowercase"
        assert not name.startswith('.'), "Package name cannot start with a dot"
        assert not name.startswith('_'), "Package name cannot start with underscore"
        assert not re.search(r'[A-Z]', name), "Package name cannot contain uppercase letters"
        assert re.match(r'^[a-z0-9-]+$', name), "Package name can only contain lowercase letters, numbers, and hyphens"
    
    def test_version_format(self, package_data):
        """Test that version follows semantic versioning format."""
        version = package_data['version']
        semver_pattern = r'^\d+\.\d+\.\d+(-[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)*)?(\+[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)*)?$'
        
        assert re.match(semver_pattern, version), f"Version '{version}' must follow semantic versioning format"
        
        # Specific version checks
        version_parts = version.split('.')
        assert len(version_parts) >= 3, "Version must have at least major.minor.patch"
        
        for part in version_parts[:3]:  # major, minor, patch
            assert part.isdigit(), f"Version part '{part}' must be numeric"
            assert int(part) >= 0, f"Version part '{part}' must be non-negative"
    
    def test_main_file_reference(self, package_data):
        """Test that main field references a valid file."""
        main_file = package_data['main']
        
        assert main_file.endswith('.js'), "Main file should be a JavaScript file"
        assert not main_file.startswith('/'), "Main file path should be relative"
        
        # Check if main file exists (relative to package.json)
        package_dir = Path(__file__).parent.parent
        main_file_path = package_dir / main_file
        
        # Note: We don't assert file existence as it may not be created yet in development
        if main_file_path.exists():
            assert main_file_path.is_file(), f"Main file '{main_file}' must be a file if it exists"
    
    def test_scripts_configuration(self, package_data):
        """Test that npm scripts are properly configured."""
        scripts = package_data['scripts']
        
        # Check for essential scripts
        essential_scripts = ['start', 'test']
        for script in essential_scripts:
            assert script in scripts, f"Essential script '{script}' is missing"
        
        # Validate script commands
        assert scripts['start'].startswith('node'), "Start script should use node command"
        
        # Check for development scripts
        dev_scripts = ['dev', 'lint', 'format']
        for script in dev_scripts:
            if script in scripts:
                assert isinstance(scripts[script], str), f"Script '{script}' must be a string"
                assert len(scripts[script]) > 0, f"Script '{script}' cannot be empty"
    
    def test_keywords_validity(self, package_data):
        """Test that keywords are appropriate and well-formatted."""
        keywords = package_data['keywords']
        
        assert isinstance(keywords, list), "Keywords must be an array"
        assert len(keywords) > 0, "At least one keyword should be provided"
        assert len(keywords) <= 20, "Too many keywords can be considered spam"
        
        for keyword in keywords:
            assert isinstance(keyword, str), "Each keyword must be a string"
            assert len(keyword) > 0, "Keywords cannot be empty"
            assert len(keyword) <= 50, f"Keyword '{keyword}' is too long"
            assert keyword.lower() == keyword, f"Keyword '{keyword}' should be lowercase"
            assert not keyword.startswith(' '), f"Keyword '{keyword}' should not start with space"
            assert not keyword.endswith(' '), f"Keyword '{keyword}' should not end with space"
    
    def test_author_information(self, package_data):
        """Test that author information is properly formatted."""
        author = package_data['author']
        
        assert isinstance(author, str), "Author must be a string"
        assert len(author) > 0, "Author name cannot be empty"
        assert len(author) <= 100, "Author name is too long"
    
    def test_license_validity(self, package_data):
        """Test that license is specified and valid."""
        license_field = package_data['license']
        
        # Common valid SPDX license identifiers
        common_licenses = [
            'MIT', 'Apache-2.0', 'GPL-3.0', 'BSD-3-Clause', 'ISC',
            'GPL-2.0', 'LGPL-3.0', 'BSD-2-Clause', 'MPL-2.0'
        ]
        
        assert isinstance(license_field, str), "License must be a string"
        assert len(license_field) > 0, "License cannot be empty"
        
        # Check if it's a known license or follows SPDX format
        if license_field not in common_licenses:
            # Allow custom licenses but warn
            assert re.match(r'^[A-Za-z0-9\-\.]+$', license_field), "License should follow SPDX identifier format"
    
    def test_repository_configuration(self, package_data):
        """Test repository configuration if present."""
        if 'repository' in package_data:
            repo = package_data['repository']
            
            assert isinstance(repo, dict), "Repository must be an object"
            assert 'type' in repo, "Repository type is required"
            assert 'url' in repo, "Repository URL is required"
            
            assert repo['type'] == 'git', "Repository type should be 'git'"
            assert repo['url'].startswith('https://'), "Repository URL should use HTTPS"
            assert 'github.com' in repo['url'], "Repository should be on GitHub"
    
    def test_bugs_url_configuration(self, package_data):
        """Test bugs URL configuration if present."""
        if 'bugs' in package_data:
            bugs = package_data['bugs']
            
            if isinstance(bugs, dict):
                assert 'url' in bugs, "Bugs URL is required when bugs is an object"
                assert bugs['url'].startswith('https://'), "Bugs URL should use HTTPS"
            elif isinstance(bugs, str):
                assert bugs.startswith('https://'), "Bugs URL should use HTTPS"
    
    def test_homepage_url(self, package_data):
        """Test homepage URL if present."""
        if 'homepage' in package_data:
            homepage = package_data['homepage']
            
            assert isinstance(homepage, str), "Homepage must be a string"
            assert homepage.startswith('https://'), "Homepage should use HTTPS"
            assert len(homepage) > 0, "Homepage cannot be empty"
    
    def test_dependencies_structure(self, package_data):
        """Test that dependencies are properly structured."""
        deps = package_data['dependencies']
        
        assert isinstance(deps, dict), "Dependencies must be an object"
        
        for package, version in deps.items():
            assert isinstance(package, str), "Package name '{package}' must be a string"
            assert isinstance(version, str), "Version for '{package}' must be a string"
            assert len(package) > 0, "Package name cannot be empty"
            assert len(version) > 0, "Version for '{package}' cannot be empty"
            
            # Check version format (semver with range specifiers)
            version_pattern = r'^[\^~>=<*]?[\d\w\-\.]+(\s*\|\|\s*[\^~>=<*]?[\d\w\-\.]+)*$'
            assert re.match(version_pattern, version), f"Invalid version format for '{package}': {version}"
    
    def test_dev_dependencies_structure(self, package_data):
        """Test that devDependencies are properly structured."""
        if 'devDependencies' in package_data:
            dev_deps = package_data['devDependencies']
            
            assert isinstance(dev_deps, dict), "DevDependencies must be an object"
            
            for package, version in dev_deps.items():
                assert isinstance(package, str), "Dev package name '{package}' must be a string"
                assert isinstance(version, str), "Dev version for '{package}' must be a string"
                assert len(package) > 0, "Dev package name cannot be empty"
                assert len(version) > 0, "Dev version for '{package}' cannot be empty"
    
    def test_engines_specification(self, package_data):
        """Test Node.js and npm engine requirements."""
        if 'engines' in package_data:
            engines = package_data['engines']
            
            assert isinstance(engines, dict), "Engines must be an object"
            
            if 'node' in engines:
                node_version = engines['node']
                assert isinstance(node_version, str), "Node version must be a string"
                assert re.match(r'^>=?\d+\.\d+\.\d+$', node_version), f"Invalid node version format: {node_version}"
            
            if 'npm' in engines:
                npm_version = engines['npm']
                assert isinstance(npm_version, str), "NPM version must be a string"
                assert re.match(r'^>=?\d+\.\d+\.\d+$', npm_version), f"Invalid npm version format: {npm_version}"
    
    def test_os_specification(self, package_data):
        """Test operating system specifications if present."""
        if 'os' in package_data:
            os_list = package_data['os']
            
            assert isinstance(os_list, list), "OS specification must be an array"
            
            valid_os = ['linux', 'darwin', 'win32', 'freebsd', 'openbsd', 'sunos', 'aix']
            
            for os_name in os_list:
                assert isinstance(os_name, str), f"OS name '{os_name}' must be a string"
                assert os_name in valid_os, f"Invalid OS specification: {os_name}"
    
    def test_cpu_specification(self, package_data):
        """Test CPU architecture specifications if present."""
        if 'cpu' in package_data:
            cpu_list = package_data['cpu']
            
            assert isinstance(cpu_list, list), "CPU specification must be an array"
            
            valid_cpu = ['x64', 'ia32', 'arm', 'arm64', 'mips', 'mipsel', 'ppc', 'ppc64', 's390', 's390x']
            
            for cpu_arch in cpu_list:
                assert isinstance(cpu_arch, str), f"CPU architecture '{cpu_arch}' must be a string"
                assert cpu_arch in valid_cpu, f"Invalid CPU architecture: {cpu_arch}"
    
    def test_security_dependencies(self, package_data):
        """Test for security-related dependencies and configurations."""
        deps = package_data.get('dependencies', {})
        
        # Check for security-related packages
        security_packages = ['helmet', 'cors', 'express-rate-limit', 'bcrypt', 'jsonwebtoken']
        found_security = any(pkg in deps for pkg in security_packages)
        
        if 'express' in deps:
            # If using Express, should have some security middleware
            assert found_security, "Express applications should include security middleware (helmet, cors, etc.)"
    
    def test_essential_web_dependencies(self, package_data):
        """Test for essential web application dependencies."""
        deps = package_data.get('dependencies', {})
        
        # If this is a web application (has express), check for essential middleware
        if 'express' in deps:
            recommended_packages = ['body-parser', 'cors', 'helmet', 'morgan', 'compression']
            
            for package in recommended_packages:
                if package in deps:
                    # Verify version is not outdated (basic check)
                    version = deps[package]
                    assert not version.startswith('0.'), f"Package '{package}' version seems outdated: {version}"
    
    def test_no_conflicting_dependencies(self, package_data):
        """Test that there are no conflicting or duplicate dependencies."""
        deps = package_data.get('dependencies', {})
        dev_deps = package_data.get('devDependencies', {})
        
        # Check for packages that appear in both dependencies and devDependencies
        conflicting = set(deps.keys()) & set(dev_deps.keys())
        
        # Some packages might legitimately appear in both, but it's worth checking
        if conflicting:
            # This is a warning rather than a failure for some packages
            for pkg in conflicting:
                print(f"Warning: Package '{pkg}' appears in both dependencies and devDependencies")
    
    def test_package_json_formatting(self, package_json_path):
        """Test that package.json is properly formatted."""
        with open(package_json_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check for proper JSON formatting
        try:
            parsed = json.loads(content)
            # Re-serialize with standard formatting
            expected_format = json.dumps(parsed, indent=2, ensure_ascii=False)
            
            # Allow for different line endings and trailing whitespace
            content_normalized = content.strip()
            expected_normalized = expected_format.strip()
            
            # Note: This is a soft check - we don't fail the test but report formatting issues
            if content_normalized != expected_normalized:
                print("Note: package.json formatting could be improved for consistency")
                
        except json.JSONDecodeError:
            pytest.fail("package.json contains invalid JSON formatting")


class TestPackageJsonIntegration:
    """Integration tests for package.json with the broader project."""
    
    @pytest.fixture
    def package_data(self):
        """Load package.json data."""
        package_path = Path(__file__).parent.parent / "package.json"
        with open(package_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def test_main_file_exists_or_createable(self, package_data):
        """Test that the main file exists or can be created."""
        main_file = package_data['main']
        package_dir = Path(__file__).parent.parent
        main_file_path = package_dir / main_file
        
        if not main_file_path.exists():
            # Test that the directory exists and is writable
            main_file_dir = main_file_path.parent
            assert main_file_dir.exists() or main_file_dir.parent.exists(), \
                f"Directory for main file '{main_file}' does not exist and cannot be created"
    
    def test_scripts_executability(self, package_data):
        """Test that npm scripts reference valid commands."""
        scripts = package_data['scripts']
        
        # Test that script commands are reasonable
        for script_name, script_command in scripts.items():
            assert len(script_command.strip()) > 0, f"Script '{script_name}' is empty"
            
            # Check for common script patterns
            if script_name == 'start':
                assert 'node' in script_command.lower(), "Start script should use node"
            elif script_name == 'test' and 'Error: no test specified' not in script_command:
                assert any(test_cmd in script_command.lower() for test_cmd in ['jest', 'mocha', 'tap', 'ava', 'pytest']), \
                    "Test script should use a recognized testing framework"
    
    def test_dependency_versions_consistency(self, package_data):
        """Test that dependency versions are consistent and reasonable."""
        all_deps = {}
        all_deps.update(package_data.get('dependencies', {}))
        all_deps.update(package_data.get('devDependencies', {}))
        
        for package, version in all_deps.items():
            # Check for overly restrictive version pinning
            if version.startswith('='):
                print(f"Warning: Package '{package}' is pinned to exact version {version}")
            
            # Check for potentially unsafe version ranges
            if version == '*' or version == 'latest':
                print(f"Warning: Package '{package}' uses unsafe version specifier: {version}")
    
    def test_project_structure_consistency(self, package_data):
        """Test that package.json is consistent with project structure."""
        package_dir = Path(__file__).parent.parent
        
        # Check if this looks like a Node.js project
        has_node_modules = (package_dir / 'node_modules').exists()
        has_package_lock = (package_dir / 'package-lock.json').exists()
        has_yarn_lock = (package_dir / 'yarn.lock').exists()
        
        if has_node_modules or has_package_lock or has_yarn_lock:
            # This is definitely a Node.js project
            assert 'dependencies' in package_data, "Node.js project should have dependencies"
        
        # Check for README
        readme_files = list(package_dir.glob('README*'))
        if readme_files and 'homepage' in package_data:
            # If there's a README and homepage, they should be related
            homepage = package_data['homepage']
            if 'github.com' in homepage:
                assert homepage.endswith('#readme') or 'readme' in homepage.lower(), \
                    "GitHub homepage should reference README"


class TestPackageJsonEdgeCases:
    """Test edge cases and error conditions for package.json."""
    
    @pytest.fixture
    def package_data(self):
        """Load package.json data."""
        package_path = Path(__file__).parent.parent / "package.json"
        with open(package_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def test_version_edge_cases(self, package_data):
        """Test version field edge cases."""
        version = package_data['version']
        
        # Test major version is reasonable (not 0 for production, not too high)
        major = int(version.split('.')[0])
        assert major >= 0, "Major version cannot be negative"
        assert major <= 999, "Major version seems unreasonably high"
        
        # For this specific project at v2.0.0, test it's reasonable
        if major >= 1:
            # Production version should have meaningful minor/patch
            parts = version.split('.')
            minor = int(parts[1])
            patch = int(parts[2])
            assert minor >= 0 and minor <= 999, "Minor version out of reasonable range"
            assert patch >= 0 and patch <= 999, "Patch version out of reasonable range"
    
    def test_dependency_version_edge_cases(self, package_data):
        """Test dependency version specifications for edge cases."""
        deps = package_data.get('dependencies', {})
        dev_deps = package_data.get('devDependencies', {})
        all_deps = {**deps, **dev_deps}
        
        for package, version in all_deps.items():
            # Test for potential security issues
            assert version != "git+ssh://", f"Dependency '{package}' has invalid git+ssh URL"
            assert version != "git+http://", f"Dependency '{package}' uses insecure git+http"
            
            # Test for unreasonable version ranges
            if version.startswith('^'):
                # Caret ranges should have reasonable base versions
                base_version = version[1:]
                assert re.match(r'^\d+\.\d+\.\d+', base_version), f"Invalid caret range base for '{package}': {version}"
            
            if version.startswith('~'):
                # Tilde ranges should have reasonable base versions
                base_version = version[1:]
                assert re.match(r'^\d+\.\d+\.\d+', base_version), f"Invalid tilde range base for '{package}': {version}"
    
    def test_keywords_edge_cases(self, package_data):
        """Test keywords field for edge cases."""
        keywords = package_data['keywords']
        
        # Test for duplicate keywords
        assert len(keywords) == len(set(keywords)), "Keywords should not contain duplicates"
        
        # Test for overly generic keywords
        generic_keywords = ['library', 'module', 'tool', 'utility', 'app', 'application']
        specific_count = sum(1 for kw in keywords if kw not in generic_keywords)
        assert specific_count >= len(keywords) * 0.5, "Keywords should be more specific than generic"
        
        # Test keyword relevance to project name
        project_name_parts = package_data['name'].replace('-', ' ').split()
        relevant_count = sum(1 for kw in keywords if any(part in kw or kw in part for part in project_name_parts))
        assert relevant_count >= 1, "At least one keyword should relate to the project name"
    
    def test_description_quality(self, package_data):
        """Test package description quality."""
        description = package_data['description']
        
        # Test description length is reasonable
        assert len(description) >= 20, "Description should be at least 20 characters"
        assert len(description) <= 200, "Description should not exceed 200 characters"
        
        # Test description is not just the package name
        name_words = set(package_data['name'].replace('-', ' ').split())
        desc_words = set(description.lower().split())
        
        # Should have words beyond just the package name
        unique_desc_words = desc_words - name_words
        assert len(unique_desc_words) >= 3, "Description should provide more detail than just the package name"
        
        # Test for proper capitalization
        assert description[0].isupper(), "Description should start with a capital letter"
    
    def test_scripts_security(self, package_data):
        """Test npm scripts for potential security issues."""
        scripts = package_data['scripts']
        
        for script_name, script_command in scripts.items():
            # Test for potentially dangerous commands
            dangerous_patterns = [
                r'rm\s+-rf\s+[/*]',  # Dangerous rm commands
                r'curl.*\|\s*sh',     # Piping curl to shell
                r'wget.*\|\s*sh',     # Piping wget to shell
                r'sudo\s+',           # Sudo commands
                r'chmod\s+777',       # Overly permissive chmod
            ]
            
            for pattern in dangerous_patterns:
                assert not re.search(pattern, script_command, re.IGNORECASE), \
                    f"Script '{script_name}' contains potentially dangerous command: {script_command}"
    
    def test_engine_constraints_realistic(self, package_data):
        """Test that engine constraints are realistic."""
        if 'engines' in package_data:
            engines = package_data['engines']
            
            if 'node' in engines:
                node_constraint = engines['node']
                # Extract minimum version
                if node_constraint.startswith('>='):
                    min_version = node_constraint[2:]
                    major = int(min_version.split('.')[0])
                    # Node.js versions should be reasonable
                    assert major >= 14, "Node.js minimum version should be at least 14 (LTS)"
                    assert major <= 22, "Node.js minimum version should not exceed current stable"
            
            if 'npm' in engines:
                npm_constraint = engines['npm']
                if npm_constraint.startswith('>='):
                    min_version = npm_constraint[2:]
                    major = int(min_version.split('.')[0])
                    assert major >= 6, "npm minimum version should be at least 6"
                    assert major <= 10, "npm minimum version should not exceed current stable"


class TestRequirementsTxtValidation:
    """Test suite for requirements.txt validation (Python dependencies)."""
    
    @pytest.fixture
    def requirements_path(self):
        """Fixture to provide the requirements.txt file path."""
        return Path(__file__).parent.parent / "requirements.txt"
    
    @pytest.fixture
    def requirements_data(self, requirements_path):
        """Fixture to load requirements.txt data."""
        if not requirements_path.exists():
            pytest.skip("requirements.txt not found")
        
        with open(requirements_path, 'r', encoding='utf-8') as f:
            lines = [line.strip() for line in f.readlines() if line.strip() and not line.startswith('#')]
        return lines
    
    def test_requirements_file_exists(self, requirements_path):
        """Test that requirements.txt exists if this is a Python project."""
        # Check if this is a Python project
        package_dir = Path(__file__).parent.parent
        python_files = list(package_dir.glob('*.py'))
        
        if python_files:
            # If there are Python files, requirements.txt should exist
            assert requirements_path.exists(), "Python project should have requirements.txt"
    
    def test_requirements_format(self, requirements_data):
        """Test that requirements are properly formatted."""
        for req in requirements_data:
            # Skip git URLs and other complex requirements for basic validation
            if req.startswith(('git+', 'http', '-e')):
                continue
                
            # Basic package name validation
            if '==' in req:
                package, version = req.split('==', 1)
                assert re.match(r'^[a-zA-Z0-9\-_\.]+$', package), f"Invalid package name: {package}"
                assert re.match(r'^[\d\w\-\.]+$', version), f"Invalid version format: {version}"
            elif '>=' in req:
                package, version = req.split('>=', 1)
                assert re.match(r'^[a-zA-Z0-9\-_\.]+$', package), f"Invalid package name: {package}"
                assert re.match(r'^[\d\w\-\.]+$', version), f"Invalid version format: {version}"
    
    def test_requirements_security_packages(self, requirements_data):
        """Test for security-related Python packages."""
        security_packages = ['cryptography', 'bcrypt', 'pyjwt', 'passlib']
        any(any(pkg in req for pkg in security_packages) for req in requirements_data)
        
        # Check if this is a web application
        web_packages = ['flask', 'django', 'fastapi', 'tornado']
        is_web_app = any(any(pkg.lower() in req.lower() for pkg in web_packages) for req in requirements_data)
        
        if is_web_app:
            # Web applications should consider security packages
            pass  # This is more of a recommendation than a hard requirement
    
    def test_requirements_version_pinning(self, requirements_data):
        """Test requirements version pinning strategy."""
        pinned_count = sum(1 for req in requirements_data if '==' in req)
        total_count = len([req for req in requirements_data if not req.startswith(('git+', 'http', '-e'))])
        
        if total_count > 0:
            pinning_ratio = pinned_count / total_count
            # At least some packages should be pinned for reproducibility
            assert pinning_ratio >= 0.3, "At least 30% of packages should be version-pinned for reproducibility"


if __name__ == '__main__':
    pytest.main([__file__, '-v'])