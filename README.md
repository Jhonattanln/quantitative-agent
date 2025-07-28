# Quantitative Agent - Azure Data Lake Storage Connection

Este projeto fornece uma biblioteca Python para conectar e interagir com o Azure Data Lake Storage (ADLS) usando Pydantic para validação de dados e Azure SDK.

## Características

- **Validação robusta de configuração** usando Pydantic v2
- **Classe orientada a objetos** para conexões ADLS
- **Função legacy** para compatibilidade com código existente
- **Testes unitários abrangentes** usando pytest
- **Tratamento de erros** e logging
- **Suporte a diferentes tipos de arquivo**

## Estrutura do Projeto

```
quantitative-agent/
├── src/
│   ├── __init__.py
│   ├── adls-connection.py     # Módulo principal
│   ├── app.py
│   └── bing-connection.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py           # Configurações e fixtures dos testes
│   ├── test_adls_connection.py  # Testes unitários principais
│   └── test_integration.py   # Testes de integração
├── requirements.txt
├── pytest.ini
└── README.md
```

## Instalação

1. Clone o repositório:
```bash
git clone <repository-url>
cd quantitative-agent
```

2. Crie um ambiente virtual:
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# ou
.venv\Scripts\activate  # Windows
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

## Configuração

Configure as variáveis de ambiente necessárias:

```bash
# .env file
ADLS_URL=https://yourstorageaccount.blob.core.windows.net
AZURE_STORAGE_CONTAINER_NAME=your-container-name
```

## Uso

### Usando a Classe ADLSConnection

```python
from src.adls_connection import ADLSConnection, ADLSConfig

# Opção 1: Usando variáveis de ambiente
connection = ADLSConnection()

# Opção 2: Usando configuração explícita
config = ADLSConfig(
    adls_url="https://mystorageaccount.blob.core.windows.net",
    container_name="my-container"
)
connection = ADLSConnection(config)

# Lendo conteúdo de um blob
content = connection.read_blob_content("document-name", "pdf")
if content:
    print("Conteúdo do documento:", content)
else:
    print("Erro ao ler o documento")
```

### Usando a Função Legacy

```python
from src.adls_connection import connected_agent_tool_read_json

# Função legacy para compatibilidade
content = connected_agent_tool_read_json("document-name")
```

### Validação de Configuração com Pydantic

```python
from src.adls_connection import ADLSConfig
from pydantic import ValidationError

try:
    config = ADLSConfig(
        adls_url="https://valid.blob.core.windows.net",
        container_name="my-container"
    )
except ValidationError as e:
    print("Erro de validação:", e)
```

## Executando os Testes

### Todos os Testes
```bash
pytest
```

### Apenas Testes Unitários
```bash
pytest tests/test_adls_connection.py -v
```

### Excluindo Testes de Integração
```bash
pytest -m "not integration"
```

### Testes com Cobertura
```bash
pytest --cov=src --cov-report=html
```

### Executando Testes Específicos
```bash
# Testes de uma classe específica
pytest tests/test_adls_connection.py::TestADLSConfig -v

# Teste específico
pytest tests/test_adls_connection.py::TestADLSConfig::test_valid_config_creation -v
```

## Estrutura de Testes

### Testes de Unidade

- **TestADLSConfig**: Testa a validação de configuração Pydantic
- **TestADLSConnection**: Testa as funcionalidades da classe principal
- **TestLegacyFunction**: Testa a função legacy para compatibilidade

### Fixtures Disponíveis

- `valid_adls_config`: Configuração válida para testes
- `mock_blob_service_client`: Mock do cliente Azure Blob
- `mock_default_azure_credential`: Mock das credenciais Azure
- `mock_environment_variables`: Mock das variáveis de ambiente
- `sample_blob_content`: Conteúdo de exemplo para testes

## API Reference

### Classe ADLSConfig

Modelo Pydantic para configuração de conexão ADLS.

**Campos:**
- `adls_url` (str): URL do Azure Data Lake Storage (deve ser HTTPS)
- `container_name` (str): Nome do container de armazenamento

**Validações:**
- URL deve começar com 'https://'
- Nome do container não pode estar vazio

### Classe ADLSConnection

Classe principal para interação com ADLS.

**Métodos:**
- `__init__(config: Optional[ADLSConfig] = None)`: Inicializa a conexão
- `read_blob_content(blob_path: str, file_extension: str = "pdf") -> Optional[str]`: Lê conteúdo de um blob

### Função Legacy

- `connected_agent_tool_read_json(paper: str) -> Optional[str]`: Função legacy para compatibilidade

## Tratamento de Erros

A biblioteca inclui tratamento de erros robusto:

- **Validação de configuração**: Usando Pydantic validators
- **Logging de erros**: Para problemas de conexão e leitura
- **Retorno seguro**: Retorna `None` em caso de erro em vez de lançar exceções

## Contribuindo

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -am 'Adiciona nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request

## Dependências

- `azure-storage-blob`: Cliente para Azure Blob Storage
- `azure-identity`: Autenticação Azure
- `pydantic`: Validação de dados
- `python-dotenv`: Carregamento de variáveis de ambiente
- `pytest`: Framework de testes
- `pytest-mock`: Extensões de mock para pytest

## Licença

[Inserir informações de licença aqui]