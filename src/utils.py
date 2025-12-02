"""
Utilitários para verificação de conflitos e cálculo de intervalos.

Este módulo fornece funções auxiliares para trabalhar com conjuntos de cursos,
incluindo detecção de conflitos e cálculo de intervalos ociosos.
"""

from typing import List, Set, Tuple
from src.course import Course


def check_conflicts(courses: List[Course]) -> List[Tuple[Course, Course]]:
    """
    Verifica todos os conflitos de horário em uma lista de cursos.
    
    Args:
        courses: Lista de cursos a verificar
        
    Returns:
        Lista de tuplas contendo pares de cursos que conflitam
    """
    conflicts = []
    for i, course1 in enumerate(courses):
        for course2 in courses[i + 1:]:
            if course1.conflicts_with(course2):
                conflicts.append((course1, course2))
    return conflicts


def has_conflicts(courses: List[Course]) -> bool:
    """
    Verifica se há algum conflito de horário em uma lista de cursos.
    
    Args:
        courses: Lista de cursos a verificar
        
    Returns:
        True se há pelo menos um conflito, False caso contrário
    """
    return len(check_conflicts(courses)) > 0


def calculate_total_gap(courses: List[Course]) -> float:
    """
    Calcula o tempo total de intervalo (idle) entre cursos.
    
    Os cursos são ordenados por horário de início antes do cálculo.
    
    Args:
        courses: Lista de cursos
        
    Returns:
        Tempo total de intervalo em horas
    """
    if len(courses) <= 1:
        return 0.0
    
    # Ordena cursos por horário de início
    sorted_courses = sorted(courses, key=lambda c: c.start_time)
    
    total_gap = 0.0
    for i in range(len(sorted_courses) - 1):
        # gap_to() retorna 0 se os cursos se sobrepõem (conflitam)
        gap = sorted_courses[i].gap_to(sorted_courses[i + 1])
        total_gap += gap
    
    return total_gap


def calculate_total_credits(courses: List[Course]) -> int:
    """
    Calcula o número total de créditos de uma lista de cursos.
    
    Args:
        courses: Lista de cursos
        
    Returns:
        Total de créditos
    """
    return sum(course.credits for course in courses)


def check_prerequisites(courses: List[Course], available_course_ids: Set[str]) -> bool:
    """
    Verifica se todos os pré-requisitos dos cursos estão satisfeitos.
    
    Args:
        courses: Lista de cursos a verificar
        available_course_ids: Conjunto de IDs de cursos já cursados/disponíveis
        
    Returns:
        True se todos os pré-requisitos estão satisfeitos, False caso contrário
    """
    for course in courses:
        if course.prerequisites:
            for prereq_id in course.prerequisites:
                if prereq_id not in available_course_ids:
                    return False
    return True


def validate_schedule(courses: List[Course], completed_course_ids: Set[str] = None) -> Tuple[bool, str]:
    """
    Valida se um cronograma de cursos é viável.
    
    Verifica conflitos de horário e pré-requisitos.
    
    Args:
        courses: Lista de cursos no cronograma
        completed_course_ids: Conjunto de IDs de cursos já concluídos
        
    Returns:
        Tupla (é_válido, mensagem_de_erro)
    """
    if completed_course_ids is None:
        completed_course_ids = set()
    
    # Verifica conflitos de horário
    conflicts = check_conflicts(courses)
    if conflicts:
        conflict_info = ", ".join([f"{c1.id} vs {c2.id}" for c1, c2 in conflicts])
        return False, f"Conflitos de horário detectados: {conflict_info}"
    
    # Verifica pré-requisitos
    # Os cursos no cronograma atual + os cursos já concluídos formam o conjunto disponível
    all_available = completed_course_ids.union({c.id for c in courses})
    
    if not check_prerequisites(courses, all_available):
        return False, "Pré-requisitos não satisfeitos"
    
    return True, "Cronograma válido"
