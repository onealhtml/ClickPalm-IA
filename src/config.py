"""
Configurações e variáveis de ambiente do sistema.
"""
import os
from dotenv import load_dotenv


class Config:
    """Classe de configuração do sistema."""

    def __init__(self):
        """Inicializa e carrega as configurações."""
        load_dotenv()
        self._validate_config()

    @property
    def ai_provider(self) -> str:
        """Retorna o provedor de IA a ser utilizado ('gemini' ou 'nova')."""
        return os.getenv('AI_PROVIDER', 'gemini').lower()

    @property
    def gemini_api_key(self) -> str:
        """Retorna a chave da API do Gemini."""
        return os.getenv('GEMINI_API_KEY')

    @property
    def model_name(self) -> str:
        """Retorna o nome do modelo Gemini a ser utilizado."""
        return os.getenv('GEMINI_MODEL', 'gemini-3.1-flash-lite')

    @property
    def aws_region(self) -> str:
        """Retorna a região AWS utilizada pelo Amazon Bedrock."""
        return os.getenv('AWS_REGION', 'us-east-1')

    @property
    def nova_model_id(self) -> str:
        """Retorna o identificador do modelo Amazon Nova Lite no Bedrock."""
        return os.getenv('NOVA_MODEL_ID', 'us.amazon.nova-lite-v1:0')

    @property
    def exams_directory(self) -> str:
        """Retorna o diretório onde os exames estão armazenados."""
        return os.getenv('EXAMS_DIR', 'exames')

    def _validate_config(self):
        """Valida se as configurações necessárias estão presentes."""
        # A chave do Gemini só é obrigatória quando esse provedor é utilizado.
        # As credenciais da AWS (Nova) são resolvidas pelo boto3 sob demanda.
        if self.ai_provider == 'gemini' and not self.gemini_api_key:
            raise ValueError(
                "GEMINI_API_KEY não encontrada! "
                "Crie um arquivo .env com sua chave da API."
            )


# Instância global de configuração
config = Config()

