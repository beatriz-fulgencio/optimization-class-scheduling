"""
Algoritmo Branch and Bound para agendamento de cursos.

Este módulo implementa um algoritmo Branch and Bound que explora o espaço
de soluções de forma sistemática, podando ramos que não podem levar a
soluções melhores que a melhor solução encontrada até o momento.
"""

from typing import List, Set, Tuple, Optional
from src.course import Course
from src.utils import calculate_total_credits, calculate_total_gap


class BranchAndBoundNode:
    """
    Representa um nó na árvore de busca do Branch and Bound.
    
    Attributes:
        level: Nível do nó na árvore (índice do curso sendo considerado)
        selected: Lista de cursos selecionados até este nó
        credits: Total de créditos acumulados
        gap: Total de gap acumulado
        bound: Limite superior estimado para este ramo
    """
    def __init__(self, level: int, selected: List[Course], credits: int, gap: float, bound: float):
        self.level = level
        self.selected = selected
        self.credits = credits
        self.gap = gap
        self.bound = bound


def calculate_upper_bound(
    node: BranchAndBoundNode,
    eligible_courses: List[Course],
    objective: str = 'combined',
    gap_penalty: float = 0.1
) -> float:
    """
    Calcula o limite superior (upper bound) para um nó.
    
    Estima o melhor valor possível que pode ser alcançado a partir deste nó,
    considerando os cursos restantes de forma otimista (sem conflitos).
    
    Args:
        node: Nó atual
        eligible_courses: Lista de todos os cursos elegíveis
        objective: Tipo de função objetivo ('max_credits', 'min_gaps', 'combined')
        gap_penalty: Penalidade para gaps (usado em 'combined')
        
    Returns:
        Valor do limite superior
    """
    if objective == 'max_credits':
        # Assume que todos os cursos restantes podem ser adicionados
        remaining_credits = sum(
            c.credits for c in eligible_courses[node.level:]
        )
        return node.credits + remaining_credits
    
    elif objective == 'min_gaps':
        # Para minimização, o bound é o gap atual (otimista: sem gaps adicionais)
        return node.gap
    
    else:  # combined
        # Assume melhor caso: máximo de créditos com gaps mínimos
        remaining_credits = sum(
            c.credits for c in eligible_courses[node.level:]
        )
        return node.credits + remaining_credits - gap_penalty * node.gap


def branch_and_bound_schedule_max_credits(
    available_courses: List[Course],
    completed_course_ids: Set[str] = None
) -> Tuple[List[Course], int, float]:
    """
    Implementa Branch and Bound focado em MAXIMIZAR CRÉDITOS (FO1).
    
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
    
    # Filtra cursos elegíveis
    eligible_courses = [
        course for course in available_courses
        if all(prereq in completed_course_ids for prereq in (course.prerequisites or []))
    ]
    
    if not eligible_courses:
        return [], 0, 0.0
    
    # Ordena por créditos decrescentes para melhor poda
    eligible_courses.sort(key=lambda c: -c.credits)
    
    # Inicializa melhor solução
    best_solution = []
    best_credits = 0
    best_gap = 0.0
    
    # Fila de nós a explorar (DFS usando lista)
    queue = [BranchAndBoundNode(0, [], 0, 0.0, sum(c.credits for c in eligible_courses))]
    
    nodes_explored = 0
    nodes_pruned = 0
    
    while queue:
        node = queue.pop()
        nodes_explored += 1
        
        # Poda: se o limite superior não pode melhorar a melhor solução
        if node.bound <= best_credits:
            nodes_pruned += 1
            continue
        
        # Se chegamos ao final da lista de cursos
        if node.level >= len(eligible_courses):
            if node.credits > best_credits:
                best_solution = node.selected.copy()
                best_credits = node.credits
                best_gap = calculate_total_gap(node.selected)
            continue
        
        current_course = eligible_courses[node.level]
        
        # Verifica se o curso atual conflita com algum já selecionado
        has_conflict = any(
            current_course.conflicts_with(selected)
            for selected in node.selected
        )
        
        # Ramo 1: Incluir o curso atual (se não há conflito)
        if not has_conflict:
            new_selected = node.selected + [current_course]
            new_credits = node.credits + current_course.credits
            new_gap = calculate_total_gap(new_selected)
            new_bound = calculate_upper_bound(
                BranchAndBoundNode(node.level + 1, new_selected, new_credits, new_gap, 0),
                eligible_courses,
                'max_credits'
            )
            
            if new_bound > best_credits:
                queue.append(BranchAndBoundNode(
                    node.level + 1,
                    new_selected,
                    new_credits,
                    new_gap,
                    new_bound
                ))
        
        # Ramo 2: Não incluir o curso atual
        new_bound = calculate_upper_bound(
            BranchAndBoundNode(node.level + 1, node.selected, node.credits, node.gap, 0),
            eligible_courses,
            'max_credits'
        )
        
        if new_bound > best_credits:
            queue.append(BranchAndBoundNode(
                node.level + 1,
                node.selected.copy(),
                node.credits,
                node.gap,
                new_bound
            ))
    
    return best_solution, best_credits, best_gap


def branch_and_bound_schedule_min_gaps(
    available_courses: List[Course],
    completed_course_ids: Set[str] = None
) -> Tuple[List[Course], int, float]:
    """
    Implementa Branch and Bound focado em MINIMIZAR INTERVALOS (FO2).
    
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
    
    # Filtra cursos elegíveis
    eligible_courses = [
        course for course in available_courses
        if all(prereq in completed_course_ids for prereq in (course.prerequisites or []))
    ]
    
    if not eligible_courses:
        return [], 0, 0.0
    
    # Ordena por horário de término para melhor poda
    eligible_courses.sort(key=lambda c: c.end_time)
    
    # Inicializa melhor solução
    best_solution = []
    best_gap = float('inf')
    best_credits = 0
    
    # Fila de nós a explorar
    queue = [BranchAndBoundNode(0, [], 0, 0.0, 0.0)]
    
    while queue:
        node = queue.pop()
        
        # Poda: se o limite inferior não pode melhorar a melhor solução
        if best_gap < float('inf') and node.gap >= best_gap:
            continue
        
        # Se chegamos ao final da lista de cursos
        if node.level >= len(eligible_courses):
            if len(node.selected) > 0:  # Só considera soluções não vazias
                if node.gap < best_gap or (node.gap == best_gap and node.credits > best_credits):
                    best_solution = node.selected.copy()
                    best_gap = node.gap
                    best_credits = node.credits
            continue
        
        current_course = eligible_courses[node.level]
        
        # Verifica conflitos
        has_conflict = any(
            current_course.conflicts_with(selected)
            for selected in node.selected
        )
        
        # Ramo 1: Incluir o curso atual (se não há conflito)
        if not has_conflict:
            new_selected = node.selected + [current_course]
            new_gap = calculate_total_gap(new_selected)
            new_credits = node.credits + current_course.credits
            
            queue.append(BranchAndBoundNode(
                node.level + 1,
                new_selected,
                new_credits,
                new_gap,
                new_gap
            ))
        
        # Ramo 2: Não incluir o curso atual
        queue.append(BranchAndBoundNode(
            node.level + 1,
            node.selected.copy(),
            node.credits,
            node.gap,
            node.gap
        ))
    
    if best_gap == float('inf'):
        return [], 0, 0.0
    
    return best_solution, best_credits, best_gap


def branch_and_bound_schedule(
    available_courses: List[Course],
    completed_course_ids: Set[str] = None,
    gap_penalty: float = 0.1
) -> Tuple[List[Course], int, float]:
    """
    Implementa Branch and Bound COMBINADO para agendamento de cursos (FO3).
    
    Maximiza: créditos - penalidade × gaps
    
    Args:
        available_courses: Lista de cursos disponíveis para agendamento
        completed_course_ids: Conjunto de IDs de cursos já concluídos
        gap_penalty: Penalidade por hora de intervalo
        
    Returns:
        Tupla contendo:
        - Lista de cursos selecionados
        - Total de créditos
        - Total de intervalo (gap) em horas
    """
    if completed_course_ids is None:
        completed_course_ids = set()
    
    # Filtra cursos elegíveis
    eligible_courses = [
        course for course in available_courses
        if all(prereq in completed_course_ids for prereq in (course.prerequisites or []))
    ]
    
    if not eligible_courses:
        return [], 0, 0.0
    
    # Ordena por razão end_time/credits para melhor poda
    eligible_courses.sort(key=lambda c: c.end_time / c.credits)
    
    # Inicializa melhor solução
    best_solution = []
    best_objective = float('-inf')
    best_credits = 0
    best_gap = 0.0
    
    # Fila de nós a explorar
    initial_bound = sum(c.credits for c in eligible_courses)
    queue = [BranchAndBoundNode(0, [], 0, 0.0, initial_bound)]
    
    while queue:
        node = queue.pop()
        
        # Calcula valor objetivo do nó
        objective_value = node.credits - gap_penalty * node.gap
        
        # Poda: se o limite superior não pode melhorar a melhor solução
        if node.bound - gap_penalty * node.gap <= best_objective:
            continue
        
        # Se chegamos ao final da lista de cursos
        if node.level >= len(eligible_courses):
            if objective_value > best_objective:
                best_solution = node.selected.copy()
                best_objective = objective_value
                best_credits = node.credits
                best_gap = node.gap
            continue
        
        current_course = eligible_courses[node.level]
        
        # Verifica conflitos
        has_conflict = any(
            current_course.conflicts_with(selected)
            for selected in node.selected
        )
        
        # Ramo 1: Incluir o curso atual (se não há conflito)
        if not has_conflict:
            new_selected = node.selected + [current_course]
            new_credits = node.credits + current_course.credits
            new_gap = calculate_total_gap(new_selected)
            new_bound = calculate_upper_bound(
                BranchAndBoundNode(node.level + 1, new_selected, new_credits, new_gap, 0),
                eligible_courses,
                'combined',
                gap_penalty
            )
            
            if new_bound - gap_penalty * new_gap > best_objective:
                queue.append(BranchAndBoundNode(
                    node.level + 1,
                    new_selected,
                    new_credits,
                    new_gap,
                    new_bound
                ))
        
        # Ramo 2: Não incluir o curso atual
        new_bound = calculate_upper_bound(
            BranchAndBoundNode(node.level + 1, node.selected, node.credits, node.gap, 0),
            eligible_courses,
            'combined',
            gap_penalty
        )
        
        if new_bound - gap_penalty * node.gap > best_objective:
            queue.append(BranchAndBoundNode(
                node.level + 1,
                node.selected.copy(),
                node.credits,
                node.gap,
                new_bound
            ))
    
    return best_solution, best_credits, best_gap


def branch_and_bound_schedule_with_info(
    available_courses: List[Course],
    completed_course_ids: Set[str] = None,
    gap_penalty: float = 0.1
) -> dict:
    """
    Versão do algoritmo Branch and Bound que retorna informações detalhadas.
    
    Args:
        available_courses: Lista de cursos disponíveis para agendamento
        completed_course_ids: Conjunto de IDs de cursos já concluídos
        gap_penalty: Penalidade para gaps
        
    Returns:
        Dicionário com informações detalhadas sobre o agendamento
    """
    courses, credits, gap = branch_and_bound_schedule(
        available_courses, completed_course_ids, gap_penalty
    )
    
    return {
        'courses': courses,
        'total_credits': credits,
        'total_gap': gap,
        'num_courses': len(courses),
        'course_ids': [c.id for c in courses]
    }
