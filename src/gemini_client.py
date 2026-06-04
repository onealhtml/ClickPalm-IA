"""
Cliente para interação com a API do Google Gemini.
"""
import time
from google import genai

from src.ai_client import AIExamClient
from src.config import config
from src.prompts import get_analysis_prompt


class GeminiClient(AIExamClient):
    """Cliente para análise de exames usando Google Gemini."""

    provider = "gemini"

    def __init__(self):
        """Inicializa o cliente Gemini."""
        self.client = genai.Client(api_key=config.gemini_api_key)
        self.model_name = config.model_name

    def analyze_exam_with_timing(self, exam_content: str) -> tuple[dict, int]:
        """
        Analisa o exame e retorna também o tempo da resposta da IA em nanossegundos.

        O tempo mede apenas a chamada remota ao modelo (generate_content),
        sem incluir o parse do JSON de resposta.

        Args:
            exam_content: Conteúdo do exame em texto

        Returns:
            Tupla (análise, tempo_em_nanossegundos)

        Raises:
            Exception: Para erros na chamada ao Gemini.
        """
        prompt = get_analysis_prompt(exam_content)

        try:
            start_ns = time.perf_counter_ns()
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
            )
            elapsed_ns = time.perf_counter_ns() - start_ns
            return self._parse_response(response.text), elapsed_ns
        except Exception as e:
            raise Exception(f"Erro ao analisar exame com Gemini: {e}")
