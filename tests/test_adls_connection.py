"""
Unit tests for ADLS connection module.
"""
import os
import sys
import pytest
from unittest.mock import Mock, patch, MagicMock
from pydantic import ValidationError

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

# Import the module using importlib due to dash in filename
import importlib.util
spec = importlib.util.spec_from_file_location("adls_connection", 
                                              os.path.join(os.path.dirname(__file__), '..', 'src', 'adls-connection.py'))
adls_module = importlib.util.module_from_spec(spec)
sys.modules['adls_connection'] = adls_module  # Add to sys.modules for patch to work
spec.loader.exec_module(adls_module)

ADLSConfig = adls_module.ADLSConfig
ADLSConnection = adls_module.ADLSConnection
connected_agent_tool_read_json = adls_module.connected_agent_tool_read_json


class TestADLSConfig:
    """Test cases for ADLSConfig Pydantic model."""
    
    def test_valid_config_creation(self):
        """Test creating a valid ADLS configuration."""
        config = ADLSConfig(
            adls_url="https://teststorage.blob.core.windows.net",
            container_name="test-container"
        )
        assert config.adls_url == "https://teststorage.blob.core.windows.net"
        assert config.container_name == "test-container"
    
    def test_invalid_adls_url_validation(self):
        """Test validation of invalid ADLS URL."""
        with pytest.raises(ValidationError) as exc_info:
            ADLSConfig(
                adls_url="invalid-url",
                container_name="test-container"
            )
        assert "ADLS URL must be a valid HTTPS URL" in str(exc_info.value)
    
    def test_empty_adls_url_validation(self):
        """Test validation of empty ADLS URL."""
        with pytest.raises(ValidationError) as exc_info:
            ADLSConfig(
                adls_url="",
                container_name="test-container"
            )
        assert "ADLS URL must be a valid HTTPS URL" in str(exc_info.value)
    
    def test_empty_container_name_validation(self):
        """Test validation of empty container name."""
        with pytest.raises(ValidationError) as exc_info:
            ADLSConfig(
                adls_url="https://teststorage.blob.core.windows.net",
                container_name=""
            )
        assert "Container name cannot be empty" in str(exc_info.value)
    
    def test_whitespace_container_name_validation(self):
        """Test validation of whitespace-only container name."""
        with pytest.raises(ValidationError) as exc_info:
            ADLSConfig(
                adls_url="https://teststorage.blob.core.windows.net",
                container_name="   "
            )
        assert "Container name cannot be empty" in str(exc_info.value)
    
    def test_container_name_strip_whitespace(self):
        """Test that container name strips whitespace."""
        config = ADLSConfig(
            adls_url="https://teststorage.blob.core.windows.net",
            container_name="  test-container  "
        )
        assert config.container_name == "test-container"


class TestADLSConnection:
    """Test cases for ADLSConnection class."""
    
    def test_init_with_config(self):
        """Test initialization with provided config."""
        config = ADLSConfig(
            adls_url="https://teststorage.blob.core.windows.net",
            container_name="test-container"
        )
        
        with patch.object(adls_module, 'DefaultAzureCredential') as mock_credential, \
             patch.object(adls_module, 'BlobServiceClient') as mock_blob_service:
            
            connection = ADLSConnection(config)
            
            assert connection.config == config
            mock_credential.assert_called_once()
            mock_blob_service.assert_called_once_with(
                account_url=config.adls_url,
                credential=mock_credential.return_value
            )
    
    @patch.dict(os.environ, {
        'ADLS_URL': 'https://teststorage.blob.core.windows.net',
        'AZURE_STORAGE_CONTAINER_NAME': 'test-container'
    })
    def test_init_with_environment_variables(self):
        """Test initialization with environment variables."""
        with patch.object(adls_module, 'DefaultAzureCredential') as mock_credential, \
             patch.object(adls_module, 'BlobServiceClient') as mock_blob_service, \
             patch.object(adls_module.dotenv, 'load_dotenv') as mock_load_dotenv:
            
            connection = ADLSConnection()
            
            mock_load_dotenv.assert_called_once()
            assert connection.config.adls_url == "https://teststorage.blob.core.windows.net"
            assert connection.config.container_name == "test-container"
            mock_credential.assert_called_once()
            mock_blob_service.assert_called_once()
    
    @patch.dict(os.environ, {}, clear=True)
    def test_init_missing_environment_variables(self):
        """Test initialization with missing environment variables."""
        with patch.object(adls_module.dotenv, 'load_dotenv'):
            with pytest.raises(ValueError) as exc_info:
                ADLSConnection()
            
            assert "ADLS_URL and AZURE_STORAGE_CONTAINER_NAME must be set" in str(exc_info.value)
    
    def test_read_blob_content_success(self):
        """Test successful blob content reading."""
        # Setup
        config = ADLSConfig(
            adls_url="https://teststorage.blob.core.windows.net",
            container_name="test-container"
        )
        
        mock_blob_data = Mock()
        mock_blob_data.readall.return_value = b"Sample PDF content"
        
        mock_blob_client = Mock()
        mock_blob_client.download_blob.return_value = mock_blob_data
        
        with patch.object(adls_module, 'DefaultAzureCredential') as mock_credential, \
             patch.object(adls_module, 'BlobServiceClient') as mock_blob_service:
            
            mock_blob_service_instance = Mock()
            mock_blob_service_instance.get_blob_client.return_value = mock_blob_client
            mock_blob_service.return_value = mock_blob_service_instance
            
            # Test
            connection = ADLSConnection(config)
            result = connection.read_blob_content("test-paper", "pdf")
            
            # Assertions
            assert result == "Sample PDF content"
            mock_blob_service_instance.get_blob_client.assert_called_once_with(
                container="test-container",
                blob="quant/test-paper.pdf"
            )
            mock_blob_client.download_blob.assert_called_once()
            mock_blob_data.readall.assert_called_once()
    
    def test_read_blob_content_exception(self):
        """Test blob content reading with exception."""
        # Setup
        config = ADLSConfig(
            adls_url="https://teststorage.blob.core.windows.net",
            container_name="test-container"
        )
        
        with patch.object(adls_module, 'DefaultAzureCredential'), \
             patch.object(adls_module, 'BlobServiceClient') as mock_blob_service, \
             patch.object(adls_module.logging, 'error') as mock_logging:
            
            mock_blob_service_instance = Mock()
            mock_blob_service_instance.get_blob_client.side_effect = Exception("Blob not found")
            mock_blob_service.return_value = mock_blob_service_instance
            
            # Test
            connection = ADLSConnection(config)
            result = connection.read_blob_content("test-paper", "pdf")
            
            # Assertions
            assert result is None
            mock_logging.assert_called_once()
            assert "Error reading blob" in mock_logging.call_args[0][0]
    
    def test_read_blob_content_different_extension(self):
        """Test blob content reading with different file extension."""
        # Setup
        config = ADLSConfig(
            adls_url="https://teststorage.blob.core.windows.net",
            container_name="test-container"
        )
        
        mock_blob_data = Mock()
        mock_blob_data.readall.return_value = b"Sample JSON content"
        
        mock_blob_client = Mock()
        mock_blob_client.download_blob.return_value = mock_blob_data
        
        with patch.object(adls_module, 'DefaultAzureCredential'), \
             patch.object(adls_module, 'BlobServiceClient') as mock_blob_service:
            
            mock_blob_service_instance = Mock()
            mock_blob_service_instance.get_blob_client.return_value = mock_blob_client
            mock_blob_service.return_value = mock_blob_service_instance
            
            # Test
            connection = ADLSConnection(config)
            result = connection.read_blob_content("test-data", "json")
            
            # Assertions
            assert result == "Sample JSON content"
            mock_blob_service_instance.get_blob_client.assert_called_once_with(
                container="test-container",
                blob="quant/test-data.json"
            )


class TestLegacyFunction:
    """Test cases for the legacy function."""
    
    @patch.dict(os.environ, {
        'ADLS_URL': 'https://teststorage.blob.core.windows.net',
        'AZURE_STORAGE_CONTAINER_NAME': 'test-container'
    })
    def test_connected_agent_tool_read_json_success(self):
        """Test successful execution of legacy function."""
        # Setup
        mock_connection_instance = Mock()
        mock_connection_instance.read_blob_content.return_value = "Sample content"
        
        with patch.object(adls_module, 'ADLSConnection') as mock_adls_connection, \
             patch.object(adls_module.dotenv, 'load_dotenv'):
            
            mock_adls_connection.return_value = mock_connection_instance
            
            # Test
            result = connected_agent_tool_read_json("test-paper")
            
            # Assertions
            assert result == "Sample content"
            mock_adls_connection.assert_called_once()
            mock_connection_instance.read_blob_content.assert_called_once_with("test-paper", "pdf")
    
    @patch.dict(os.environ, {}, clear=True)
    def test_connected_agent_tool_read_json_exception(self):
        """Test legacy function with exception."""
        with patch.object(adls_module.logging, 'error') as mock_logging, \
             patch.object(adls_module.dotenv, 'load_dotenv'):
            
            # Test
            result = connected_agent_tool_read_json("test-paper")
            
            # Assertions
            assert result is None
            mock_logging.assert_called_once()
            assert "Error in legacy function" in mock_logging.call_args[0][0]


if __name__ == "__main__":
    pytest.main([__file__])
