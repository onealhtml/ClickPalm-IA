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
    def gemini_requests_per_minute(self) -> int:
        """Limite local de chamadas por minuto ao Gemini. Use 0 para desativar."""
        return self._get_int_env('GEMINI_REQUESTS_PER_MINUTE', 10, minimum=0)

    @property
    def gemini_max_retries(self) -> int:
        """Número de novas tentativas para erros transitórios do Gemini."""
        return self._get_int_env('GEMINI_MAX_RETRIES', 6, minimum=0)

    @property
    def gemini_retry_initial_delay_seconds(self) -> float:
        """Espera inicial do retry exponencial do Gemini."""
        return self._get_float_env(
            'GEMINI_RETRY_INITIAL_DELAY_SECONDS', 2.0, minimum=0.0
        )

    @property
    def gemini_retry_max_delay_seconds(self) -> float:
        """Espera máxima entre retries do Gemini."""
        return self._get_float_env(
            'GEMINI_RETRY_MAX_DELAY_SECONDS', 60.0, minimum=0.0
        )

    @property
    def gemini_retry_jitter_seconds(self) -> float:
        """Variação aleatória somada ao retry para evitar rajadas sincronizadas."""
        return self._get_float_env(
            'GEMINI_RETRY_JITTER_SECONDS', 1.5, minimum=0.0
        )

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

    def _get_int_env(self, name: str, default: int, minimum: int | None = None) -> int:
        """Lê inteiro de variável de ambiente com mensagem clara em caso inválido."""
        raw = os.getenv(name)
        if raw is None or raw == '':
            return default
        try:
            value = int(raw)
        except ValueError as exc:
            raise ValueError(f"{name} deve ser um número inteiro.") from exc
        if minimum is not None and value < minimum:
            raise ValueError(f"{name} deve ser maior ou igual a {minimum}.")
        return value

    def _get_float_env(
        self, name: str, default: float, minimum: float | None = None
    ) -> float:
        """Lê float de variável de ambiente com mensagem clara em caso inválido."""
        raw = os.getenv(name)
        if raw is None or raw == '':
            return default
        try:
            value = float(raw)
        except ValueError as exc:
            raise ValueError(f"{name} deve ser um número.") from exc
        if minimum is not None and value < minimum:
            raise ValueError(f"{name} deve ser maior ou igual a {minimum}.")
        return value


# Instância global de configuração
config = Config()
