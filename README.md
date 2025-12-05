# Academic Course Scheduling Optimization

Sistema de otimização de agendamento de cursos acadêmicos usando Weighted Interval Scheduling.

## Limitações do Projeto

Este projeto foi desenvolvido com as seguintes limitações:
- **Um aluno apenas**: O planejamento é feito considerando a grade de apenas um estudante
- **Um semestre apenas**: O sistema planeja cursos para um único semestre acadêmico

## Descrição

Este repositório implementa dois algoritmos para resolver o problema de agendamento ponderado de intervalos no contexto de cursos acadêmicos:

1. **Branch and Bound**: Algoritmo de busca sistemática que explora o espaço de soluções com podas inteligentes. Três variantes são implementadas:
   - **FO1**: Ordena por créditos (maior primeiro) e explora sistematicamente - foco em maximizar créditos
   - **FO2**: Ordena por horário de término e minimiza gaps - foco em minimizar intervalos
   - **FO3**: Ordena pela razão `end_time/credits` - abordagem balanceada

2. **Programação Linear Inteira (ILP)**: Solução exata que garante resultado ótimo. Três funções objetivo são implementadas:
   - **FO1**: `maximize(créditos)` - maximiza apenas créditos
   - **FO2**: `minimize(gaps)` - minimiza apenas intervalos ociosos
   - **FO3**: `maximize(créditos - penalidade × gaps)` - balanceia ambos objetivos

## Funções Objetivo

O sistema implementa **3 funções objetivo diferentes**, permitindo comparar como diferentes objetivos de otimização geram resultados diferentes:

### FO1: Maximizar Créditos
- **Objetivo**: Maximizar o total de créditos cursados
- **Trade-off**: Pode resultar em maiores intervalos entre aulas
- **Uso**: Ideal para estudantes que querem completar o máximo de créditos possível

### FO2: Minimizar Intervalos (Gaps)
- **Objetivo**: Minimizar o tempo ocioso entre aulas
- **Trade-off**: Pode resultar em menos créditos totais
- **Uso**: Ideal para estudantes que preferem ter um horário mais compacto

### FO3: Combinada (Balanceada)
- **Objetivo**: Balancear créditos e gaps
- **Fórmula**: `maximize(créditos - penalidade × gaps)`
- **Trade-off**: Solução intermediária que considera ambos aspectos
- **Uso**: Ideal para a maioria dos casos, oferecendo um equilíbrio

## Características

- ✅ Modelo de curso com horários, créditos e pré-requisitos
- ✅ Verificador de conflitos de horário
- ✅ Calculadora de intervalos ociosos (gaps)
- ✅ Algoritmo guloso eficiente
- ✅ Algoritmo ILP para solução ótima
- ✅ Script de comparação entre algoritmos
- ✅ Dados de exemplo realistas
- ✅ Testes abrangentes
- ✅ Type hints completos
- ✅ Docstrings em português

## Instalação

```bash
# Clone o repositório
git clone https://github.com/beatriz-fulgencio/optimization.git
cd optimization

# Instale as dependências
pip install -r requirements.txt
```

## Uso

### Executar Comparação dos Algoritmos e Funções Objetivo

Execute o script principal para comparar ambos os algoritmos com as 3 funções objetivo:

```bash
python -m src.compare
```

Ou especifique um arquivo JSON personalizado:

```bash
python -m src.compare data/meus_cursos.json
```

Este comando irá:
- Executar os algoritmos Guloso e ILP
- Testar as 3 funções objetivo (FO1, FO2, FO3)
- Comparar desempenho (tempo de execução)
- Comparar resultados (créditos e gaps)
- Mostrar que funções objetivo diferentes geram resultados diferentes

### Usar no Código Python

```python
from src.course import Course
from src.branch_and_bound_algorithm import (
    branch_and_bound_schedule_max_credits,  # FO1: Max créditos
    branch_and_bound_schedule_min_gaps,      # FO2: Min gaps
    branch_and_bound_schedule                # FO3: Combinada
)
from src.ilp_algorithm import (
    ilp_schedule_max_credits,      # FO1: Max créditos
    ilp_schedule_min_gaps,         # FO2: Min gaps
    ilp_schedule                   # FO3: Combinada
)

# Criar cursos
courses = [
    Course("MAT101", "Cálculo I", 8.0, 10.0, 4),
    Course("FIS101", "Física I", 10.0, 12.0, 4),
    Course("PROG101", "Programação", 14.0, 16.0, 4),
]

# FO1: Maximizar créditos
selected, credits, gap = branch_and_bound_schedule_max_credits(courses)
print(f"FO1 - Branch&Bound: {credits} créditos, {gap:.1f}h de gap")

selected, credits, gap = ilp_schedule_max_credits(courses)
print(f"FO1 - ILP: {credits} créditos, {gap:.1f}h de gap")

# FO2: Minimizar gaps
selected, credits, gap = branch_and_bound_schedule_min_gaps(courses)
print(f"FO2 - Branch&Bound: {credits} créditos, {gap:.1f}h de gap")

selected, credits, gap = ilp_schedule_min_gaps(courses)
print(f"FO2 - ILP: {credits} créditos, {gap:.1f}h de gap")

# FO3: Combinada
selected, credits, gap = branch_and_bound_schedule(courses)
print(f"FO3 - Branch&Bound: {credits} créditos, {gap:.1f}h de gap")

selected, credits, gap = ilp_schedule(courses, gap_penalty=0.1)
print(f"FO3 - ILP: {credits} créditos, {gap:.1f}h de gap")
```

### Formato do JSON de Dados

```json
{
  "courses": [
    {
      "id": "MAT101",
      "name": "Cálculo I",
      "start_time": 8.0,
      "end_time": 10.0,
      "credits": 4,
      "prerequisites": []
    },
    {
      "id": "MAT102",
      "name": "Cálculo II",
      "start_time": 10.0,
      "end_time": 12.0,
      "credits": 4,
      "prerequisites": ["MAT101"]
    }
  ]
}
```

## Executar Testes

```bash
# Executar todos os testes
pytest

# Executar com cobertura
pytest --cov=src

# Executar testes específicos
pytest tests/test_course.py
pytest tests/test_greedy_algorithm.py
pytest tests/test_ilp_algorithm.py
```

## Estrutura do Projeto

```
optimization/
├── src/
│   ├── __init__.py
│   ├── course.py              # Modelo de curso
│   ├── utils.py               # Utilitários (conflitos, gaps)
│   ├── greedy_algorithm.py    # Algoritmo guloso
│   ├── ilp_algorithm.py       # Algoritmo ILP
│   └── compare.py             # Script de comparação
├── tests/
│   ├── test_course.py
│   ├── test_utils.py
│   ├── test_greedy_algorithm.py
│   ├── test_ilp_algorithm.py
│   └── test_integration.py
├── data/
│   └── sample_courses.json    # Dados de exemplo
├── requirements.txt
└── README.md
```

## Algoritmos

### Branch and Bound

- **Complexidade**: Exponencial no pior caso, mas com podas eficientes
- **Vantagem**: Explora sistematicamente o espaço de soluções, garante solução ótima
- **Técnica**: Usa limites superiores (upper bounds) para podar ramos que não podem levar a soluções melhores
- **Limitação**: Pode ser lento para problemas muito grandes

**Três variantes implementadas:**
1. **FO1 (Max Créditos)**: Ordena por `-credits, end_time` e poda baseado em créditos remanescentes
2. **FO2 (Min Gaps)**: Ordena por `end_time` e poda baseado em gaps acumulados
3. **FO3 (Combinada)**: Ordena por `end_time/credits` e poda baseado em objetivo combinado

### Algoritmo ILP

- **Complexidade**: Exponencial no pior caso (NP-difícil)
- **Vantagem**: Garante solução ótima usando solvers especializados
- **Técnica**: Formula o problema como otimização linear inteira
- **Limitação**: Pode ser lento para problemas muito grandes

**Três funções objetivo implementadas:**
1. **FO1**: `maximize Σ(créditos × x[i])`
2. **FO2**: `minimize Σ(gap[i,j] × y[i,j])`
3. **FO3**: `maximize Σ(créditos × x[i]) - penalidade × Σ(gap[i,j] × y[i,j])`

## Comparação de Funções Objetivo

O projeto demonstra que **funções objetivo diferentes geram resultados diferentes**:

- **FO1** tende a selecionar mais cursos com mais créditos, mesmo com gaps maiores
- **FO2** tende a selecionar cursos mais próximos no tempo, mesmo com menos créditos
- **FO3** encontra um equilíbrio entre as duas métricas

## Métricas de Comparação

O sistema compara os algoritmos em três dimensões:

1. **Desempenho**: Tempo de execução de cada algoritmo
   - Branch and Bound: Geralmente < 0.01 segundos para instâncias pequenas
   - ILP: Pode variar de 0.1 a vários segundos

2. **Resultado**: Qualidade da solução
   - Créditos totais obtidos
   - Gap total (horas ociosas)
   
3. **Otimalidade**: 
   - Ambos algoritmos garantem solução ótima
   - Branch and Bound: Busca sistemática com poda
   - ILP: Formulação como problema de otimização linear inteira

## Restrições

- **Conflitos de Horário**: Cursos não podem se sobrepor
- **Pré-requisitos**: Só podem ser cursados se os pré-requisitos foram concluídos

## Exemplos de Saída

```
====================================================================================================
COMPARAÇÃO DE ALGORITMOS DE AGENDAMENTO DE CURSOS
Trabalho Final - Otimização
====================================================================================================

LIMITAÇÕES DO PROJETO:
  • Planejamento de grade para UM ALUNO apenas
  • Planejamento de UM SEMESTRE apenas

====================================================================================================

████████████████████████████████████████████████████████████████████████████████████████████████████
FUNÇÃO OBJETIVO 1: MAXIMIZAR CRÉDITOS
████████████████████████████████████████████████████████████████████████████████████████████████████

Executando GULOSO (FO1: Max Créditos)...
✓ Concluído em 0.0023 segundos

Executando ILP (FO1: Max Créditos)...
✓ Concluído em 0.1245 segundos

████████████████████████████████████████████████████████████████████████████████████████████████████
FUNÇÃO OBJETIVO 2: MINIMIZAR INTERVALOS (GAPS)
████████████████████████████████████████████████████████████████████████████████████████████████████

Executando GULOSO (FO2: Min Gaps)...
✓ Concluído em 0.0021 segundos

Executando ILP (FO2: Min Gaps)...
✓ Concluído em 0.1156 segundos

████████████████████████████████████████████████████████████████████████████████████████████████████
FUNÇÃO OBJETIVO 3: COMBINADA (Créditos - Penalidade × Gaps)
████████████████████████████████████████████████████████████████████████████████████████████████████

Executando GULOSO (FO3: Combinada)...
✓ Concluído em 0.0022 segundos

Executando ILP (FO3: Combinada)...
✓ Concluído em 0.1289 segundos

====================================================================================================
TABELA COMPARATIVA - RESULTADOS DAS 3 FUNÇÕES OBJETIVO
====================================================================================================

Função Objetivo                Algoritmo    Cursos   Créditos   Gap (h)    Tempo (s)   
----------------------------------------------------------------------------------------------------
FO1: Max Créditos              Guloso       5        19         6.00       0.0023      
FO1: Max Créditos              ILP          5        20         4.50       0.1245      
----------------------------------------------------------------------------------------------------
FO2: Min Gaps                  Guloso       5        18         2.00       0.0021      
FO2: Min Gaps                  ILP          5        18         1.50       0.1156      
----------------------------------------------------------------------------------------------------
FO3: Combinada                 Guloso       5        19         4.00       0.0022      
FO3: Combinada                 ILP          5        19         3.50       0.1289      

====================================================================================================
ANÁLISE COMPARATIVA - DIFERENÇAS ENTRE FUNÇÕES OBJETIVO
====================================================================================================

1. COMPARAÇÃO FO1 vs FO2 vs FO3 (Algoritmo ILP - Ótimo):
----------------------------------------------------------------------------------------------------
   FO1 (Max Créditos)    : 20 créditos, 4.50h de gap
   FO2 (Min Gaps)        : 18 créditos, 1.50h de gap
   FO3 (Combinada)       : 19 créditos, 3.50h de gap

   ✓ CONFIRMADO: Funções objetivo diferentes geram RESULTADOS DIFERENTES!

2. COMPARAÇÃO DE DESEMPENHO (Tempo de Execução):
----------------------------------------------------------------------------------------------------
   Função Objetivo          Guloso (s)      ILP (s)         Speedup        
   FO1: Max Créditos        0.0023          0.1245          54.13x
   FO2: Min Gaps            0.0021          0.1156          55.05x
   FO3: Combinada           0.0022          0.1289          58.59x

   ✓ Guloso é MAIS RÁPIDO (heurística)
   ✓ ILP é MAIS LENTO mas garante solução ÓTIMA

3. QUALIDADE DA SOLUÇÃO (ILP vs Guloso):
----------------------------------------------------------------------------------------------------
   FO1: ILP obteve 1 créditos a MAIS (5.3%)
   FO2: ILP teve 0.50h a MENOS de gap (25.0%)
   FO3: ILP créditos=19 gap=3.50h, Guloso créditos=19 gap=4.00h

====================================================================================================
CONCLUSÃO
====================================================================================================

✓ Foram implementados 2 ALGORITMOS:
  1. Branch and Bound (Busca Sistemática com Poda - Ótimo)
  2. ILP (Programação Linear Inteira - Ótimo)

✓ Foram implementadas 3 FUNÇÕES OBJETIVO:
  1. FO1: Maximizar Créditos
  2. FO2: Minimizar Intervalos
  3. FO3: Combinada (Balanceia ambos objetivos)

✓ COMPARAÇÕES REALIZADAS:
  • Desempenho: Tempo de execução de cada algoritmo
  • Resultado: Créditos e gaps obtidos
  • Diferenças: Cada FO pode gerar soluções diferentes

====================================================================================================
```

## Autor
- André Arantes
- Beatriz Demetrio
- Beatriz Fulgêncio

## Referências

- Weighted Interval Scheduling Problem
- Integer Linear Programming
- PuLP - Python Linear Programming Library
