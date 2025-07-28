"""
Test configuration and fixtures for the test suite.
"""
import os
import sys
import pytest
from unittest.mock import Mock, patch

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

try:
    from adls_connection import ADLSConfig, ADLSConnection
except ImportError:
    # Handle the case where the module name has dashes
    import importlib.util
    spec = importlib.util.spec_from_file_location("adls_connection", 
                                                  os.path.join(os.path.dirname(__file__), '..', 'src', 'adls-connection.py'))
    adls_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(adls_module)
    ADLSConfig = adls_module.ADLSConfig
    ADLSConnection = adls_module.ADLSConnection


@pytest.fixture
def valid_adls_config():
    """Fixture for a valid ADLS configuration."""
    return ADLSConfig(
        adls_url="https://teststorage.blob.core.windows.net",
        container_name="test-container"
    )


@pytest.fixture
def mock_blob_service_client():
    """Fixture for mocking BlobServiceClient."""
    with patch('adls_connection.BlobServiceClient') as mock_client:
        yield mock_client


@pytest.fixture
def mock_default_azure_credential():
    """Fixture for mocking DefaultAzureCredential."""
    with patch('adls_connection.DefaultAzureCredential') as mock_credential:
        yield mock_credential


@pytest.fixture
def mock_environment_variables():
    """Fixture for mocking environment variables."""
    env_vars = {
        "ADLS_URL": "https://teststorage.blob.core.windows.net",
        "AZURE_STORAGE_CONTAINER_NAME": "test-container"
    }
    with patch.dict(os.environ, env_vars):
        yield env_vars


@pytest.fixture
def sample_blob_content():
    """Fixture for sample blob content."""
    return "Sample PDF content from Azure Blob Storage"
