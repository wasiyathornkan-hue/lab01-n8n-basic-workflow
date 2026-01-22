"""
Pytest Configuration for Lab 01
"""

import pytest
import os


def pytest_configure(config):
    """Configure pytest"""
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )


def pytest_collection_modifyitems(config, items):
    """Modify test collection"""
    # เรียงลำดับ tests ตามชื่อ
    items.sort(key=lambda x: x.name)


@pytest.fixture(scope="session")
def n8n_url():
    """Get n8n base URL from environment"""
    return os.environ.get("N8N_BASE_URL", "http://localhost:5678")


@pytest.fixture(scope="session")
def webhook_url(n8n_url):
    """Get webhook URL"""
    return f"{n8n_url}/webhook-test/lab01"
