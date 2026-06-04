"""
Cliente para interação com o Amazon Bedrock (modelo Amazon Nova Lite).

Utiliza a API Converse do Bedrock Runtime, que oferece uma interface
unificada de mensagens para os modelos Nova.
"""
import time

from src.ai_client import AIExamClient
from src.config import config
from src.prompts import get_analysis_prompt


class NovaClient(AIExamClient):
    """Cliente para análise de exames usando Amazon Nova Lite via Bedrock."""

    provider = "nova"

    def __init__(self):
        """Inicializa o cliente Bedrock Runtime para o Amazon Nova."""
        # Importação tardia: boto3 só é necessário quando o Nova é usado.
        import boto3

        self.model_name = config.nova_model_id
        self.client = boto3.client(
            "bedrock-runtime",
            region_name=config.aws_region,
        )

    def analyze_exam_with_timing(self, exam_content: str) -> tuple[dict, int]:
        """
        Analisa o exame com o Amazon Nova e retorna o tempo da resposta.

        O tempo mede apenas a chamada remota ao modelo (converse), sem incluir
        o parse do JSON de resposta.

        Args:
            exam_content: Conteúdo do exame em texto

        Returns:
            Tupla (análise, tempo_em_nanossegundos)

        Raises:
            Exception: Para erros na chamada ao Bedrock.
        """
        prompt = get_analysis_prompt(exam_content)

        try:
            start_ns = time.perf_counter_ns()
            response = self.client.converse(
                modelId=self.model_name,
                messages=[{"role": "user", "content": [{"text": prompt}]}],
                inferenceConfig={
                    "maxTokens": 2000,
                    "temperature": 0.2,
                    "topP": 0.9,
                },
            )
            elapsed_ns = time.perf_counter_ns() - start_ns

            text = response["output"]["message"]["content"][0]["text"]
            return self._parse_response(text), elapsed_ns
        except Exception as e:
            raise Exception(f"Erro ao analisar exame com Amazon Nova (Bedrock): {e}")
