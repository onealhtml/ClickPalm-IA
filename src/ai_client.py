"""
Interface base e fábrica de clientes de IA para análise de exames.

Define um contrato comum (`AIExamClient`) para que diferentes provedores
(Google Gemini, Amazon Nova via Bedrock, etc.) sejam intercambiáveis no
restante da aplicação.
"""
import json
from abc import ABC, abstractmethod


class AIExamClient(ABC):
    """Interface comum para clientes de IA que analisam exames."""

    #: Rótulo legível do provedor (ex.: "gemini", "nova")
    provider: str = "desconhecido"

    #: Nome/identificador do modelo utilizado
    model_name: str = ""

    @abstractmethod
    def analyze_exam_with_timing(self, exam_content: str) -> tuple[dict, int]:
        """
        Analisa o exame e retorna a análise junto do tempo da resposta da IA.

        Args:
            exam_content: Conteúdo do exame em texto

        Returns:
            Tupla (análise, tempo_em_nanossegundos). O tempo mede apenas a
            chamada remota ao modelo, sem incluir o parse do JSON.
        """
        raise NotImplementedError

    def analyze_exam(self, exam_content: str) -> dict:
        """
        Analisa o conteúdo do exame e retorna apenas o dicionário da análise.

        Args:
            exam_content: Conteúdo do exame em texto

        Returns:
            Dicionário com os dados da análise
        """
        analysis, _elapsed_ns = self.analyze_exam_with_timing(exam_content)
        return analysis

    def _parse_response(self, response_text: str) -> dict:
        """
        Faz o parse da resposta do modelo para JSON.

        Tolera marcadores de bloco de código (```json ... ```) e texto extra
        ao redor do objeto JSON.

        Args:
            response_text: Texto retornado pela API

        Returns:
            Dicionário com os dados parseados
        """
        cleaned_text = response_text.strip()

        # Remove marcadores de bloco de código
        if cleaned_text.startswith('```json'):
            cleaned_text = cleaned_text[7:]
        if cleaned_text.startswith('```'):
            cleaned_text = cleaned_text[3:]
        if cleaned_text.endswith('```'):
            cleaned_text = cleaned_text[:-3]
        cleaned_text = cleaned_text.strip()

        try:
            return json.loads(cleaned_text)
        except json.JSONDecodeError:
            # Fallback: extrai o objeto JSON mais externo do texto
            start = cleaned_text.find('{')
            end = cleaned_text.rfind('}')
            if start != -1 and end != -1 and end > start:
                return json.loads(cleaned_text[start:end + 1])
            raise


def get_ai_client(provider: str = None) -> AIExamClient:
    """
    Cria o cliente de IA de acordo com o provedor configurado.

    As importações dos provedores são feitas sob demanda para que dependências
    específicas (ex.: boto3 para o Nova) só sejam exigidas quando realmente
    utilizadas.

    Args:
        provider: 'gemini' ou 'nova'. Se None, usa config.ai_provider.

    Returns:
        Instância de um cliente que implementa AIExamClient.

    Raises:
        ValueError: Se o provedor informado for desconhecido.
    """
    from src.config import config

    provider = (provider or config.ai_provider).lower()

    if provider == 'gemini':
        from src.gemini_client import GeminiClient
        return GeminiClient()
    if provider == 'nova':
        from src.nova_client import NovaClient
        return NovaClient()

    raise ValueError(
        f"Provedor de IA desconhecido: '{provider}'. Use 'gemini' ou 'nova'."
    )
