"""
Cliente para interação com a API do Google Gemini.
"""
from email.utils import parsedate_to_datetime
import random
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
        requests_per_minute = config.gemini_requests_per_minute
        self._request_interval_seconds = (
            60.0 / requests_per_minute if requests_per_minute > 0 else 0.0
        )
        self._last_request_started_at = 0.0

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
            response, elapsed_ns = self._generate_content_with_retries(prompt)
            return self._parse_response(response.text), elapsed_ns
        except Exception as e:
            raise Exception(f"Erro ao analisar exame com Gemini: {e}")

    def _generate_content_with_retries(self, prompt: str):
        """
        Executa a chamada ao Gemini com rate limit local e retry para falhas transitórias.

        O tempo retornado mede somente a chamada remota que respondeu com sucesso.
        Esperas por limite local e backoff ficam fora do benchmark.
        """
        max_retries = config.gemini_max_retries
        max_attempts = max_retries + 1

        for attempt in range(1, max_attempts + 1):
            try:
                return self._call_gemini_once(prompt)
            except Exception as error:
                if attempt >= max_attempts or not self._is_transient_error(error):
                    raise

                delay = self._retry_delay_seconds(error, attempt)
                print(
                    "Gemini erro transitório "
                    f"({self._error_label(error)}). "
                    f"Retry {attempt}/{max_retries} em {delay:.1f}s..."
                )
                time.sleep(delay)

    def _call_gemini_once(self, prompt: str):
        """Aplica o limite local e faz uma única chamada ao Gemini."""
        self._wait_for_rate_limit()
        start_ns = time.perf_counter_ns()
        response = self.client.models.generate_content(
            model=self.model_name,
            contents=prompt,
        )
        elapsed_ns = time.perf_counter_ns() - start_ns
        return response, elapsed_ns

    def _wait_for_rate_limit(self) -> None:
        """Espaça chamadas ao Gemini para reduzir estouro de requests por minuto."""
        if self._request_interval_seconds <= 0:
            return

        now = time.monotonic()
        elapsed = now - self._last_request_started_at
        wait_seconds = self._request_interval_seconds - elapsed
        if wait_seconds > 0:
            print(f"Gemini rate limit: aguardando {wait_seconds:.1f}s...")
            time.sleep(wait_seconds)

        self._last_request_started_at = time.monotonic()

    def _retry_delay_seconds(self, error: Exception, attempt: int) -> float:
        """Calcula backoff exponencial, respeitando Retry-After quando vier da API."""
        retry_after = self._retry_after_seconds(error)
        if retry_after is not None:
            return retry_after

        initial_delay = config.gemini_retry_initial_delay_seconds
        max_delay = config.gemini_retry_max_delay_seconds
        delay = initial_delay * (2 ** (attempt - 1))

        if self._error_code(error) == 429 and self._request_interval_seconds > 0:
            delay = max(delay, self._request_interval_seconds)

        if max_delay > 0:
            delay = min(delay, max_delay)

        jitter = config.gemini_retry_jitter_seconds
        if jitter > 0:
            delay += random.uniform(0, jitter)

        return max(delay, 0.0)

    def _retry_after_seconds(self, error: Exception) -> float | None:
        """Extrai Retry-After de headers HTTP, se o SDK disponibilizar."""
        response = getattr(error, "response", None)
        headers = getattr(response, "headers", None)
        if not headers:
            return None

        raw_value = headers.get("Retry-After") or headers.get("retry-after")
        if not raw_value:
            return None

        try:
            return max(float(raw_value), 0.0)
        except ValueError:
            try:
                retry_at = parsedate_to_datetime(raw_value)
            except (TypeError, ValueError):
                return None
            return max(retry_at.timestamp() - time.time(), 0.0)

    def _is_transient_error(self, error: Exception) -> bool:
        """Identifica erros que podem melhorar com espera e nova tentativa."""
        code = self._error_code(error)
        if code in {408, 409, 425, 429, 500, 502, 503, 504}:
            return True

        status = str(getattr(error, "status", "")).upper()
        if status in {
            "ABORTED",
            "DEADLINE_EXCEEDED",
            "INTERNAL",
            "RESOURCE_EXHAUSTED",
            "UNAVAILABLE",
        }:
            return True

        text = str(error).lower()
        transient_markers = (
            "429",
            "503",
            "deadline exceeded",
            "overloaded",
            "quota",
            "rate limit",
            "resource_exhausted",
            "server error",
            "service unavailable",
            "temporarily unavailable",
            "too many requests",
            "unavailable",
        )
        return any(marker in text for marker in transient_markers)

    def _error_code(self, error: Exception) -> int | None:
        """Retorna o código HTTP do erro quando disponível."""
        code = getattr(error, "code", None)
        try:
            return int(code)
        except (TypeError, ValueError):
            return None

    def _error_label(self, error: Exception) -> str:
        """Monta rótulo curto para log de retry."""
        code = self._error_code(error)
        status = getattr(error, "status", None)
        message = getattr(error, "message", None) or str(error)
        parts = []
        if code is not None:
            parts.append(str(code))
        if status:
            parts.append(str(status))
        if message:
            parts.append(str(message).splitlines()[0])
        return " - ".join(parts)
