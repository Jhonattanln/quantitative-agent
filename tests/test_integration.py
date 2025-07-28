"""
Integration tests for ADLS connection module.
These tests are marked as integration tests and can be skipped during unit testing.
"""
import os
import sys
import pytest
from unittest.mock import patch

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

# Import the module
import importlib.util
spec = importlib.util.spec_from_file_location("adls_connection", 
                                              os.path.join(os.path.dirname(__file__), '..', 'src', 'adls-connection.py'))
adls_module = importlib.util.module_from_spec(spec)
sys.modules['adls_connection'] = adls_module
spec.loader.exec_module(adls_module)

ADLSConfig = adls_module.ADLSConfig
ADLSConnection = adls_module.ADLSConnection


@pytest.mark.integration
class TestADLSConnectionIntegration:
    """Integration tests for ADLS connection."""
    
    @pytest.mark.skipif(
        not os.getenv('ADLS_URL') or not os.getenv('AZURE_STORAGE_CONTAINER_NAME'),
        reason="ADLS environment variables not set"
    )
    def test_real_adls_connection(self):
        """Test real ADLS connection (requires valid credentials)."""
        # This test would only run if proper environment variables are set
        # and valid Azure credentials are available
        connection = ADLSConnection()
        assert connection.config.adls_url
        assert connection.config.container_name
        
        # Note: This would require a real blob to exist for full testing
        # result = connection.read_blob_content("test-file", "txt")
        # assert result is not None or result is None  # Either is valid
    
    def test_configuration_validation_integration(self):
        """Integration test for configuration validation."""
        # Test with invalid URL
        with pytest.raises(ValueError, match="ADLS URL must be a valid HTTPS URL"):
            ADLSConfig(adls_url="http://invalid.com", container_name="test")
        
        # Test with valid configuration
        config = ADLSConfig(
            adls_url="https://valid.blob.core.windows.net",
            container_name="test-container"
        )
        assert config.adls_url == "https://valid.blob.core.windows.net"
        assert config.container_name == "test-container"
