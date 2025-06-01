# Claude Scaffold Test Suite

This directory contains comprehensive unit tests for the Claude Scaffold project.

## Test Structure

```
tests/
├── conftest.py                    # Pytest configuration and fixtures
├── test_cli.py                    # CLI interface tests
├── test_claude_enhancer.py        # Claude enhancer module tests
├── test_claude_interactive.py     # Claude interactive setup tests
├── test_claude_processor.py       # Claude processor tests
├── test_documentation_generator.py # Documentation generator tests
├── test_formatters.py             # Formatter utility tests
├── test_interactive_collectors.py # Interactive collector tests
├── test_interactive_setup.py      # Interactive setup tests
├── test_project_config.py         # Project configuration tests
├── test_project_creator.py        # Project creator tests
├── test_project_helpers.py        # Project helper tests
├── test_scaffold.py               # Main scaffold module tests
├── test_task_manager.py           # Task manager tests
├── test_template_base.py          # Base template tests
├── test_template_commands.py      # Command template tests
└── test_templates.py              # Template system tests
```

## Running Tests

### Run all tests with coverage:
```bash
# Using the test runner script
./run_tests.py

# Or directly with pytest
pytest -v --cov=src --cov-report=term-missing --cov-report=html
```

### Run specific test file:
```bash
./run_tests.py tests/test_cli.py

# Or
pytest tests/test_cli.py -v
```

### Run specific test:
```bash
pytest tests/test_cli.py::TestCLI::test_new_command_default -v
```

### Run tests by marker:
```bash
# Run only unit tests
pytest -m unit

# Run only integration tests
pytest -m integration

# Skip slow tests
pytest -m "not slow"
```

## Test Coverage Goals

- **Target Coverage**: 80% minimum
- **Critical Modules**: 90%+ coverage for core functionality
- **Focus Areas**:
  - All public methods
  - Error handling paths
  - Edge cases
  - Integration points

## Writing Tests

### Test Structure
```python
class TestModuleName:
    """Test cases for module functionality."""
    
    def setup_method(self):
        """Set up test fixtures."""
        # Initialize test objects
    
    def test_method_success(self):
        """Test successful execution."""
        # Arrange
        # Act
        # Assert
    
    def test_method_failure(self):
        """Test failure scenarios."""
        # Test error handling
```

### Using Fixtures
```python
def test_with_fixtures(temp_dir, mock_project_data):
    """Test using pytest fixtures."""
    # temp_dir: temporary directory
    # mock_project_data: sample project configuration
```

### Mocking Guidelines
```python
@patch('module.external_dependency')
def test_with_mock(mock_dep):
    """Test with mocked dependencies."""
    mock_dep.return_value = 'expected'
    # Test isolated unit
```

## Test Categories

### Unit Tests
- Test individual functions/methods
- Mock all external dependencies
- Fast execution
- High coverage

### Integration Tests
- Test module interactions
- Limited mocking
- Test file system operations
- Test CLI commands

### Claude Integration Tests
- Test Claude CLI interactions
- Mock subprocess calls
- Test prompt generation
- Test response parsing

## Common Test Patterns

### Testing CLI Commands
```python
@patch('sys.argv', ['command', 'arg1', 'arg2'])
def test_cli_command():
    """Test CLI command execution."""
    result = main()
    assert result == 0
```

### Testing File Operations
```python
def test_file_operations(temp_dir):
    """Test file creation/modification."""
    test_file = temp_dir / 'test.txt'
    # Perform operations
    assert test_file.exists()
```

### Testing Interactive Prompts
```python
@patch('questionary.text')
def test_interactive(mock_text):
    """Test interactive user input."""
    mock_text.return_value.ask.return_value = 'user input'
    # Test interaction
```

## Debugging Tests

### Run with verbose output:
```bash
pytest -vv
```

### Show print statements:
```bash
pytest -s
```

### Debug specific test:
```bash
pytest --pdb tests/test_file.py::test_name
```

### Generate detailed HTML report:
```bash
pytest --cov=src --cov-report=html
# Open htmlcov/index.html
```

## Continuous Integration

Tests are automatically run on:
- Every push to main branch
- Every pull request
- Can be triggered manually

## Contributing Tests

When adding new features:
1. Write tests first (TDD)
2. Ensure all tests pass
3. Maintain or improve coverage
4. Document complex test scenarios
5. Use meaningful test names
6. Group related tests in classes

## Test Maintenance

- Regularly review and update tests
- Remove obsolete tests
- Refactor duplicate test code
- Keep tests simple and focused
- Ensure tests are deterministic