"""
Processador de arquivos de exames.
"""
import json
import os
from typing import Optional

from src.gemini_client import GeminiClient


class FileProcessor:
    """Processador de arquivos de exames médicos."""

    def __init__(self):
        """Inicializa o processador."""
        self.gemini_client = GeminiClient()

    def process_file(self, file_path: str, force_reprocess: bool = False) -> dict:
        """
        Processa um arquivo de exame.

        Args:
            file_path: Caminho para o arquivo de texto
            force_reprocess: Se True, força o reprocessamento mesmo se o JSON já existir

        Returns:
            Dicionário com a análise do exame

        Raises:
            FileNotFoundError: Se o arquivo não existir
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Arquivo não encontrado: {file_path}")

        # Define o nome do arquivo JSON de saída
        json_file = self._get_json_file_path(file_path)

        # Verifica se já existe análise e não força reprocessamento
        if os.path.exists(json_file) and not force_reprocess:
            print(f"Análise já existe: {os.path.basename(file_path)}")
            return self._load_json(json_file)

        # Lê o conteúdo do arquivo
        exam_content = self._read_file(file_path)

        # Analisa com Gemini
        print(f"Analisando: {os.path.basename(file_path)}")
        analysis = self.gemini_client.analyze_exam(exam_content)

        # Salva o resultado
        self._save_json(json_file, analysis)
        print(f"Salvo em: {os.path.basename(json_file)}")

        return analysis

    def _get_json_file_path(self, text_file_path: str) -> str:
        """
        Retorna o caminho do arquivo JSON correspondente.

        Args:
            text_file_path: Caminho do arquivo de texto

        Returns:
            Caminho do arquivo JSON
        """
        base_name = os.path.splitext(text_file_path)[0]
        return f"{base_name}_analise.json"

    def _read_file(self, file_path: str) -> str:
        """
        Lê o conteúdo de um arquivo.

        Args:
            file_path: Caminho do arquivo

        Returns:
            Conteúdo do arquivo
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()

    def _load_json(self, json_file: str) -> dict:
        """
        Carrega um arquivo JSON.

        Args:
            json_file: Caminho do arquivo JSON

        Returns:
            Dicionário com os dados do JSON
        """
        with open(json_file, 'r', encoding='utf-8') as f:
            return json.load(f)

    def _save_json(self, json_file: str, data: dict) -> None:
        """
        Salva dados em um arquivo JSON.

        Args:
            json_file: Caminho do arquivo JSON
            data: Dados a serem salvos
        """
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

