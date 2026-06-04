# ClickPalm-IA

Análise automatizada de laudos de mamografia com IA, com suporte a múltiplos
provedores: **Google Gemini** e **Amazon Nova Lite (via Bedrock)**.

## Instalação

```bash
pip install -r requirements.txt
```

Copie `.env.example` para `.env` e preencha as credenciais:

```
AI_PROVIDER=gemini            # 'gemini' ou 'nova'
GEMINI_API_KEY=sua_chave_aqui
GEMINI_MODEL=gemini-3.1-flash-lite
AWS_REGION=us-east-1
NOVA_MODEL_ID=us.amazon.nova-lite-v1:0
```

### Acesso ao Amazon Nova (Bedrock)

Para usar o Nova Lite é necessário:

1. Habilitar o acesso ao modelo **Amazon Nova Lite** no console do Bedrock
   (região `us-east-1`), em **Bedrock → Model access**.
2. Autenticar de uma das formas:
   - **API key do Bedrock (recomendada)** — gere uma chave de longo prazo em
     **Bedrock → API keys** e coloque em `AWS_BEARER_TOKEN_BEDROCK` no `.env`.
     É um token único, lido automaticamente pelo boto3.
   - **Credenciais IAM** — `AWS_ACCESS_KEY_ID` / `AWS_SECRET_ACCESS_KEY` (ou
     `aws configure`). A IAM precisa da permissão `bedrock:InvokeModel`.

## Uso

1. Coloque os arquivos `.txt` na pasta `exames/`
2. Execute: `python main.py`
3. Os resultados serão salvos como `_analise.json`

O modelo usado pelo `main.py` é definido por `AI_PROVIDER` no `.env`.

## Comparação de modelos (Gemini vs Nova Lite)

Para comparar os dois provedores nos mesmos laudos:

```bash
python compare.py
python compare.py --runs 3        # 3 execuções por modelo (média de tempo)
```

O `compare.py` mede:

- **Tempo de resposta** de cada modelo (apenas a chamada à IA), em ms.
- **Concordância de extração** campo a campo entre os dois modelos
  (cisto, nódulo, calcificação, microcalcificação e BI-RADS).

Saídas geradas:

- `comparison_report.json` — relatório completo (tempos + concordância + saídas).
- `<laudo>_gemini.json` e `<laudo>_nova.json` — extrações lado a lado para
  revisão manual das divergências.

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
