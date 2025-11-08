"""
Analisador principal de exames médicos.
"""
import os

from src.config import config
from src.directory_processor import DirectoryProcessor


class ExamAnalyzer:
    """Classe principal para análise de exames médicos."""

    def __init__(self):
        """Inicializa o analisador de exames."""
        self.directory_processor = DirectoryProcessor()

    def run(self) -> None:
        """
        Executa o processo de análise de exames.
        """
        print("=" * 60)
        print("CLICKPALM - Analisador de Laudos de Mamografia")
        print("=" * 60)

        # Define o diretório de exames
        exams_dir = config.exams_directory

        # Verifica se o diretório existe
        if not os.path.exists(exams_dir):
            self._create_exams_directory(exams_dir)
            return

        # Processa os arquivos
        stats = self.directory_processor.process_directory(exams_dir)

        # Imprime resumo apenas se houver arquivos
        if stats['total'] > 0:
            self.directory_processor.print_summary(stats)
            print("\nProcessamento concluído!")

    def _create_exams_directory(self, exams_dir: str) -> None:
        """
        Cria o diretório de exames se não existir.

        Args:
            exams_dir: Caminho do diretório
        """
        os.makedirs(exams_dir)
        print(f"\nDiretório '{exams_dir}' criado.")
        print(f"\nPor favor:")
        print(f"   1. Adicione os arquivos .txt dos exames no diretório '{exams_dir}'")
        print(f"   2. Execute o programa novamente")
        print("\n" + "=" * 60)
"""
ClickPalm-IA - Sistema de análise de laudos de mamografia com IA
"""

__version__ = "1.0.0"
__author__ = "ClickPalm-IA Team"

