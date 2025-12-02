"""
Algoritmo heurístico guloso para agendamento de cursos.

Este módulo implementa uma abordagem gulosa que ordena os cursos pela
razão entre horário de término e créditos, maximizando créditos enquanto
minimiza os intervalos ociosos.
"""

from typing import List, Set, Tuple
from src.course import Course
from src.utils import calculate_total_credits, calculate_total_gap


def greedy_schedule_max_credits(
    available_courses: List[Course],
    completed_course_ids: Set[str] = None
) -> Tuple[List[Course], int, float]:
    """
    Implementa o algoritmo guloso focado em MAXIMIZAR CRÉDITOS (FO1).
    
    O algoritmo ordena os cursos por créditos (maior primeiro),
    e depois por horário de término (menor primeiro) em caso de empate.
    
    Args:
        available_courses: Lista de cursos disponíveis para agendamento
        completed_course_ids: Conjunto de IDs de cursos já concluídos
        
    Returns:
        Tupla contendo:
        - Lista de cursos selecionados
        - Total de créditos
        - Total de intervalo (gap) em horas
    """
    if completed_course_ids is None:
        completed_course_ids = set()
    
    # Filtra cursos cujos pré-requisitos foram satisfeitos
    eligible_courses = [
        course for course in available_courses
        if all(prereq in completed_course_ids for prereq in (course.prerequisites or []))
    ]
    
    # Ordena por créditos (maior primeiro), depois por horário de término (menor primeiro)
    sorted_courses = sorted(
        eligible_courses,
        key=lambda c: (-c.credits, c.end_time)
    )
    
    selected_courses = []
    
    for course in sorted_courses:
        has_conflict = False
        for selected in selected_courses:
            if course.conflicts_with(selected):
                has_conflict = True
                break
        
        if not has_conflict:
            selected_courses.append(course)
    
    total_credits = calculate_total_credits(selected_courses)
    total_gap = calculate_total_gap(selected_courses)
    
    return selected_courses, total_credits, total_gap


def greedy_schedule_min_gaps(
    available_courses: List[Course],
    completed_course_ids: Set[str] = None
) -> Tuple[List[Course], int, float]:
    """
    Implementa o algoritmo guloso focado em MINIMIZAR INTERVALOS (FO2).
    
    O algoritmo ordena os cursos por horário de término (menor primeiro),
    priorizando cursos que terminam mais cedo para minimizar gaps.
    
    Args:
        available_courses: Lista de cursos disponíveis para agendamento
        completed_course_ids: Conjunto de IDs de cursos já concluídos
        
    Returns:
        Tupla contendo:
        - Lista de cursos selecionados
        - Total de créditos
        - Total de intervalo (gap) em horas
    """
    if completed_course_ids is None:
        completed_course_ids = set()
    
    # Filtra cursos cujos pré-requisitos foram satisfeitos
    eligible_courses = [
        course for course in available_courses
        if all(prereq in completed_course_ids for prereq in (course.prerequisites or []))
    ]
    
    # Ordena por horário de término (menor primeiro)
    sorted_courses = sorted(
        eligible_courses,
        key=lambda c: c.end_time
    )
    
    selected_courses = []
    
    for course in sorted_courses:
        has_conflict = False
        for selected in selected_courses:
            if course.conflicts_with(selected):
                has_conflict = True
                break
        
        if not has_conflict:
            selected_courses.append(course)
    
    total_credits = calculate_total_credits(selected_courses)
    total_gap = calculate_total_gap(selected_courses)
    
    return selected_courses, total_credits, total_gap


def greedy_schedule(
    available_courses: List[Course],
    completed_course_ids: Set[str] = None
) -> Tuple[List[Course], int, float]:
    """
    Implementa o algoritmo guloso COMBINADO para agendamento de cursos (FO3).
    
    O algoritmo ordena os cursos pela razão end_time/credits (menor primeiro),
    priorizando cursos que terminam mais cedo e têm mais créditos.
    Esta é uma abordagem balanceada que considera ambos os objetivos.
    Em seguida, seleciona cursos que não conflitam entre si.
    
    Args:
        available_courses: Lista de cursos disponíveis para agendamento
        completed_course_ids: Conjunto de IDs de cursos já concluídos (para pré-requisitos)
        
    Returns:
        Tupla contendo:
        - Lista de cursos selecionados
        - Total de créditos
        - Total de intervalo (gap) em horas
    """
    if completed_course_ids is None:
        completed_course_ids = set()
    
    # Filtra cursos cujos pré-requisitos foram satisfeitos
    eligible_courses = [
        course for course in available_courses
        if all(prereq in completed_course_ids for prereq in (course.prerequisites or []))
    ]
    
    # Ordena por razão end_time/credits (menor valor = melhor)
    # Cursos que terminam mais cedo e têm mais créditos são priorizados
    sorted_courses = sorted(
        eligible_courses,
        key=lambda c: c.end_time / c.credits
    )
    
    selected_courses = []
    
    for course in sorted_courses:
        # Verifica se o curso conflita com algum curso já selecionado
        has_conflict = False
        for selected in selected_courses:
            if course.conflicts_with(selected):
                has_conflict = True
                break
        
        if not has_conflict:
            selected_courses.append(course)
    
    total_credits = calculate_total_credits(selected_courses)
    total_gap = calculate_total_gap(selected_courses)
    
    return selected_courses, total_credits, total_gap


def greedy_schedule_with_info(
    available_courses: List[Course],
    completed_course_ids: Set[str] = None
) -> dict:
    """
    Versão do algoritmo guloso que retorna informações detalhadas.
    
    Args:
        available_courses: Lista de cursos disponíveis para agendamento
        completed_course_ids: Conjunto de IDs de cursos já concluídos
        
    Returns:
        Dicionário com informações detalhadas sobre o agendamento:
        - 'courses': Lista de cursos selecionados
        - 'total_credits': Total de créditos
        - 'total_gap': Total de intervalo em horas
        - 'num_courses': Número de cursos selecionados
        - 'course_ids': Lista de IDs dos cursos selecionados
    """
    courses, credits, gap = greedy_schedule(available_courses, completed_course_ids)
    
    return {
        'courses': courses,
        'total_credits': credits,
        'total_gap': gap,
        'num_courses': len(courses),
        'course_ids': [c.id for c in courses]
    }
