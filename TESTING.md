# Guia de Testes

Este documento fornece instruções completas para executar os testes do projeto de otimização de agendamento de cursos.

## Pré-requisitos

Certifique-se de que as dependências estão instaladas:

```bash
pip install -r requirements.txt
```

As principais dependências para testes são:
- `pytest>=7.4.0` - Framework de testes
- `pulp>=2.7.0` - Biblioteca de otimização (necessária para os algoritmos)

## Estrutura dos Testes

O projeto possui 54 testes organizados em 5 arquivos:

```
tests/
├── test_course.py                      # 8 testes - Modelo de curso
├── test_branch_and_bound_algorithm.py  # 11 testes - Algoritmo Branch and Bound
├── test_ilp_algorithm.py               # 10 testes - Algoritmo ILP
├── test_integration.py                 # 8 testes - Testes de integração
└── test_utils.py                       # 17 testes - Funções utilitárias
```

## Executando os Testes

### Executar Todos os Testes

```bash
python -m pytest tests/
```

Ou simplesmente:

```bash
pytest
```

### Executar com Saída Detalhada

```bash
pytest -v
```

### Executar um Arquivo Específico

```bash
# Testes do Branch and Bound
pytest tests/test_branch_and_bound_algorithm.py -v

# Testes do ILP
pytest tests/test_ilp_algorithm.py -v

# Testes de integração
pytest tests/test_integration.py -v

# Testes das funções utilitárias
pytest tests/test_utils.py -v

# Testes do modelo de curso
pytest tests/test_course.py -v
```

### Executar um Teste Específico

```bash
pytest tests/test_branch_and_bound_algorithm.py::test_bnb_schedule_no_conflicts -v
```

### Executar com Cobertura de Código

```bash
pytest --cov=src --cov-report=html
```

Isso gerará um relatório HTML em `htmlcov/index.html`.

### Executar com Cobertura e Detalhes

```bash
pytest --cov=src --cov-report=term-missing -v
```

### Executar Testes que Falharam na Última Execução

```bash
pytest --lf
```

### Executar Apenas Testes Rápidos (sem testes lentos)

```bash
pytest -m "not slow"
```

## Opções Úteis do Pytest

| Opção | Descrição |
|-------|-----------|
| `-v` ou `--verbose` | Saída detalhada |
| `-s` | Mostra prints durante os testes |
| `-x` | Para na primeira falha |
| `--tb=short` | Traceback resumido |
| `--tb=line` | Traceback de uma linha |
| `-k EXPRESSION` | Executa testes que correspondem à expressão |
| `--collect-only` | Lista todos os testes sem executá-los |
| `-q` | Modo silencioso |
| `--durations=10` | Mostra os 10 testes mais lentos |

## Exemplos Práticos

### Executar apenas testes relacionados a conflitos

```bash
pytest -k "conflict" -v
```

### Executar apenas testes de otimalidade

```bash
pytest -k "optimal" -v
```

### Executar testes com tempo de execução

```bash
pytest --durations=0 -v
```

### Ver quais testes serão executados sem executá-los

```bash
pytest --collect-only
```

## Verificando Erros e Warnings

### Executar com modo strict (warnings são erros)

```bash
pytest --strict-warnings
```

### Mostrar warnings

```bash
pytest -W default
```

## Continuous Integration

Para CI/CD, recomenda-se:

```bash
pytest -v --tb=short --cov=src --cov-report=xml --cov-report=term
```

## Depuração

### Entrar no debugger quando um teste falha

```bash
pytest --pdb
```

### Usar breakpoint no código

Adicione `breakpoint()` no código de teste e execute:

```bash
pytest -s
```

## Testes por Categoria

### Testes do Modelo de Dados

```bash
pytest tests/test_course.py tests/test_utils.py -v
```

### Testes dos Algoritmos

```bash
pytest tests/test_branch_and_bound_algorithm.py tests/test_ilp_algorithm.py -v
```

### Testes de Integração e Sistema

```bash
pytest tests/test_integration.py -v
```

## Verificando a Integridade do Projeto

Execute esta sequência de comandos para verificação completa:

```bash
# 1. Executar todos os testes
pytest -v

# 2. Verificar cobertura
pytest --cov=src --cov-report=term-missing

# 3. Verificar se há testes duplicados ou mal nomeados
pytest --collect-only

# 4. Executar script de comparação
python -m src.compare
```

## Resultados Esperados

Todos os 54 testes devem passar:

```
============================== 54 passed in X.XXs ==============================
```

Se algum teste falhar, verifique:
1. Se as dependências estão instaladas corretamente
2. Se você está no diretório correto do projeto
3. Se não há conflitos de importação
4. Se os arquivos de dados necessários existem (`data/sample_courses.json`)

## Troubleshooting

### Erro: "ModuleNotFoundError: No module named 'src'"

Execute os testes do diretório raiz do projeto:

```bash
cd /caminho/para/optimization-main
pytest
```

### Erro: "No module named 'pulp'"

Instale as dependências:

```bash
pip install -r requirements.txt
```

### Testes Lentos

Se os testes do ILP estiverem muito lentos, verifique se o solver CBC está instalado corretamente:

```bash
python -c "import pulp; print(pulp.PULP_CBC_CMD().available())"
```

## Executando Testes em Paralelo

Para acelerar a execução, instale pytest-xdist:

```bash
pip install pytest-xdist
```

E execute:

```bash
pytest -n auto
```

Isso executará os testes em múltiplos processos.

## Relatórios de Teste

### Gerar relatório JUnit (para CI/CD)

```bash
pytest --junitxml=test-results.xml
```

### Gerar relatório HTML

```bash
pytest --html=report.html --self-contained-html
```

(Requer: `pip install pytest-html`)

## Contato

Se você encontrar problemas com os testes, verifique:
- README.md para informações gerais do projeto
- RESUMO_MODIFICACOES.md para detalhes sobre as implementações
- Issues no repositório GitHub

---

**Última atualização:** Dezembro 2025
