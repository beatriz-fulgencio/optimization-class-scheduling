"""
Script de comparação entre algoritmos Guloso e ILP com 3 funções objetivo.

Este script compara o desempenho e resultados dos algoritmos
de agendamento de cursos usando 3 funções objetivo diferentes:
- FO1: Maximizar créditos
- FO2: Minimizar intervalos (gaps)
- FO3: Combinada (maximizar créditos - penalidade × gaps)
"""

import json
import time
from typing import List, Set, Dict, Tuple
from src.course import Course
from src.greedy_algorithm import (
    greedy_schedule_max_credits,
    greedy_schedule_min_gaps,
    greedy_schedule
)
from src.ilp_algorithm import (
    ilp_schedule_max_credits,
    ilp_schedule_min_gaps,
    ilp_schedule
)


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


def run_algorithm(
    algorithm_func,
    courses: List[Course],
    completed_ids: Set[str],
    *args
) -> Tuple[List[Course], int, float, float]:
    """
    Executa um algoritmo e mede o tempo de execução.
    
    Returns:
        Tupla com (cursos_selecionados, créditos, gap, tempo)
    """
    start_time = time.time()
    selected, credits, gap = algorithm_func(courses, completed_ids, *args)
    exec_time = time.time() - start_time
    return selected, credits, gap, exec_time


def compare_algorithms(
    available_courses: List[Course],
    completed_course_ids: Set[str] = None,
    gap_penalty: float = 0.1
) -> Dict:
    """
    Compara os algoritmos Guloso e ILP usando 3 funções objetivo diferentes.
    
    Args:
        available_courses: Lista de cursos disponíveis
        completed_course_ids: Conjunto de IDs de cursos já concluídos
        gap_penalty: Penalidade de gap para o algoritmo ILP combinado
        
    Returns:
        Dicionário com resultados comparativos
    """
    if completed_course_ids is None:
        completed_course_ids = set()
    
    print("=" * 100)
    print("COMPARAÇÃO DE ALGORITMOS DE AGENDAMENTO DE CURSOS")
    print("Trabalho Final - Otimização")
    print("=" * 100)
    print()
    print("LIMITAÇÕES DO PROJETO:")
    print("  • Planejamento de grade para UM ALUNO apenas")
    print("  • Planejamento de UM SEMESTRE apenas")
    print()
    print("=" * 100)
    print()
    
    # Dicionário para armazenar todos os resultados
    results = {}
    
    # ========== FUNÇÃO OBJETIVO 1: MAXIMIZAR CRÉDITOS ==========
    print("█" * 100)
    print("FUNÇÃO OBJETIVO 1: MAXIMIZAR CRÉDITOS")
    print("█" * 100)
    print()
    
    print("Executando GULOSO (FO1: Max Créditos)...")
    g1_courses, g1_credits, g1_gap, g1_time = run_algorithm(
        greedy_schedule_max_credits, available_courses, completed_course_ids
    )
    print(f"✓ Concluído em {g1_time:.4f} segundos")
    print()
    
    print("Executando ILP (FO1: Max Créditos)...")
    i1_courses, i1_credits, i1_gap, i1_time = run_algorithm(
        ilp_schedule_max_credits, available_courses, completed_course_ids
    )
    print(f"✓ Concluído em {i1_time:.4f} segundos")
    print()
    
    results['fo1'] = {
        'greedy': {'courses': g1_courses, 'credits': g1_credits, 'gap': g1_gap, 'time': g1_time},
        'ilp': {'courses': i1_courses, 'credits': i1_credits, 'gap': i1_gap, 'time': i1_time}
    }
    
    # ========== FUNÇÃO OBJETIVO 2: MINIMIZAR GAPS ==========
    print("█" * 100)
    print("FUNÇÃO OBJETIVO 2: MINIMIZAR INTERVALOS (GAPS)")
    print("█" * 100)
    print()
    
    print("Executando GULOSO (FO2: Min Gaps)...")
    g2_courses, g2_credits, g2_gap, g2_time = run_algorithm(
        greedy_schedule_min_gaps, available_courses, completed_course_ids
    )
    print(f"✓ Concluído em {g2_time:.4f} segundos")
    print()
    
    print("Executando ILP (FO2: Min Gaps)...")
    i2_courses, i2_credits, i2_gap, i2_time = run_algorithm(
        ilp_schedule_min_gaps, available_courses, completed_course_ids
    )
    print(f"✓ Concluído em {i2_time:.4f} segundos")
    print()
    
    results['fo2'] = {
        'greedy': {'courses': g2_courses, 'credits': g2_credits, 'gap': g2_gap, 'time': g2_time},
        'ilp': {'courses': i2_courses, 'credits': i2_credits, 'gap': i2_gap, 'time': i2_time}
    }
    
    # ========== FUNÇÃO OBJETIVO 3: COMBINADA ==========
    print("█" * 100)
    print("FUNÇÃO OBJETIVO 3: COMBINADA (Créditos - Penalidade × Gaps)")
    print(f"Penalidade de gap: {gap_penalty}")
    print("█" * 100)
    print()
    
    print("Executando GULOSO (FO3: Combinada)...")
    g3_courses, g3_credits, g3_gap, g3_time = run_algorithm(
        greedy_schedule, available_courses, completed_course_ids
    )
    print(f"✓ Concluído em {g3_time:.4f} segundos")
    print()
    
    print("Executando ILP (FO3: Combinada)...")
    i3_courses, i3_credits, i3_gap, i3_time = run_algorithm(
        ilp_schedule, available_courses, completed_course_ids, gap_penalty
    )
    print(f"✓ Concluído em {i3_time:.4f} segundos")
    print()
    
    results['fo3'] = {
        'greedy': {'courses': g3_courses, 'credits': g3_credits, 'gap': g3_gap, 'time': g3_time},
        'ilp': {'courses': i3_courses, 'credits': i3_credits, 'gap': i3_gap, 'time': i3_time}
    }
    
    # ========== TABELA COMPARATIVA ==========
    print("=" * 100)
    print("TABELA COMPARATIVA - RESULTADOS DAS 3 FUNÇÕES OBJETIVO")
    print("=" * 100)
    print()
    
    print(f"{'Função Objetivo':<30} {'Algoritmo':<12} {'Cursos':<8} {'Créditos':<10} {'Gap (h)':<10} {'Tempo (s)':<12}")
    print("-" * 100)
    
    # FO1
    print(f"{'FO1: Max Créditos':<30} {'Guloso':<12} {len(g1_courses):<8} {g1_credits:<10} {g1_gap:<10.2f} {g1_time:<12.4f}")
    print(f"{'FO1: Max Créditos':<30} {'ILP':<12} {len(i1_courses):<8} {i1_credits:<10} {i1_gap:<10.2f} {i1_time:<12.4f}")
    print("-" * 100)
    
    # FO2
    print(f"{'FO2: Min Gaps':<30} {'Guloso':<12} {len(g2_courses):<8} {g2_credits:<10} {g2_gap:<10.2f} {g2_time:<12.4f}")
    print(f"{'FO2: Min Gaps':<30} {'ILP':<12} {len(i2_courses):<8} {i2_credits:<10} {i2_gap:<10.2f} {i2_time:<12.4f}")
    print("-" * 100)
    
    # FO3
    print(f"{'FO3: Combinada':<30} {'Guloso':<12} {len(g3_courses):<8} {g3_credits:<10} {g3_gap:<10.2f} {g3_time:<12.4f}")
    print(f"{'FO3: Combinada':<30} {'ILP':<12} {len(i3_courses):<8} {i3_credits:<10} {i3_gap:<10.2f} {i3_time:<12.4f}")
    print()
    
    # ========== ANÁLISE COMPARATIVA ==========
    print("=" * 100)
    print("ANÁLISE COMPARATIVA - DIFERENÇAS ENTRE FUNÇÕES OBJETIVO")
    print("=" * 100)
    print()
    
    print("1. COMPARAÇÃO FO1 vs FO2 vs FO3 (Algoritmo ILP - Ótimo):")
    print("-" * 100)
    print(f"   FO1 (Max Créditos)    : {i1_credits} créditos, {i1_gap:.2f}h de gap")
    print(f"   FO2 (Min Gaps)        : {i2_credits} créditos, {i2_gap:.2f}h de gap")
    print(f"   FO3 (Combinada)       : {i3_credits} créditos, {i3_gap:.2f}h de gap")
    print()
    
    # Mostra que diferentes FOs geram diferentes resultados
    if i1_credits != i2_credits or i1_gap != i2_gap:
        print("   ✓ CONFIRMADO: Funções objetivo diferentes geram RESULTADOS DIFERENTES!")
    else:
        print("   ⚠ Neste caso específico, as FOs geraram resultados similares")
    print()
    
    print("2. COMPARAÇÃO DE DESEMPENHO (Tempo de Execução):")
    print("-" * 100)
    print(f"   {'Função Objetivo':<25} {'Guloso (s)':<15} {'ILP (s)':<15} {'Speedup':<15}")
    print(f"   {'FO1: Max Créditos':<25} {g1_time:<15.4f} {i1_time:<15.4f} {i1_time/g1_time if g1_time > 0 else 0:<15.2f}x")
    print(f"   {'FO2: Min Gaps':<25} {g2_time:<15.4f} {i2_time:<15.4f} {i2_time/g2_time if g2_time > 0 else 0:<15.2f}x")
    print(f"   {'FO3: Combinada':<25} {g3_time:<15.4f} {i3_time:<15.4f} {i3_time/g3_time if g3_time > 0 else 0:<15.2f}x")
    print()
    print(f"   ✓ Guloso é MAIS RÁPIDO (heurística)")
    print(f"   ✓ ILP é MAIS LENTO mas garante solução ÓTIMA")
    print()
    
    print("3. QUALIDADE DA SOLUÇÃO (ILP vs Guloso):")
    print("-" * 100)
    
    # FO1
    if i1_credits > g1_credits:
        print(f"   FO1: ILP obteve {i1_credits - g1_credits} créditos a MAIS ({((i1_credits-g1_credits)/g1_credits*100):.1f}%)")
    elif i1_credits < g1_credits:
        print(f"   FO1: Guloso obteve {g1_credits - i1_credits} créditos a MAIS")
    else:
        print(f"   FO1: Mesma quantidade de créditos ({i1_credits})")
    
    # FO2
    if i2_gap < g2_gap:
        print(f"   FO2: ILP teve {g2_gap - i2_gap:.2f}h a MENOS de gap ({((g2_gap-i2_gap)/g2_gap*100):.1f}%)")
    elif i2_gap > g2_gap:
        print(f"   FO2: Guloso teve {i2_gap - g2_gap:.2f}h a MENOS de gap")
    else:
        print(f"   FO2: Mesmo gap total ({i2_gap:.2f}h)")
    
    # FO3
    print(f"   FO3: ILP créditos={i3_credits} gap={i3_gap:.2f}h, Guloso créditos={g3_credits} gap={g3_gap:.2f}h")
    print()
    
    # ========== CURSOS SELECIONADOS ==========
    print("=" * 100)
    print("CURSOS SELECIONADOS POR CADA FUNÇÃO OBJETIVO")
    print("=" * 100)
    print()
    
    for fo_name, fo_data in [('FO1 (Max Créditos)', results['fo1']), 
                              ('FO2 (Min Gaps)', results['fo2']), 
                              ('FO3 (Combinada)', results['fo3'])]:
        print(f"--- {fo_name} - ILP (Ótimo) ---")
        for course in sorted(fo_data['ilp']['courses'], key=lambda c: c.start_time):
            print(f"  {course.id:<10} {course.name:<40} {course.start_time:.1f}h-{course.end_time:.1f}h ({course.credits} créd)")
        print()
        
        print(f"--- {fo_name} - Guloso (Heurística) ---")
        for course in sorted(fo_data['greedy']['courses'], key=lambda c: c.start_time):
            print(f"  {course.id:<10} {course.name:<40} {course.start_time:.1f}h-{course.end_time:.1f}h ({course.credits} créd)")
        print()
    
    print("=" * 100)
    print("CONCLUSÃO")
    print("=" * 100)
    print()
    print("✓ Foram implementados 2 ALGORITMOS:")
    print("  1. Guloso (Heurística - Rápido)")
    print("  2. ILP (Otimização Exata - Lento mas Ótimo)")
    print()
    print("✓ Foram implementadas 3 FUNÇÕES OBJETIVO:")
    print("  1. FO1: Maximizar Créditos")
    print("  2. FO2: Minimizar Intervalos")
    print("  3. FO3: Combinada (Balanceia ambos objetivos)")
    print()
    print("✓ COMPARAÇÕES REALIZADAS:")
    print("  • Desempenho: Tempo de execução de cada algoritmo")
    print("  • Resultado: Créditos e gaps obtidos")
    print("  • Diferenças: Cada FO pode gerar soluções diferentes")
    print()
    print("=" * 100)
    
    return results


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
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
