"""
Exemplo de uso da biblioteca ADLS Connection
Este arquivo demonstra como usar as classes e funções da biblioteca.
"""
import os
import sys
import importlib.util

# Importar o módulo usando importlib devido ao dash no nome do arquivo
spec = importlib.util.spec_from_file_location("adls_connection", 
                                              os.path.join(os.path.dirname(__file__), 'src', 'adls-connection.py'))
adls_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(adls_module)

ADLSConnection = adls_module.ADLSConnection
ADLSConfig = adls_module.ADLSConfig
connected_agent_tool_read_json = adls_module.connected_agent_tool_read_json


def exemplo_basico():
    """Exemplo básico de uso com variáveis de ambiente."""
    print("=== Exemplo Básico ===")
    
    # Opção 1: Usando variáveis de ambiente (.env)
    try:
        connection = ADLSConnection()
        print(f"Conectado ao ADLS: {connection.config.adls_url}")
        print(f"Container: {connection.config.container_name}")
        
        # Tentativa de leitura de um arquivo
        content = connection.read_blob_content("exemplo-documento", "pdf")
        if content:
            print(f"Conteúdo lido: {content[:100]}...")  # Primeiros 100 caracteres
        else:
            print("Não foi possível ler o documento (pode não existir)")
            
    except ValueError as e:
        print(f"Erro de configuração: {e}")
    except Exception as e:
        print(f"Erro inesperado: {e}")


def exemplo_configuracao_explicita():
    """Exemplo usando configuração explícita."""
    print("\n=== Exemplo com Configuração Explícita ===")
    
    # Opção 2: Usando configuração explícita
    try:
        config = ADLSConfig(
            adls_url="https://exemploteste.blob.core.windows.net",
            container_name="documentos-quantitativos"
        )
        
        connection = ADLSConnection(config)
        print("Conexão criada com configuração explícita")
        
        # Testando diferentes tipos de arquivo
        for file_type in ["pdf", "json", "txt"]:
            content = connection.read_blob_content("relatorio-mensal", file_type)
            if content:
                print(f"Arquivo {file_type} encontrado: {len(content)} caracteres")
            else:
                print(f"Arquivo {file_type} não encontrado")
                
    except Exception as e:
        print(f"Erro: {e}")


def exemplo_funcao_legacy():
    """Exemplo usando a função legacy."""
    print("\n=== Exemplo com Função Legacy ===")
    
    # Usando a função legacy para compatibilidade
    try:
        content = connected_agent_tool_read_json("documento-importante")
        if content:
            print(f"Conteúdo via função legacy: {content[:50]}...")
        else:
            print("Documento não encontrado via função legacy")
            
    except Exception as e:
        print(f"Erro na função legacy: {e}")


def exemplo_validacao():
    """Exemplo de validação de configuração."""
    print("\n=== Exemplo de Validação ===")
    
    # Testando validações
    configuracoes_teste = [
        {"adls_url": "http://invalid.com", "container_name": "test"},  # URL inválida
        {"adls_url": "https://valid.blob.core.windows.net", "container_name": ""},  # Container vazio
        {"adls_url": "https://valid.blob.core.windows.net", "container_name": "valid-container"},  # Válida
    ]
    
    for i, config_data in enumerate(configuracoes_teste, 1):
        try:
            config = ADLSConfig(**config_data)
            print(f"Configuração {i}: ✓ Válida")
        except Exception as e:
            print(f"Configuração {i}: ✗ Inválida - {e}")


def exemplo_tratamento_erro():
    """Exemplo de tratamento de erros."""
    print("\n=== Exemplo de Tratamento de Erros ===")
    
    try:
        # Configuração válida mas arquivo inexistente
        config = ADLSConfig(
            adls_url="https://teste.blob.core.windows.net",
            container_name="container-inexistente"
        )
        
        connection = ADLSConnection(config)
        
        # Tentativa de leitura que deve falhar
        content = connection.read_blob_content("arquivo-inexistente", "pdf")
        
        if content is None:
            print("Tratamento correto: arquivo não encontrado retornou None")
        else:
            print(f"Conteúdo inesperado: {content}")
            
    except Exception as e:
        print(f"Erro capturado: {e}")


if __name__ == "__main__":
    print("Demonstração da Biblioteca ADLS Connection")
    print("=" * 50)
    
    # Verificar se as variáveis de ambiente estão configuradas
    if not os.getenv("ADLS_URL"):
        print("AVISO: Variável ADLS_URL não configurada")
        print("Para usar os exemplos, configure o arquivo .env")
        print("Veja .env.example para referência")
        print()
    
    # Executar exemplos
    exemplo_validacao()
    exemplo_configuracao_explicita()
    exemplo_funcao_legacy()
    exemplo_tratamento_erro()
    
    # Só executar exemplo básico se as variáveis estiverem configuradas
    if os.getenv("ADLS_URL") and os.getenv("AZURE_STORAGE_CONTAINER_NAME"):
        exemplo_basico()
    else:
        print("\n=== Exemplo Básico ===")
        print("Pulado: variáveis de ambiente não configuradas")
    
    print("\n" + "=" * 50)
    print("Demonstração concluída!")
