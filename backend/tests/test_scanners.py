"""
Basic tests for scanners.
Non-compliant: minimal test coverage, no proper test framework setup.
"""
from src.scanners.static_scanner import StaticScanner
from src.scanners.secret_scanner import SecretScanner

def test_static_scanner():
    """Test static scanner finds patterns"""
    scanner = StaticScanner()
    files = [
        {
            "path": "test.py",
            "content": "password = 'secret123'\napi_key = 'key123'"
        }
    ]
    findings = scanner.scan(files)
    assert len(findings) > 0
    assert any(f['category'] == 'hardcoded_secrets' for f in findings)

def test_secret_scanner():
    """Test secret scanner finds secrets"""
    scanner = SecretScanner()
    files = [
        {
            "path": "config.py",
            "content": "API_KEY = 'ghp_1234567890abcdefghijklmnopqrstuvwxyz'"
        }
    ]
    findings = scanner.scan(files)
    assert len(findings) > 0
    assert any(f['category'] == 'github_token' for f in findings)

