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
    return f"""Você é um especialista em análise de relatórios de mamografia. Sua tarefa é ler o relatório fornecido e extrair as informações solicitadas. Siga ATENTAMENTE as "Diretrizes de Interpretação".

Diretrizes de Interpretação:

1.  Identificação Geral de Achados:
    * Para cada categoria principal (Cisto, Nódulo, Calcificação, Microcalcificação), determine o Status (Presente ou Ausente) e, se presente, extraia a Localização e o Tamanho.
    * Se informações específicas não estiverem disponíveis no texto, utilize "Ausente".

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
Parênquima mamário heterogeneamente denso, o que reduz a sensibilidade da mamografia.
Alterações arquiteturais, relacionadas à mamoplastia.
Nódulo denso de contornos espiculados projetado no QSE da mama esquerda, associado a retração cutânea, com correspondência ao ultrassom, maior em relação ao exame de 01/2024. Prosseguir com core biopsy.
Cisto oleoso na mama esquerda.
Calcificações esparsas.
Ausência de microcalcificações pleomórficas agrupadas ou ramificadas. Implante bilateral, sem sinais de roturas extracapsulares. Linfonodo axilar, de aspecto reacional. 
ACR-BIRADS® categoria 5.

SAÍDA (FHIR Bundle):
{{
  "resourceType": "Bundle",
  "type": "collection",
  "entry": [
    {{
      "fullUrl": "urn:uuid:a1f3c2d4-0001-4e8b-b301-aabbcc110001",
      "resource": {{
        "resourceType": "DiagnosticReport",
        "text": {{
          "status": "generated",
          "div": "<div xmlns=\"http://www.w3.org/1999/xhtml\">Laudo mamográfico: BI-RADS 5. Cisto oleoso na mama esquerda. Nódulo denso espiculado no QSE da mama esquerda. Calcificações esparsas. Ausência de microcalcificações.</div>"
        }},
        "status": "final",
        "category": [{{"coding": [{{"system": "http://terminology.hl7.org/CodeSystem/v2-0074", "code": "RAD", "display": "Radiology"}}]}}],
        "code": {{"coding": [{{"system": "http://loinc.org", "code": "24606-6", "display": "MG Breast Screening"}}]}},
        "subject": {{"display": "Paciente não identificada"}},
        "_effectiveDateTime": {{"extension": [{{"url": "http://hl7.org/fhir/StructureDefinition/data-absent-reason", "valueCode": "unknown"}}]}},
        "result": [
          {{"reference": "urn:uuid:a1f3c2d4-0001-4e8b-b301-aabbcc110002", "display": "Cisto"}},
          {{"reference": "urn:uuid:a1f3c2d4-0001-4e8b-b301-aabbcc110003", "display": "Nódulo"}},
          {{"reference": "urn:uuid:a1f3c2d4-0001-4e8b-b301-aabbcc110004", "display": "Calcificação"}},
          {{"reference": "urn:uuid:a1f3c2d4-0001-4e8b-b301-aabbcc110005", "display": "Microcalcificação"}}
        ],
        "conclusion": "Parênquima mamário heterogeneamente denso. Nódulo denso de contornos espiculados no QSE da mama esquerda, associado a retração cutânea. Cisto oleoso na mama esquerda. Calcificações esparsas. Achados altamente sugestivos de malignidade.",
        "conclusionCode": [{{"coding": [{{"system": "http://snomed.info/sct", "code": "397145000", "display": "Mammography assessment (Category 5) - Highly suggestive of malignancy (finding)"}}], "text": "BI-RADS 5"}}]
      }}
    }},
    {{
      "fullUrl": "urn:uuid:a1f3c2d4-0001-4e8b-b301-aabbcc110002",
      "resource": {{
        "resourceType": "Observation",
        "text": {{"status": "generated", "div": "<div xmlns=\"http://www.w3.org/1999/xhtml\">Cisto presente: cisto oleoso na mama esquerda.</div>"}},
        "status": "final",
        "code": {{"coding": [{{"system": "http://snomed.info/sct", "code": "399294002", "display": "Cyst of breast"}}], "text": "Cisto"}},
        "subject": {{"display": "Paciente não identificada"}},
        "_effectiveDateTime": {{"extension": [{{"url": "http://hl7.org/fhir/StructureDefinition/data-absent-reason", "valueCode": "unknown"}}]}},
        "performer": [{{"display": "Médico Responsável"}}],
        "valueBoolean": true,
        "note": [{{"text": "Cisto oleoso na mama esquerda"}}]
      }}
    }},
    {{
      "fullUrl": "urn:uuid:a1f3c2d4-0001-4e8b-b301-aabbcc110003",
      "resource": {{
        "resourceType": "Observation",
        "text": {{"status": "generated", "div": "<div xmlns=\"http://www.w3.org/1999/xhtml\">Nódulo presente: nódulo denso de contornos espiculados no QSE da mama esquerda, com retração cutânea.</div>"}},
        "status": "final",
        "code": {{"coding": [{{"system": "http://snomed.info/sct", "code": "89164003", "display": "Breast lump"}}], "text": "Nódulo"}},
        "subject": {{"display": "Paciente não identificada"}},
        "_effectiveDateTime": {{"extension": [{{"url": "http://hl7.org/fhir/StructureDefinition/data-absent-reason", "valueCode": "unknown"}}]}},
        "performer": [{{"display": "Médico Responsável"}}],
        "valueBoolean": true,
        "note": [{{"text": "Nódulo denso de contornos espiculados no QSE da mama esquerda, associado a retração cutânea"}}]
      }}
    }},
    {{
      "fullUrl": "urn:uuid:a1f3c2d4-0001-4e8b-b301-aabbcc110004",
      "resource": {{
        "resourceType": "Observation",
        "text": {{"status": "generated", "div": "<div xmlns=\"http://www.w3.org/1999/xhtml\">Calcificação presente: esparsas.</div>"}},
        "status": "final",
        "code": {{"coding": [{{"system": "http://snomed.info/sct", "code": "309587003", "display": "Calcification of breast"}}], "text": "Calcificação"}},
        "subject": {{"display": "Paciente não identificada"}},
        "_effectiveDateTime": {{"extension": [{{"url": "http://hl7.org/fhir/StructureDefinition/data-absent-reason", "valueCode": "unknown"}}]}},
        "performer": [{{"display": "Médico Responsável"}}],
        "valueBoolean": true,
        "note": [{{"text": "Calcificações esparsas"}}]
      }}
    }},
    {{
      "fullUrl": "urn:uuid:a1f3c2d4-0001-4e8b-b301-aabbcc110005",
      "resource": {{
        "resourceType": "Observation",
        "text": {{"status": "generated", "div": "<div xmlns=\"http://www.w3.org/1999/xhtml\">Microcalcificação: ausente.</div>"}},
        "status": "final",
        "code": {{"coding": [{{"system": "http://snomed.info/sct", "code": "44771000", "display": "Microcalcifications of the breast"}}], "text": "Microcalcificação"}},
        "subject": {{"display": "Paciente não identificada"}},
        "_effectiveDateTime": {{"extension": [{{"url": "http://hl7.org/fhir/StructureDefinition/data-absent-reason", "valueCode": "unknown"}}]}},
        "performer": [{{"display": "Médico Responsável"}}],
        "valueBoolean": false
      }}
    }}
  ]
}}

Exemplo 2:
ENTRADA:
MAMOGRAFIA DIGITAL (DR) ECOGRAFIA MAMÁRIA ECOGRAFIA DAS AXILAS
Breve resumo Clínico: 66 anos. Assintomática.
A investigação realizada permite referir: Mamas heterogeneamente densas.
Nódulo circunscrito, de média densidade, medindo cerca de 1,0cm de diâmetro, na junção dos quadrantes internos à esquerda, que ao ultrassom corresponde a cisto.
Não há nódulos.
Conclusão: Achados mamográficos e ecográficos benignos. BI-RADS 2.

SAÍDA (FHIR Bundle):
{{
  "resourceType": "Bundle",
  "type": "collection",
  "entry": [
    {{
      "fullUrl": "urn:uuid:1a2b3c4d-0002-4000-8000-aabbcc220001",
      "resource": {{
        "resourceType": "DiagnosticReport",
        "text": {{
          "status": "generated",
          "div": "<div xmlns=\"http://www.w3.org/1999/xhtml\">Laudo mamográfico: BI-RADS 2. Cisto na junção dos quadrantes internos à esquerda (~1,0cm). Mamas heterogeneamente densas. Achados benignos.</div>"
        }},
        "status": "final",
        "category": [{{"coding": [{{"system": "http://terminology.hl7.org/CodeSystem/v2-0074", "code": "RAD", "display": "Radiology"}}]}}],
        "code": {{"coding": [{{"system": "http://loinc.org", "code": "24606-6", "display": "MG Breast Screening"}}]}},
        "subject": {{"display": "Paciente não identificada"}},
        "_effectiveDateTime": {{"extension": [{{"url": "http://hl7.org/fhir/StructureDefinition/data-absent-reason", "valueCode": "unknown"}}]}},
        "result": [
          {{"reference": "urn:uuid:1a2b3c4d-0002-4000-8000-aabbcc220002", "display": "Cisto"}},
          {{"reference": "urn:uuid:1a2b3c4d-0002-4000-8000-aabbcc220003", "display": "Nódulo"}},
          {{"reference": "urn:uuid:1a2b3c4d-0002-4000-8000-aabbcc220004", "display": "Calcificação"}},
          {{"reference": "urn:uuid:1a2b3c4d-0002-4000-8000-aabbcc220005", "display": "Microcalcificação"}}
        ],
        "conclusion": "Mamas heterogeneamente densas. Achados mamográficos e ecográficos benignos.",
        "conclusionCode": [{{"coding": [{{"system": "http://snomed.info/sct", "code": "397141009", "display": "Mammography assessment (Category 2) - Benign finding (finding)"}}], "text": "BI-RADS 2"}}]
      }}
    }},
    {{
      "fullUrl": "urn:uuid:1a2b3c4d-0002-4000-8000-aabbcc220002",
      "resource": {{
        "resourceType": "Observation",
        "text": {{"status": "generated", "div": "<div xmlns=\"http://www.w3.org/1999/xhtml\">Cisto presente: junção dos quadrantes internos à esquerda, ~1,0cm.</div>"}},
        "status": "final",
        "code": {{"coding": [{{"system": "http://snomed.info/sct", "code": "399294002", "display": "Cyst of breast"}}], "text": "Cisto"}},
        "subject": {{"display": "Paciente não identificada"}},
        "_effectiveDateTime": {{"extension": [{{"url": "http://hl7.org/fhir/StructureDefinition/data-absent-reason", "valueCode": "unknown"}}]}},
        "performer": [{{"display": "Médico Responsável"}}],
        "valueBoolean": true,
        "note": [{{"text": "Junção dos quadrantes internos à esquerda, medindo cerca de 1,0cm de diâmetro"}}]
      }}
    }},
    {{
      "fullUrl": "urn:uuid:1a2b3c4d-0002-4000-8000-aabbcc220003",
      "resource": {{
        "resourceType": "Observation",
        "text": {{"status": "generated", "div": "<div xmlns=\"http://www.w3.org/1999/xhtml\">Nódulo: ausente.</div>"}},
        "status": "final",
        "code": {{"coding": [{{"system": "http://snomed.info/sct", "code": "89164003", "display": "Breast lump"}}], "text": "Nódulo"}},
        "subject": {{"display": "Paciente não identificada"}},
        "_effectiveDateTime": {{"extension": [{{"url": "http://hl7.org/fhir/StructureDefinition/data-absent-reason", "valueCode": "unknown"}}]}},
        "performer": [{{"display": "Médico Responsável"}}],
        "valueBoolean": false
      }}
    }},
    {{
      "fullUrl": "urn:uuid:1a2b3c4d-0002-4000-8000-aabbcc220004",
      "resource": {{
        "resourceType": "Observation",
        "text": {{"status": "generated", "div": "<div xmlns=\"http://www.w3.org/1999/xhtml\">Calcificação: ausente.</div>"}},
        "status": "final",
        "code": {{"coding": [{{"system": "http://snomed.info/sct", "code": "309587003", "display": "Calcification of breast"}}], "text": "Calcificação"}},
        "subject": {{"display": "Paciente não identificada"}},
        "_effectiveDateTime": {{"extension": [{{"url": "http://hl7.org/fhir/StructureDefinition/data-absent-reason", "valueCode": "unknown"}}]}},
        "performer": [{{"display": "Médico Responsável"}}],
        "valueBoolean": false
      }}
    }},
    {{
      "fullUrl": "urn:uuid:1a2b3c4d-0002-4000-8000-aabbcc220005",
      "resource": {{
        "resourceType": "Observation",
        "text": {{"status": "generated", "div": "<div xmlns=\"http://www.w3.org/1999/xhtml\">Microcalcificação: ausente.</div>"}},
        "status": "final",
        "code": {{"coding": [{{"system": "http://snomed.info/sct", "code": "44771000", "display": "Microcalcifications of the breast"}}], "text": "Microcalcificação"}},
        "subject": {{"display": "Paciente não identificada"}},
        "_effectiveDateTime": {{"extension": [{{"url": "http://hl7.org/fhir/StructureDefinition/data-absent-reason", "valueCode": "unknown"}}]}},
        "performer": [{{"display": "Médico Responsável"}}],
        "valueBoolean": false
      }}
    }}
  ]
}}

Exemplo 3:
ENTRADA:
MAMOGRAFIA DIGITAL BILATERAL
Indicação do exame: nódulo palpável na mama esquerda.
Mamas heterogeneamente densas. Na mama esquerda observa-se nódulo denso e irregular, nos quadrantes superiores e laterais, associado a espessamento cutâneo, medindo aproximadamente 6,4cm.
Não se observa linfonodos nos prolongamentos axilares. Não dispomos exames anteriores para comparação.
Impressão diagnóstica: Classificação BI-RADS categoria V (achados mamográficos altamente sugestivos de malignidade)

SAÍDA (FHIR Bundle):
{{
  "resourceType": "Bundle",
  "type": "collection",
  "entry": [
    {{
      "fullUrl": "urn:uuid:a1f3c2d4-0011-4e8b-b301-aabbcc330001",
      "resource": {{
        "resourceType": "DiagnosticReport",
        "text": {{
          "status": "generated",
          "div": "<div xmlns=\"http://www.w3.org/1999/xhtml\">Laudo mamográfico: BI-RADS 5. Nódulo denso e irregular nos quadrantes superiores e laterais da mama esquerda (~6,4cm), com espessamento cutâneo. Mamas heterogeneamente densas. Achados altamente sugestivos de malignidade.</div>"
        }},
        "status": "final",
        "category": [{{"coding": [{{"system": "http://terminology.hl7.org/CodeSystem/v2-0074", "code": "RAD", "display": "Radiology"}}]}}],
        "code": {{"coding": [{{"system": "http://loinc.org", "code": "24606-6", "display": "MG Breast Screening"}}]}},
        "subject": {{"display": "Paciente não identificada"}},
        "_effectiveDateTime": {{"extension": [{{"url": "http://hl7.org/fhir/StructureDefinition/data-absent-reason", "valueCode": "unknown"}}]}},
        "result": [
          {{"reference": "urn:uuid:a1f3c2d4-0011-4e8b-b301-aabbcc330002", "display": "Cisto"}},
          {{"reference": "urn:uuid:a1f3c2d4-0011-4e8b-b301-aabbcc330003", "display": "Nódulo"}},
          {{"reference": "urn:uuid:a1f3c2d4-0011-4e8b-b301-aabbcc330004", "display": "Calcificação"}},
          {{"reference": "urn:uuid:a1f3c2d4-0011-4e8b-b301-aabbcc330005", "display": "Microcalcificação"}}
        ],
        "conclusion": "Nódulo denso e irregular nos quadrantes superiores e laterais da mama esquerda, associado a espessamento cutâneo, medindo aproximadamente 6,4cm. Achados mamográficos altamente sugestivos de malignidade.",
        "conclusionCode": [{{"coding": [{{"system": "http://snomed.info/sct", "code": "397145000", "display": "Mammography assessment (Category 5) - Highly suggestive of malignancy (finding)"}}], "text": "BI-RADS 5"}}]
      }}
    }},
    {{
      "fullUrl": "urn:uuid:a1f3c2d4-0011-4e8b-b301-aabbcc330002",
      "resource": {{
        "resourceType": "Observation",
        "text": {{"status": "generated", "div": "<div xmlns=\"http://www.w3.org/1999/xhtml\">Cisto: ausente.</div>"}},
        "status": "final",
        "code": {{"coding": [{{"system": "http://snomed.info/sct", "code": "399294002", "display": "Cyst of breast"}}], "text": "Cisto"}},
        "subject": {{"display": "Paciente não identificada"}},
        "_effectiveDateTime": {{"extension": [{{"url": "http://hl7.org/fhir/StructureDefinition/data-absent-reason", "valueCode": "unknown"}}]}},
        "performer": [{{"display": "Médico Responsável"}}],
        "valueBoolean": false
      }}
    }},
    {{
      "fullUrl": "urn:uuid:a1f3c2d4-0011-4e8b-b301-aabbcc330003",
      "resource": {{
        "resourceType": "Observation",
        "text": {{"status": "generated", "div": "<div xmlns=\"http://www.w3.org/1999/xhtml\">Nódulo presente: nódulo denso e irregular nos quadrantes superiores e laterais da mama esquerda, ~6,4cm, com espessamento cutâneo.</div>"}},
        "status": "final",
        "code": {{"coding": [{{"system": "http://snomed.info/sct", "code": "89164003", "display": "Breast lump"}}], "text": "Nódulo"}},
        "subject": {{"display": "Paciente não identificada"}},
        "_effectiveDateTime": {{"extension": [{{"url": "http://hl7.org/fhir/StructureDefinition/data-absent-reason", "valueCode": "unknown"}}]}},
        "performer": [{{"display": "Médico Responsável"}}],
        "valueBoolean": true,
        "note": [{{"text": "Nódulo denso e irregular, nos quadrantes superiores e laterais da mama esquerda, associado a espessamento cutâneo, medindo aproximadamente 6,4cm"}}]
      }}
    }},
    {{
      "fullUrl": "urn:uuid:a1f3c2d4-0011-4e8b-b301-aabbcc330004",
      "resource": {{
        "resourceType": "Observation",
        "text": {{"status": "generated", "div": "<div xmlns=\"http://www.w3.org/1999/xhtml\">Calcificação: ausente.</div>"}},
        "status": "final",
        "code": {{"coding": [{{"system": "http://snomed.info/sct", "code": "309587003", "display": "Calcification of breast"}}], "text": "Calcificação"}},
        "subject": {{"display": "Paciente não identificada"}},
        "_effectiveDateTime": {{"extension": [{{"url": "http://hl7.org/fhir/StructureDefinition/data-absent-reason", "valueCode": "unknown"}}]}},
        "performer": [{{"display": "Médico Responsável"}}],
        "valueBoolean": false
      }}
    }},
    {{
      "fullUrl": "urn:uuid:a1f3c2d4-0011-4e8b-b301-aabbcc330005",
      "resource": {{
        "resourceType": "Observation",
        "text": {{"status": "generated", "div": "<div xmlns=\"http://www.w3.org/1999/xhtml\">Microcalcificação: ausente.</div>"}},
        "status": "final",
        "code": {{"coding": [{{"system": "http://snomed.info/sct", "code": "44771000", "display": "Microcalcifications of the breast"}}], "text": "Microcalcificação"}},
        "subject": {{"display": "Paciente não identificada"}},
        "_effectiveDateTime": {{"extension": [{{"url": "http://hl7.org/fhir/StructureDefinition/data-absent-reason", "valueCode": "unknown"}}]}},
        "performer": [{{"display": "Médico Responsável"}}],
        "valueBoolean": false
      }}
    }}
  ]
}}

Exemplo 4 (Múltiplos achados distintos, Mamo+Eco, sem reclassificação do nódulo):
ENTRADA:
Mamografia demonstrou parênquima denso.
Identificado nódulo irregular no QSM da mama direita, medindo 1,2 cm, suspeito (BI-RADS 4C).
Ultrassonografia complementar confirmou o nódulo como sólido e também revelou um cisto simples de 0,8 cm no QIL da mesma mama.
Linfonodos axilares sem alterações.

SAÍDA (FHIR Bundle):
{{
  "resourceType": "Bundle",
  "type": "collection",
  "entry": [
    {{
      "fullUrl": "urn:uuid:b7e9a1f2-0022-4c7d-a412-aabbcc440001",
      "resource": {{
        "resourceType": "DiagnosticReport",
        "text": {{
          "status": "generated",
          "div": "<div xmlns=\"http://www.w3.org/1999/xhtml\">Laudo mamográfico/ecográfico: BI-RADS 4C. Nódulo irregular sólido no QSM da mama direita (1,2cm). Cisto simples no QIL da mama direita (0,8cm). Parênquima denso. Achado suspeito.</div>"
        }},
        "status": "final",
        "category": [{{"coding": [{{"system": "http://terminology.hl7.org/CodeSystem/v2-0074", "code": "RAD", "display": "Radiology"}}]}}],
        "code": {{"coding": [{{"system": "http://loinc.org", "code": "24606-6", "display": "MG Breast Screening"}}]}},
        "subject": {{"display": "Paciente não identificada"}},
        "_effectiveDateTime": {{"extension": [{{"url": "http://hl7.org/fhir/StructureDefinition/data-absent-reason", "valueCode": "unknown"}}]}},
        "result": [
          {{"reference": "urn:uuid:b7e9a1f2-0022-4c7d-a412-aabbcc440002", "display": "Cisto"}},
          {{"reference": "urn:uuid:b7e9a1f2-0022-4c7d-a412-aabbcc440003", "display": "Nódulo"}},
          {{"reference": "urn:uuid:b7e9a1f2-0022-4c7d-a412-aabbcc440004", "display": "Calcificação"}},
          {{"reference": "urn:uuid:b7e9a1f2-0022-4c7d-a412-aabbcc440005", "display": "Microcalcificação"}}
        ],
        "conclusion": "Parênquima denso. Nódulo irregular no QSM da mama direita, medindo 1,2cm, confirmado como sólido ao ultrassom (suspeito). Cisto simples de 0,8cm no QIL da mama direita identificado ao ultrassom. Linfonodos axilares sem alterações.",
        "conclusionCode": [{{"coding": [{{"system": "http://snomed.info/sct", "code": "397143007", "display": "Mammography assessment (Category 4) - Suspicious abnormality (finding)"}}], "text": "BI-RADS 4C"}}]
      }}
    }},
    {{
      "fullUrl": "urn:uuid:b7e9a1f2-0022-4c7d-a412-aabbcc440002",
      "resource": {{
        "resourceType": "Observation",
        "text": {{"status": "generated", "div": "<div xmlns=\"http://www.w3.org/1999/xhtml\">Cisto presente: cisto simples no QIL da mama direita, 0,8cm.</div>"}},
        "status": "final",
        "code": {{"coding": [{{"system": "http://snomed.info/sct", "code": "399294002", "display": "Cyst of breast"}}], "text": "Cisto"}},
        "subject": {{"display": "Paciente não identificada"}},
        "_effectiveDateTime": {{"extension": [{{"url": "http://hl7.org/fhir/StructureDefinition/data-absent-reason", "valueCode": "unknown"}}]}},
        "performer": [{{"display": "Médico Responsável"}}],
        "valueBoolean": true,
        "note": [{{"text": "Cisto simples de 0,8cm no QIL da mama direita, identificado à ultrassonografia"}}]
      }}
    }},
    {{
      "fullUrl": "urn:uuid:b7e9a1f2-0022-4c7d-a412-aabbcc440003",
      "resource": {{
        "resourceType": "Observation",
        "text": {{"status": "generated", "div": "<div xmlns=\"http://www.w3.org/1999/xhtml\">Nódulo presente: nódulo irregular sólido no QSM da mama direita, 1,2cm, suspeito (BI-RADS 4C).</div>"}},
        "status": "final",
        "code": {{"coding": [{{"system": "http://snomed.info/sct", "code": "89164003", "display": "Breast lump"}}], "text": "Nódulo"}},
        "subject": {{"display": "Paciente não identificada"}},
        "_effectiveDateTime": {{"extension": [{{"url": "http://hl7.org/fhir/StructureDefinition/data-absent-reason", "valueCode": "unknown"}}]}},
        "performer": [{{"display": "Médico Responsável"}}],
        "valueBoolean": true,
        "note": [{{"text": "Nódulo irregular no QSM da mama direita, medindo 1,2cm, confirmado como sólido à ultrassonografia, suspeito (BI-RADS 4C)"}}]
      }}
    }},
    {{
      "fullUrl": "urn:uuid:b7e9a1f2-0022-4c7d-a412-aabbcc440004",
      "resource": {{
        "resourceType": "Observation",
        "text": {{"status": "generated", "div": "<div xmlns=\"http://www.w3.org/1999/xhtml\">Calcificação: ausente.</div>"}},
        "status": "final",
        "code": {{"coding": [{{"system": "http://snomed.info/sct", "code": "309587003", "display": "Calcification of breast"}}], "text": "Calcificação"}},
        "subject": {{"display": "Paciente não identificada"}},
        "_effectiveDateTime": {{"extension": [{{"url": "http://hl7.org/fhir/StructureDefinition/data-absent-reason", "valueCode": "unknown"}}]}},
        "performer": [{{"display": "Médico Responsável"}}],
        "valueBoolean": false
      }}
    }},
    {{
      "fullUrl": "urn:uuid:b7e9a1f2-0022-4c7d-a412-aabbcc440005",
      "resource": {{
        "resourceType": "Observation",
        "text": {{"status": "generated", "div": "<div xmlns=\"http://www.w3.org/1999/xhtml\">Microcalcificação: ausente.</div>"}},
        "status": "final",
        "code": {{"coding": [{{"system": "http://snomed.info/sct", "code": "44771000", "display": "Microcalcifications of the breast"}}], "text": "Microcalcificação"}},
        "subject": {{"display": "Paciente não identificada"}},
        "_effectiveDateTime": {{"extension": [{{"url": "http://hl7.org/fhir/StructureDefinition/data-absent-reason", "valueCode": "unknown"}}]}},
        "performer": [{{"display": "Médico Responsável"}}],
        "valueBoolean": false
      }}
    }}
  ]
}}

IMPORTANTE: Retorne a resposta APENAS em JSON válido no formato FHIR Bundle acima, sem nenhum texto adicional.

Regras de preenchimento:
- Gere UUIDs v4 únicos e válidos para cada entrada (formato: xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx).
- Se o relatório informar a data do exame, use "effectiveDateTime": "YYYY-MM-DD".
- Se a data NÃO estiver disponível, use "_effectiveDateTime" com a extensão data-absent-reason, exatamente como nos exemplos acima.
- No DiagnosticReport, preencha "conclusion" com o texto conclusivo do laudo.
- Para "conclusionCode", use o sistema "http://snomed.info/sct" e os códigos conforme o BI-RADS:
  - BI-RADS 0: "397139009" / "Mammography assessment (Category 0)"
  - BI-RADS 1: "397140006" / "Mammography assessment (Category 1) - Negative (finding)"
  - BI-RADS 2: "397141009" / "Mammography assessment (Category 2) - Benign finding (finding)"
  - BI-RADS 3: "397142002" / "Mammography assessment (Category 3) - Probably benign finding (finding)"
  - BI-RADS 4: "397143007" / "Mammography assessment (Category 4) - Suspicious abnormality (finding)"
  - BI-RADS 5: "397145000" / "Mammography assessment (Category 5) - Highly suggestive of malignancy (finding)"
  - BI-RADS 6: "397146004" / "Mammography assessment (Category 6) - Known biopsy proven malignancy (finding)"
- Nos Observation com valueBoolean true, preencha "note[0].text" com localização e/ou tamanho.
- Nos Observation com valueBoolean false, omita o campo "note".

RELATÓRIO DO EXAME:
{exam_content}
"""

