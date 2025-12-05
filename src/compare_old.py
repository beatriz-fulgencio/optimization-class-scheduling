"""
Script de comparação entre algoritmos Guloso e ILP.

Este script compara o desempenho e resultados dos algoritmos
de agendamento de cursos, fornecendo métricas detalhadas.
"""

import json
import time
from typing import List, Set
from src.course import Course
from src.greedy_algorithm import greedy_schedule_with_info
from src.ilp_algorithm import ilp_schedule_with_info


def load_courses_from_json(filepath: str) -> List[Course]:
    """
    Carrega cursos de um arquivo JSON.
    
    Args:
        filepath: Caminho para o arquivo JSON
        
    Returns:
        Lista de objetos Course
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    courses = []
    for course_data in data['courses']:
        course = Course(
            id=course_data['id'],
            name=course_data['name'],
            start_time=course_data['start_time'],
            end_time=course_data['end_time'],
            credits=course_data['credits'],
            prerequisites=course_data.get('prerequisites', [])
        )
        courses.append(course)
    
    return courses


def compare_algorithms(
    available_courses: List[Course],
    completed_course_ids: Set[str] = None,
    gap_penalty: float = 0.1
) -> dict:
    """
    Compara os algoritmos Guloso e ILP para um conjunto de cursos.
    
    Args:
        available_courses: Lista de cursos disponíveis
        completed_course_ids: Conjunto de IDs de cursos já concluídos
        gap_penalty: Penalidade de gap para o algoritmo ILP
        
    Returns:
        Dicionário com resultados comparativos
    """
    if completed_course_ids is None:
        completed_course_ids = set()
    
    print("=" * 80)
    print("COMPARAÇÃO DE ALGORITMOS DE AGENDAMENTO DE CURSOS")
    print("=" * 80)
    print()
    
    # Algoritmo Guloso
    print("Executando algoritmo GULOSO...")
    start_time = time.time()
    greedy_result = greedy_schedule_with_info(available_courses, completed_course_ids)
    greedy_time = time.time() - start_time
    
    print(f"✓ Concluído em {greedy_time:.4f} segundos")
    print()
    
    # Algoritmo ILP
    print("Executando algoritmo ILP...")
    start_time = time.time()
    ilp_result = ilp_schedule_with_info(available_courses, completed_course_ids, gap_penalty)
    ilp_time = time.time() - start_time
    
    print(f"✓ Concluído em {ilp_time:.4f} segundos")
    print()
    
    # Resultados
    print("=" * 80)
    print("RESULTADOS")
    print("=" * 80)
    print()
    
    print(f"{'Métrica':<30} {'Guloso':<25} {'ILP':<25}")
    print("-" * 80)
    print(f"{'Número de cursos':<30} {greedy_result['num_courses']:<25} {ilp_result['num_courses']:<25}")
    print(f"{'Créditos totais':<30} {greedy_result['total_credits']:<25} {ilp_result['total_credits']:<25}")
    print(f"{'Gap total (horas)':<30} {greedy_result['total_gap']:<25.2f} {ilp_result['total_gap']:<25.2f}")
    print(f"{'Tempo de execução (s)':<30} {greedy_time:<25.4f} {ilp_time:<25.4f}")
    print()
    
    # Cursos selecionados
    print("CURSOS SELECIONADOS - GULOSO:")
    print("-" * 80)
    for course in sorted(greedy_result['courses'], key=lambda c: c.start_time):
        print(f"  {course.id:<10} {course.name:<40} {course.start_time:.1f}h-{course.end_time:.1f}h ({course.credits} créditos)")
    print()
    
    print("CURSOS SELECIONADOS - ILP:")
    print("-" * 80)
    for course in sorted(ilp_result['courses'], key=lambda c: c.start_time):
        print(f"  {course.id:<10} {course.name:<40} {course.start_time:.1f}h-{course.end_time:.1f}h ({course.credits} créditos)")
    print()
    
    # Análise comparativa
    print("=" * 80)
    print("ANÁLISE COMPARATIVA")
    print("=" * 80)
    print()
    
    credits_diff = ilp_result['total_credits'] - greedy_result['total_credits']
    gap_diff = ilp_result['total_gap'] - greedy_result['total_gap']
    
    if credits_diff > 0:
        print(f"✓ ILP obteve {credits_diff} créditos a mais que Guloso")
    elif credits_diff < 0:
        print(f"✓ Guloso obteve {-credits_diff} créditos a mais que ILP")
    else:
        print("✓ Ambos os algoritmos obtiveram o mesmo número de créditos")
    
    if gap_diff < 0:
        print(f"✓ ILP teve {-gap_diff:.2f} horas a menos de gap que Guloso")
    elif gap_diff > 0:
        print(f"✓ Guloso teve {gap_diff:.2f} horas a menos de gap que ILP")
    else:
        print("✓ Ambos os algoritmos tiveram o mesmo gap total")
    
    # Calcula speedup do algoritmo guloso em relação ao ILP
    # Protege contra divisão por zero quando ILP é instantâneo
    if ilp_time > 1e-6:  # Usa epsilon para evitar problemas de precisão de ponto flutuante
        speedup = greedy_time / ilp_time
        print(f"\n✓ Guloso foi {speedup:.2f}x mais rápido que ILP")
    else:
        print(f"\n✓ Tempo de ILP foi muito pequeno para comparação precisa")
    print()
    
    return {
        'greedy': greedy_result,
        'ilp': ilp_result,
        'greedy_time': greedy_time,
        'ilp_time': ilp_time,
        'credits_difference': credits_diff,
        'gap_difference': gap_diff
    }


def main():
    """Função principal para execução do script de comparação."""
    import sys
    
    # Caminho padrão para os dados de exemplo
    data_file = 'data/sample_courses.json'
    
    if len(sys.argv) > 1:
        data_file = sys.argv[1]
    
    print(f"Carregando cursos de: {data_file}")
    print()
    
    try:
        courses = load_courses_from_json(data_file)
        print(f"✓ {len(courses)} cursos carregados com sucesso")
        print()
        
        # Executa a comparação
        compare_algorithms(courses)
        
    except FileNotFoundError:
        print(f"Erro: Arquivo '{data_file}' não encontrado")
        sys.exit(1)
    except Exception as e:
        print(f"Erro: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
