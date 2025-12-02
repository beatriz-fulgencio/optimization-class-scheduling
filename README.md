# Academic Course Scheduling Optimization

Sistema de otimização de agendamento de cursos acadêmicos usando Weighted Interval Scheduling.

## Descrição

Este repositório implementa dois algoritmos para resolver o problema de agendamento ponderado de intervalos no contexto de cursos acadêmicos:

1. **Algoritmo Guloso (Heurístico)**: Ordena cursos pela razão `end_time/credits`, priorizando cursos que terminam mais cedo e têm mais créditos. Seleciona cursos de forma gulosa evitando conflitos.

2. **Programação Linear Inteira (ILP)**: Solução exata que maximiza créditos enquanto minimiza intervalos ociosos (gaps), respeitando todas as restrições de conflitos e pré-requisitos.

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

### Executar Comparação dos Algoritmos

```bash
python -m src.compare
```

Ou especifique um arquivo JSON personalizado:

```bash
python -m src.compare data/meus_cursos.json
```

### Usar no Código Python

```python
from src.course import Course
from src.greedy_algorithm import greedy_schedule
from src.ilp_algorithm import ilp_schedule

# Criar cursos
courses = [
    Course("MAT101", "Cálculo I", 8.0, 10.0, 4),
    Course("FIS101", "Física I", 10.0, 12.0, 4),
    Course("PROG101", "Programação", 14.0, 16.0, 4),
]

# Executar algoritmo guloso
selected_greedy, credits_greedy, gap_greedy = greedy_schedule(courses)
print(f"Guloso: {credits_greedy} créditos, {gap_greedy:.1f}h de gap")

# Executar algoritmo ILP
selected_ilp, credits_ilp, gap_ilp = ilp_schedule(courses)
print(f"ILP: {credits_ilp} créditos, {gap_ilp:.1f}h de gap")
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

### Algoritmo Guloso

- **Complexidade**: O(n² log n) onde n é o número de cursos
- **Estratégia**: Ordena por `end_time/credits` (menor primeiro)
- **Vantagem**: Muito rápido, mesmo para grandes conjuntos de dados
- **Limitação**: Solução heurística, pode não ser ótima

### Algoritmo ILP

- **Complexidade**: Exponencial no pior caso (NP-difícil)
- **Estratégia**: Formulação como problema de otimização linear inteira
- **Vantagem**: Garante solução ótima
- **Limitação**: Pode ser lento para problemas muito grandes

## Métricas de Otimização

O sistema otimiza:

1. **Maximizar Créditos**: Total de créditos dos cursos selecionados
2. **Minimizar Gaps**: Intervalos ociosos entre cursos consecutivos

A função objetivo do ILP é:
```
maximize: (total_credits) - (gap_penalty × total_gap)
```

## Restrições

- **Conflitos de Horário**: Cursos não podem se sobrepor
- **Pré-requisitos**: Só podem ser cursados se os pré-requisitos foram concluídos

## Exemplos de Saída

```
================================================================================
COMPARAÇÃO DE ALGORITMOS DE AGENDAMENTO DE CURSOS
================================================================================

Executando algoritmo GULOSO...
✓ Concluído em 0.0023 segundos

Executando algoritmo ILP...
✓ Concluído em 0.1245 segundos

================================================================================
RESULTADOS
================================================================================

Métrica                        Guloso                    ILP                      
--------------------------------------------------------------------------------
Número de cursos               5                         5                        
Créditos totais                19                        20                       
Gap total (horas)              6.00                      4.00                     
Tempo de execução (s)          0.0023                    0.1245                   
```

## Contribuindo

Contribuições são bem-vindas! Por favor:

1. Faça fork do repositório
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -am 'Adiciona nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request

## Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## Autor

Beatriz Fulgêncio

## Referências

- Weighted Interval Scheduling Problem
- Integer Linear Programming
- PuLP - Python Linear Programming Library