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
    def gemini_api_key(self) -> str:
        """Retorna a chave da API do Gemini."""
        return os.getenv('GEMINI_API_KEY')

    @property
    def model_name(self) -> str:
        """Retorna o nome do modelo Gemini a ser utilizado."""
        return os.getenv('GEMINI_MODEL', 'gemini-2.5-flash')

    @property
    def exams_directory(self) -> str:
        """Retorna o diretório onde os exames estão armazenados."""
        return os.getenv('EXAMS_DIR', 'exames')

    def _validate_config(self):
        """Valida se as configurações necessárias estão presentes."""
        if not self.gemini_api_key:
            raise ValueError(
                "GEMINI_API_KEY não encontrada! "
                "Crie um arquivo .env com sua chave da API."
            )


# Instância global de configuração
config = Config()

