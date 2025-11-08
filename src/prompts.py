"""
Prompts e templates para análise de exames com IA.
"""


def get_analysis_prompt(exam_content: str) -> str:
    """
    Retorna o prompt para análise do exame pelo Gemini.

    Args:
        exam_content: Conteúdo do exame a ser analisado

    Returns:
        Prompt formatado para envio à IA
    """
    return f"""Você é um especialista em análise de relatórios de mamografia. Sua tarefa é ler o relatório fornecido e extrair as informações solicitadas na estrutura abaixo. Siga ATENTAMENTE as "Diretrizes de Interpretação".

Estrutura de Saída:
Cisto:
- Presente ou Ausente
- Localização e/ou tamanho do cisto

Nódulo:
- Presente ou Ausente
- Localização e/ou tamanho do nódulo

Calcificação:
- Presente ou Ausente
- Localização e/ou tamanho da calcificação

Microcalcificação:
- Presente ou Ausente
- Localização e/ou tamanho da microcalcificação

BI-RADS: [valor numérico]

Outras citações a avaliar: [observações adicionais relevantes]

Diretrizes de Interpretação:

1.  Identificação Geral de Achados:
    * Para cada categoria principal (Cisto, Nódulo, Calcificação, Microcalcificação), determine o Status (Presente ou Ausente) e, se presente, extraia a Localização e o Tamanho.
    * Se informações específicas não estiverem disponíveis no texto, utilize "[sem referência no texto]".

2.  Diferenciação e Reclassificação Nódulo/Cisto:
    * Definições Básicas: Nódulos são estruturas predominantemente sólidas; cistos são estruturas predominantemente líquidas.
    * Reclassificação de Nódulo Mamográfico para Cisto Ecográfico:
        * Condição de Aplicabilidade: Esta sub-regra de reclassificação aplica-se exclusivamente quando o relatório atual indica que achados de uma MAMOGRAFIA foram subsequentemente (ou conjuntamente) avaliados por ECOGRAFIA (Ultrassonografia) e esta ecografia está esclarecendo a natureza de um achado mamográfico. A simples menção de ambos os exames no histórico não ativa esta regra se não houver uma reclassificação explícita de um achado específico.
        * Ação de Reclassificação: Se, e somente se, a condição acima for atendida, e um achado inicialmente descrito como "nódulo" na mamografia for claramente identificado e reclassificado pela ecografia como "cisto" (ex: "cisto simples", "achado mamográfico corresponde a cisto ao ultrassom", "natureza cística confirmada pela ecografia"), então, para essa lesão específica:
            * Cisto: Status (Presente), com os detalhes fornecidos (idealmente da ecografia).
            * Nódulo: Status (Ausente).
        * Quando NÃO há Reclassificação (Nódulo permanece Nódulo, Cisto permanece Cisto):
            * Se a ecografia confirmar um achado mamográfico como um nódulo sólido (ex: "nódulo sólido correspondente ao achado mamográfico").
            * Se o relatório for apenas de mamografia (sem ecografia complementar descrita para o achado) ou apenas de ecografia (sem referência a um achado mamográfico sendo reclassificado).
            * Se o achado for descrito como um complexo sólido-cístico (ver abaixo).
    * Complexos Sólido-Císticos: Se uma lesão for descrita como tendo componentes tanto sólidos quanto císticos (ex: "nódulo complexo", "cisto com componente sólido", "lesão sólido-cística"), ela deve ser reportada como PRESENTE para AMBAS as categorias: Cisto E Nódulo, com as respectivas descrições e tamanhos, se disponíveis.
    * Nódulos e Cistos como Achados Distintos e Múltiplos: Se o relatório descrever um nódulo e um cisto como duas (ou mais) lesões separadas e distintas (não uma reclassificação de uma única lesão), ambos devem ser extraídos individualmente com status "Presente" e seus respectivos detalhes.
    * Detalhamento: Sempre descreva o tipo do cisto ou/e nódulo, caso presente no relatório.


3.  Múltiplos Achados do Mesmo Tipo:
    * Quando houver múltiplos cistos ou múltiplos nódulos, reporte TODOS, priorizando: a) Achados classificados como suspeitos pelo relatório, b) Achados de maior tamanho, c) Achados com características atípicas mencionadas. Liste suas localizações e tamanhos.

4.  Diferenciação entre Calcificações e Microcalcificações:
    * Calcificações: estruturas maiores, geralmente descritas como "grosseiras", "distróficas", "vasculares".
    * Microcalcificações: estruturas menores, frequentemente descritas como "puntiformes", "pleomórficas", "lineares", "agrupadas", "em cluster".
    * Se o relatório mencionar "microcalcificações" especificamente, classifique como microcalcificações. Se mencionar apenas "calcificações" (e a descrição não sugerir microcalcificações), classifique como calcificações.

Exemplos Selecionados:

Exemplo 1:
ENTRADA:
MAMOGRAFIA DIGITAL DR* BILATERAL

Indicação clínica: 69 anos. Rotina. Antecedente de neoplasia mamária.
Exame com MAMÓGRAFO DIGITAL nas incidências craniocaudal e mediolateral oblíqua acrescido de
incidências em ambas projeções obtidas com manobras de deslocamento posterior dos implantes mamários.
Status pós cirurgia conservadora da mama esquerda.
Parênquima mamário heterogeneamente denso, o que reduz a sensibilidade da mamografia.
Alterações arquiteturais, relacionadas à mamoplastia.
Nódulo denso de contornos espiculados projetado no QSE da mama esquerda, associado a retração cutânea,
com correspondência ao ultrassom, maior em relação ao exame de 01/2024. Prosseguir com core biopsy.
Cisto oleoso na mama esquerda.
Calcificações esparsas.
Ausência de microcalcificações pleomórficas agrupadas ou ramificadas. Implante bilateral, sem sinais de roturas extracapsulares. Linfonodo axilar, de aspecto reacional. ACR-BIRADS® categoria 5.
SAÍDA:
Cisto:
- Status: presente
- Localização: Imagem cística com conteúdo denso em RRA da mama esquerda; Cistos simples e de conteúdo denso esparsos bilateralmente.
- Tamanho: 2,0 cm (RRA mama esquerda); até 1,2 cm (bilateralmente)
Nódulo:
- Status: ausente
- Localização: [sem referência no texto]
- Tamanho: [sem referência no texto]
Calcificação:
- Status: presente
- Localização: bilaterais com características de benignidade
- Tamanho: [sem referência no texto]
Microcalcificação:
- Status: ausente
- Localização: [sem referência no texto]
- Tamanho: [sem referência no texto]
BI-RADS: 4
Outras citações a avaliar: Área hipoecogênica heterogênea, irregular, medindo cerca de 2,4 cm às 12h justareolar da mama direita, pode estar relacionado a ectasia ductal com discreta distorção arquitetural.

Exemplo 2:
ENTRADA:
MAMOGRAFIA DIGITAL (DR) ECOGRAFIA MAMÁRIA ECOGRAFIA DAS AXILAS Breve resumo Clínico: 66 anos. Assintomática A investigação realizada permite referir: Mamas heterogeneamente densas. Nódulo circunscrito, de média densidade, medindo cerca de 1,0cm de diâmetro, na junção dos quadrantes internos à esquerda, que ao ultrassom corresponde a cisto. Não há nódulos. Conclusão: Achados mamográficos e ecográficos benignos. BI-RADS 2.
SAÍDA:
Cisto:
- Status: presente
- Localização: junção dos quadrantes internos à esquerda
- Tamanho: medindo cerca de 1,0 cm de diâmetro
Nódulo:
- Status: ausente
- Localização: [sem referência no texto]
- Tamanho: [sem referência no texto]
Calcificação:
- Status: ausente
- Localização: [sem referência no texto]
- Tamanho: [sem referência no texto]
Microcalcificação:
- Status: ausente
- Localização: [sem referência no texto]
- Tamanho: [sem referência no texto]
BI-RADS: 2
Outras citações a avaliar: [sem referência no texto]

Exemplo 3:
ENTRADA:
MAMOGRAFIA DIGITAL BILATERAL indicação do exame: nódulo palpável na mama esquerda. Mamas heterogeneamente densas. Na mama esquerda observa-se nódulo denso e irregular, nos quadrantes superiores e laterais, associado a espessamento cutâneo, medindo aproximadamente 6,4cm. Não se observa linfonodos nos prolongamentos axilares. Não dispomos exames anteriores para comparação. Impressão diagnóstica Classificação BI-RADS categoria V (achados mamográficos altamente sugestivos de malignidade)
SAÍDA:
Cisto:
- Status: ausente
- Localização: [sem referência no texto]
- Tamanho: [sem referência no texto]
Nódulo:
- Status: presente
- Localização: Na mama esquerda, quadrantes superiores e laterais, associado a espessamento cutâneo.
- Tamanho: aproximadamente 6,4cm
Calcificação:
- Status: ausente
- Localização: [sem referência no texto]
- Tamanho: [sem referência no texto]
Microcalcificação:
- Status: ausente
- Localização: [sem referência no texto]
- Tamanho: [sem referência no texto]
BI-RADS: 5
Outras citações a avaliar: [sem referência no texto]

Exemplo 4 (Múltiplos achados distintos, Mamo+Eco, sem reclassificação do nódulo):
ENTRADA:
Mamografia demonstrou parênquima denso. Identificado nódulo irregular no QSM da mama direita, medindo 1,2 cm, suspeito (BI-RADS 4C). Ultrassonografia complementar confirmou o nódulo como sólido e também revelou um cisto simples de 0,8 cm no QIL da mesma mama. Linfonodos axilares sem alterações.
SAÍDA:
Cisto:
- Status: Presente
- Localização: QIL da mama direita
- Tamanho: 0,8 cm
Nódulo:
- Status: Presente
- Localização: QSM da mama direita
- Tamanho: 1,2 cm
Calcificação:
- Status: Ausente
- Localização: [sem referência no texto]
- Tamanho: [sem referência no texto]
Microcalcificação:
- Status: Ausente
- Localização: [sem referência no texto]
- Tamanho: [sem referência no texto]
BI-RADS: 4
Outras citações a avaliar: Parênquima denso. Nódulo suspeito. Ultrassonografia confirmou o nódulo sólido. Linfonodos axilares sem alterações.

IMPORTANTE: Retorne a resposta APENAS em formato JSON válido, seguindo exatamente esta estrutura:
{{
    "cisto": {{
        "presente": true/false,
        "detalhes": "localização e/ou tamanho"
    }},
    "nodulo": {{
        "presente": true/false,
        "detalhes": "localização e/ou tamanho"
    }},
    "calcificacao": {{
        "presente": true/false,
        "detalhes": "localização e/ou tamanho"
    }},
    "microcalcificacao": {{
        "presente": true/false,
        "detalhes": "localização e/ou tamanho"
    }},
    "bi_rads": "valor",
    "outras_citacoes": "observações adicionais relevantes"
}}

RELATÓRIO DO EXAME:
{exam_content}
"""

