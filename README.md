# ClickPalm-IA

Análise automatizada de laudos de mamografia com Google Gemini AI.

## Instalação

```bash
pip install -r requirements.txt
```

Configure a chave da API no arquivo `.env`:
```
GEMINI_API_KEY=sua_chave_aqui
```

## Uso

1. Coloque os arquivos `.txt` na pasta `exames/`
2. Execute: `python main.py`
3. Os resultados serão salvos como `_analise.json`

## Estrutura de Saída

```json
{
    "cisto": {"presente": true, "detalhes": "..."},
    "nodulo": {"presente": false, "detalhes": "..."},
    "calcificacao": {"presente": false, "detalhes": "..."},
    "microcalcificacao": {"presente": false, "detalhes": "..."},
    "bi_rads": "2",
    "outras_citacoes": "..."
}
```
