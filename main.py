"""
ClickPalm - Sistema de análise de laudos de mamografia com IA
Ponto de entrada principal da aplicação.
"""
from src.exam_analyzer import ExamAnalyzer


def main():
    """Função principal da aplicação."""
    try:
        analyzer = ExamAnalyzer()
        analyzer.run()
    except Exception as e:
        print(f"\nERRO: {e}")


if __name__ == "__main__":
    main()