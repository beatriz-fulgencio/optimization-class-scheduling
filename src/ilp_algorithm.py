"""
Algoritmo de Programação Linear Inteira (ILP) para agendamento ótimo de cursos.

Este módulo implementa uma solução exata usando ILP para maximizar créditos
enquanto minimiza intervalos ociosos no agendamento de cursos.
"""

from typing import List, Set, Tuple, Optional
import pulp
from src.course import Course
from src.utils import calculate_total_credits, calculate_total_gap


def ilp_schedule(
    available_courses: List[Course],
    completed_course_ids: Set[str] = None,
    gap_penalty: float = 0.1
) -> Tuple[List[Course], int, float]:
    """
    Implementa o algoritmo ILP para agendamento ótimo de cursos.
    
    O problema é formulado como um problema de otimização onde:
    - Maximizamos: (créditos totais) - (penalidade * gap total)
    - Restrições: não pode haver conflitos de horário e pré-requisitos devem ser satisfeitos
    
    Args:
        available_courses: Lista de cursos disponíveis para agendamento
        completed_course_ids: Conjunto de IDs de cursos já concluídos (para pré-requisitos)
        gap_penalty: Penalidade por hora de intervalo (padrão: 0.1)
        
    Returns:
        Tupla contendo:
        - Lista de cursos selecionados
        - Total de créditos
        - Total de intervalo (gap) em horas
    """
    if completed_course_ids is None:
        completed_course_ids = set()
    
    if not available_courses:
        return [], 0, 0.0
    
    # Filtra cursos cujos pré-requisitos foram satisfeitos
    eligible_courses = [
        course for course in available_courses
        if all(prereq in completed_course_ids for prereq in (course.prerequisites or []))
    ]
    
    if not eligible_courses:
        return [], 0, 0.0
    
    # Cria o problema de otimização
    prob = pulp.LpProblem("Course_Scheduling", pulp.LpMaximize)
    
    # Variáveis de decisão: x[i] = 1 se o curso i é selecionado, 0 caso contrário
    x = {}
    for i, course in enumerate(eligible_courses):
        x[i] = pulp.LpVariable(f"x_{course.id}", cat='Binary')
    
    # Função objetivo: maximizar créditos - penalidade * gap
    # Primeira parte: soma dos créditos
    credits_term = pulp.lpSum([x[i] * course.credits for i, course in enumerate(eligible_courses)])
    
    # Para calcular o gap, usamos variáveis auxiliares
    # y[i][j] = 1 se ambos os cursos i e j são selecionados e i vem antes de j
    y = {}
    gap_terms = []
    
    for i, course_i in enumerate(eligible_courses):
        for j, course_j in enumerate(eligible_courses):
            if i < j:
                # Verifica se course_i termina antes de course_j começar
                if course_i.end_time <= course_j.start_time:
                    # Cria variável para indicar se ambos são selecionados sequencialmente
                    y[(i, j)] = pulp.LpVariable(f"y_{i}_{j}", cat='Binary')
                    
                    # y[i,j] <= x[i]
                    prob += y[(i, j)] <= x[i]
                    # y[i,j] <= x[j]
                    prob += y[(i, j)] <= x[j]
                    # y[i,j] >= x[i] + x[j] - 1
                    prob += y[(i, j)] >= x[i] + x[j] - 1
                    
                    # Adiciona gap ponderado
                    gap = course_j.start_time - course_i.end_time
                    gap_terms.append(y[(i, j)] * gap * gap_penalty)
    
    # Função objetivo completa
    if gap_terms:
        prob += credits_term - pulp.lpSum(gap_terms)
    else:
        prob += credits_term
    
    # Restrições de conflito: cursos que se sobrepõem não podem ser selecionados juntos
    for i, course_i in enumerate(eligible_courses):
        for j, course_j in enumerate(eligible_courses):
            if i < j and course_i.conflicts_with(course_j):
                prob += x[i] + x[j] <= 1
    
    # Resolve o problema
    prob.solve(pulp.PULP_CBC_CMD(msg=0))
    
    # Extrai a solução
    selected_courses = []
    for i, course in enumerate(eligible_courses):
        if pulp.value(x[i]) == 1:
            selected_courses.append(course)
    
    total_credits = calculate_total_credits(selected_courses)
    total_gap = calculate_total_gap(selected_courses)
    
    return selected_courses, total_credits, total_gap


def ilp_schedule_with_info(
    available_courses: List[Course],
    completed_course_ids: Set[str] = None,
    gap_penalty: float = 0.1
) -> dict:
    """
    Versão do algoritmo ILP que retorna informações detalhadas.
    
    Args:
        available_courses: Lista de cursos disponíveis para agendamento
        completed_course_ids: Conjunto de IDs de cursos já concluídos
        gap_penalty: Penalidade por hora de intervalo
        
    Returns:
        Dicionário com informações detalhadas sobre o agendamento:
        - 'courses': Lista de cursos selecionados
        - 'total_credits': Total de créditos
        - 'total_gap': Total de intervalo em horas
        - 'num_courses': Número de cursos selecionados
        - 'course_ids': Lista de IDs dos cursos selecionados
        - 'gap_penalty': Penalidade usada
    """
    courses, credits, gap = ilp_schedule(available_courses, completed_course_ids, gap_penalty)
    
    return {
        'courses': courses,
        'total_credits': credits,
        'total_gap': gap,
        'num_courses': len(courses),
        'course_ids': [c.id for c in courses],
        'gap_penalty': gap_penalty
    }
