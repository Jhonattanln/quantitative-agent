"""
Connection to Azure Data Lake Storage (ADLS) Gen2 using the Azure SDK for Python.
This module provides classes and functions to connect to ADLS, read blob content, and validate configurations
"""
# %% Libraries]
import os
import dotenv
from pydantic import BaseModel, Field
from azure.storage.blob import BlobServiceClient
from azure.identity import DefaultAzureCredential

# %% Load environment variables
dotenv.load_dotenv()
ADLS_URL = os.getenv("ADLS_URL")
AZURE_STORAGE_CONTAINER_NAME = os.getenv("AZURE_STORAGE_CONTAINER_NAME")
