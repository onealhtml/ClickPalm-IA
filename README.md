# ClickPalm - IA Exam Analyzer 🏥🤖

Sistema inteligente de análise de laudos de mamografia utilizando Google Gemini AI.

## 📋 Descrição

Este projeto utiliza inteligência artificial (Google Gemini) para analisar automaticamente relatórios de mamografia, extraindo informações estruturadas sobre:

- **Cistos**: Presença, localização e tamanho
- **Nódulos**: Presença, localização e tamanho
- **Calcificações**: Presença, localização e tamanho
- **Microcalcificações**: Presença, localização e tamanho
- **Classificação BI-RADS**: Categoria do exame
- **Outras observações**: Informações adicionais relevantes

## 🚀 Funcionalidades

- ✅ Processamento em lote de múltiplos laudos
- ✅ Análise inteligente com IA generativa
- ✅ Diferenciação automática entre nódulos e cistos
- ✅ Identificação de calcificações e microcalcificações
- ✅ Extração da classificação BI-RADS
- ✅ Saída em formato JSON estruturado
- ✅ Evita reprocessamento de arquivos já analisados

## 📦 Instalação

### Pré-requisitos

- Python 3.8 ou superior
- Chave de API do Google Gemini

### Passos

1. Clone o repositório:
```bash
git clone https://github.com/onealhtml/ClickPalm-IA
cd ClickPalm-IA
```

2. Crie um ambiente virtual (recomendado):
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/Mac
source .venv/bin/activate
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Configure a chave de API:
   - Crie um arquivo `.env` na raiz do projeto
   - Adicione sua chave da API do Google Gemini:
```
GEMINI_API_KEY=sua_chave_aqui
```

## 🔑 Obtendo a Chave da API do Google Gemini

1. Acesse [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Faça login com sua conta Google
3. Clique em "Create API Key"
4. Copie a chave gerada e adicione ao arquivo `.env`

## 💻 Uso

1. Crie a pasta `exames` (se não existir):
```bash
mkdir exames
```

2. Adicione seus arquivos de laudo em formato `.txt` na pasta `exames/`

3. Execute o script:
```bash
python main.py
```

4. Os resultados serão salvos como arquivos JSON na mesma pasta `exames/`, com o sufixo `_analise.json`

### Exemplo de Estrutura de Arquivos

```
ClickPalm-IA/
├── exames/
│   ├── paciente001.txt
│   ├── paciente001_analise.json
│   ├── paciente002.txt
│   └── paciente002_analise.json
├── main.py
├── .env
├── requirements.txt
└── README.md
```

## 📄 Formato de Saída

O sistema gera arquivos JSON com a seguinte estrutura:

```json
{
    "cisto": {
        "presente": true,
        "detalhes": "junção dos quadrantes internos à esquerda, medindo cerca de 1,0 cm"
    },
    "nodulo": {
        "presente": false,
        "detalhes": "[sem referência no texto]"
    },
    "calcificacao": {
        "presente": false,
        "detalhes": "[sem referência no texto]"
    },
    "microcalcificacao": {
        "presente": false,
        "detalhes": "[sem referência no texto]"
    },
    "bi_rads": "2",
    "outras_citacoes": "[sem referência no texto]"
}
```

## 🔧 Tecnologias Utilizadas

- **Python 3.8+**
- **Google Generative AI (Gemini)**: Modelo de IA para análise de texto
- **python-dotenv**: Gerenciamento de variáveis de ambiente

## 🤝 Contribuindo

Contribuições são bem-vindas! Sinta-se à vontade para:

1. Fazer um fork do projeto
2. Criar uma branch para sua feature (`git checkout -b feature/MinhaFeature`)
3. Commit suas mudanças (`git commit -m 'Adiciona MinhaFeature'`)
4. Push para a branch (`git push origin feature/MinhaFeature`)
5. Abrir um Pull Request

## ⚠️ Avisos Importantes

- **Privacidade**: Este sistema processa dados médicos sensíveis. Garanta conformidade com LGPD/HIPAA
- **Uso Clínico**: Os resultados devem ser validados por profissionais qualificados
- **API**: Verifique os limites de uso da API do Google Gemini

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 👨‍💻 Autor

Desenvolvido por [Lorenzo Farias](https://github.com/onealhtml)

---

⭐ Se este projeto foi útil para você, considere dar uma estrela no GitHub!

