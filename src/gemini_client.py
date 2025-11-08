"""
Cliente para interação com a API do Google Gemini.
"""
import json
import google.generativeai as genai

from src.config import config
from src.prompts import get_analysis_prompt


class GeminiClient:
    """Cliente para análise de exames usando Google Gemini."""

    def __init__(self):
        """Inicializa o cliente Gemini."""
        genai.configure(api_key=config.gemini_api_key)
        self.model = genai.GenerativeModel(config.model_name)

    def analyze_exam(self, exam_content: str) -> dict:
        """
        Analisa o conteúdo do exame usando Google Gemini.

        Args:
            exam_content: Conteúdo do exame em texto

        Returns:
            Dicionário com os dados da análise

        Raises:
            json.JSONDecodeError: Se a resposta não for um JSON válido
            Exception: Para outros erros na API
        """
        prompt = get_analysis_prompt(exam_content)

        try:
            response = self.model.generate_content(prompt)
            return self._parse_response(response.text)
        except Exception as e:
            raise Exception(f"Erro ao analisar exame com Gemini: {e}")

    def _parse_response(self, response_text: str) -> dict:
        """
        Faz o parse da resposta do Gemini para JSON.

        Args:
            response_text: Texto retornado pela API

        Returns:
            Dicionário com os dados parseados
        """
        # Remove possíveis marcadores de código
        cleaned_text = response_text.strip()

        if cleaned_text.startswith('```json'):
            cleaned_text = cleaned_text[7:]
        if cleaned_text.startswith('```'):
            cleaned_text = cleaned_text[3:]
        if cleaned_text.endswith('```'):
            cleaned_text = cleaned_text[:-3]

        # Parse do JSON
        return json.loads(cleaned_text.strip())

