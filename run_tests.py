#!/usr/bin/env python3
"""Test runner for Claude Scaffold with coverage reporting."""

import sys
import subprocess
import os
from pathlib import Path


def run_tests():
    """Run the test suite with coverage."""
    print("🧪 Running Claude Scaffold Test Suite")
    print("=" * 60)
    
    # Change to project root
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # Install test dependencies if needed
    print("📦 Checking test dependencies...")
    try:
        import pytest
        import pytest_cov
    except ImportError:
        print("Installing test dependencies...")
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements-dev.txt"])
    
    # Run tests with coverage
    print("\n🚀 Running tests with coverage...")
    cmd = [
        sys.executable,
        "-m",
        "pytest",
        "--verbose",
        "--cov=src",
        "--cov-report=term-missing",
        "--cov-report=html",
        "--cov-fail-under=80",
    ]
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print("\n✅ All tests passed!")
        print("📊 Coverage report generated in htmlcov/index.html")
    else:
        print("\n❌ Tests failed!")
        sys.exit(1)
    
    # Run specific test categories if requested
    if len(sys.argv) > 1:
        category = sys.argv[1]
        print(f"\n🎯 Running {category} tests...")
        cmd.extend(["-m", category])
        subprocess.run(cmd)


def run_linting():
    """Run code quality checks."""
    print("\n🔍 Running code quality checks...")
    
    # Run flake8
    print("Running flake8...")
    subprocess.run([sys.executable, "-m", "flake8", "src", "--max-line-length=100"])
    
    # Run black check
    print("Running black...")
    subprocess.run([sys.executable, "-m", "black", "src", "--check"])
    
    # Run isort check
    print("Running isort...")
    subprocess.run([sys.executable, "-m", "isort", "src", "--check-only"])


if __name__ == "__main__":
    print("""
    ╔═══════════════════════════════════════════════════════════════╗
    ║                 Claude Scaffold Test Suite                    ║
    ╚═══════════════════════════════════════════════════════════════╝
    """)
    
    # Run tests
    run_tests()
    
    # Optionally run linting
    if "--lint" in sys.argv:
        run_linting()