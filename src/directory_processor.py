"""
Processador de diretórios com arquivos de exames.
"""
import glob
import os

from src.file_processor import FileProcessor


class DirectoryProcessor:
    """Processador de diretórios com múltiplos arquivos de exames."""

    def __init__(self):
        """Inicializa o processador de diretórios."""
        self.file_processor = FileProcessor()

    def process_directory(self, directory_path: str) -> dict:
        """
        Processa todos os arquivos de texto em um diretório.

        Args:
            directory_path: Caminho do diretório

        Returns:
            Dicionário com estatísticas do processamento

        Raises:
            FileNotFoundError: Se o diretório não existir
        """
        if not os.path.exists(directory_path):
            raise FileNotFoundError(f"Diretório não encontrado: {directory_path}")

        # Encontra todos os arquivos .txt
        text_files = glob.glob(os.path.join(directory_path, "*.txt"))

        if not text_files:
            print(f"Nenhum arquivo .txt encontrado em: {directory_path}")
            return {
                'total': 0,
                'processed': 0,
                'skipped': 0,
                'errors': 0
            }

        print(f"\nEncontrados {len(text_files)} arquivo(s) .txt")
        print("=" * 60)

        stats = {
            'total': len(text_files),
            'processed': 0,
            'skipped': 0,
            'errors': 0
        }

        # Processa cada arquivo
        for file_path in text_files:
            try:
                # Verifica se o JSON já existe ANTES de processar
                json_path = self.file_processor._get_json_file_path(file_path)
                json_existed_before = os.path.exists(json_path)

                # Processa o arquivo
                result = self.file_processor.process_file(file_path)

                # Conta como processado apenas se foi criado agora
                if json_existed_before:
                    stats['skipped'] += 1
                else:
                    stats['processed'] += 1

            except Exception as e:
                stats['errors'] += 1
                print(f"ERRO em {os.path.basename(file_path)}: {e}")

        return stats

    def print_summary(self, stats: dict) -> None:
        """
        Imprime um resumo do processamento.

        Args:
            stats: Dicionário com estatísticas do processamento
        """
        print("\n" + "=" * 60)
        print("RESUMO DO PROCESSAMENTO")
        print("=" * 60)
        print(f"Total de arquivos: {stats['total']}")
        print(f"Processados: {stats['processed']}")
        print(f"Já existiam: {stats['skipped']}")
        print(f"Erros: {stats['errors']}")
        print("=" * 60)

