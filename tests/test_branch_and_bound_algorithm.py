"""
Testes para o algoritmo Branch and Bound.
"""

import pytest
from src.course import Course
from src.branch_and_bound_algorithm import (
    branch_and_bound_schedule,
    branch_and_bound_schedule_with_info,
    branch_and_bound_schedule_max_credits,
    branch_and_bound_schedule_min_gaps
)


def test_bnb_schedule_no_conflicts():
    """Testa agendamento Branch and Bound sem conflitos."""
    courses = [
        Course("C1", "Course 1", 8.0, 10.0, 4),
        Course("C2", "Course 2", 10.0, 12.0, 3),
        Course("C3", "Course 3", 14.0, 16.0, 5),
    ]
    
    selected, credits, gap = branch_and_bound_schedule(courses)
    
    # Todos os cursos devem ser selecionados (sem conflitos)
    assert len(selected) == 3
    assert credits == 12
    assert gap == 2.0  # Gap entre C2 (12h) e C3 (14h)


def test_bnb_schedule_with_conflicts():
    """Testa agendamento Branch and Bound com conflitos."""
    courses = [
        Course("C1", "Course 1", 8.0, 10.0, 4),
        Course("C2", "Course 2", 9.0, 11.0, 3),
        Course("C3", "Course 3", 14.0, 16.0, 5),
    ]
    
    selected, credits, gap = branch_and_bound_schedule(courses)
    
    # C1 e C2 conflitam, o algoritmo deve escolher otimamente
    assert len(selected) == 2
    # Deve incluir C3 (5 créditos) e C1 (4 créditos) para máximo
    assert any(c.id == "C3" for c in selected)
    assert credits == 9  # C1 (4) + C3 (5)


def test_bnb_schedule_max_credits():
    """Testa Branch and Bound focado em maximizar créditos."""
    courses = [
        Course("C1", "Course 1", 8.0, 10.0, 2),
        Course("C2", "Course 2", 8.0, 10.0, 5),  # Mesmo horário, mais créditos
        Course("C3", "Course 3", 14.0, 16.0, 3),
    ]
    
    selected, credits, gap = branch_and_bound_schedule_max_credits(courses)
    
    # Deve selecionar C2 (5 créditos) ao invés de C1
    assert len(selected) == 2
    assert any(c.id == "C2" for c in selected)
    assert credits == 8  # C2 (5) + C3 (3)


def test_bnb_schedule_min_gaps():
    """Testa Branch and Bound focado em minimizar gaps."""
    courses = [
        Course("C1", "Course 1", 8.0, 10.0, 4),
        Course("C2", "Course 2", 10.0, 12.0, 3),  # Sem gap após C1
        Course("C3", "Course 3", 15.0, 17.0, 5),  # Gap de 3h após C2
    ]
    
    selected, credits, gap = branch_and_bound_schedule_min_gaps(courses)
    
    # Deve minimizar gaps - seleciona apenas um curso (gap = 0)
    # ou seleciona C1 e C2 (gap = 0) ou C2 e C3 (gap = 3) etc.
    assert len(selected) >= 1
    # Se selecionar mais de um, deve ter o menor gap possível
    if len(selected) == 2:
        assert gap <= 3.0


def test_bnb_schedule_with_prerequisites():
    """Testa agendamento Branch and Bound respeitando pré-requisitos."""
    courses = [
        Course("C1", "Course 1", 8.0, 10.0, 4, prerequisites=["C0"]),
        Course("C2", "Course 2", 10.0, 12.0, 3),
        Course("C3", "Course 3", 14.0, 16.0, 5, prerequisites=[]),
    ]
    
    # C0 não foi concluído, então C1 não pode ser selecionado
    selected, credits, gap = branch_and_bound_schedule(courses, completed_course_ids=set())
    
    assert len(selected) == 2
    assert not any(c.id == "C1" for c in selected)
    assert any(c.id == "C2" for c in selected)
    assert any(c.id == "C3" for c in selected)


def test_bnb_schedule_with_completed_prerequisites():
    """Testa agendamento Branch and Bound com pré-requisitos já concluídos."""
    courses = [
        Course("C1", "Course 1", 8.0, 10.0, 4, prerequisites=["C0"]),
        Course("C2", "Course 2", 10.0, 12.0, 3),
        Course("C3", "Course 3", 14.0, 16.0, 5),
    ]
    
    # C0 já foi concluído
    selected, credits, gap = branch_and_bound_schedule(courses, completed_course_ids={"C0"})
    
    # Todos os cursos podem ser selecionados
    assert len(selected) == 3
    assert credits == 12


def test_bnb_schedule_empty():
    """Testa agendamento Branch and Bound com lista vazia."""
    selected, credits, gap = branch_and_bound_schedule([])
    
    assert len(selected) == 0
    assert credits == 0
    assert gap == 0.0


def test_bnb_schedule_with_info():
    """Testa versão com informações detalhadas."""
    courses = [
        Course("C1", "Course 1", 8.0, 10.0, 4),
        Course("C2", "Course 2", 10.0, 12.0, 3),
    ]
    
    result = branch_and_bound_schedule_with_info(courses)
    
    assert 'courses' in result
    assert 'total_credits' in result
    assert 'total_gap' in result
    assert 'num_courses' in result
    assert 'course_ids' in result
    
    assert result['num_courses'] == 2
    assert result['total_credits'] == 7


def test_bnb_schedule_optimal_solution():
    """Testa se Branch and Bound encontra solução ótima."""
    courses = [
        Course("C1", "Course 1", 8.0, 12.0, 2),
        Course("C2", "Course 2", 8.0, 10.0, 4),  # Melhor escolha
        Course("C3", "Course 3", 10.0, 12.0, 3),  # Compatível com C2
        Course("C4", "Course 4", 14.0, 16.0, 5),
    ]
    
    selected, credits, gap = branch_and_bound_schedule_max_credits(courses)
    
    # Solução ótima: C2 (4) + C3 (3) + C4 (5) = 12 créditos
    assert credits == 12
    assert len(selected) == 3


def test_bnb_schedule_all_conflicting():
    """Testa quando todos os cursos conflitam entre si."""
    courses = [
        Course("C1", "Course 1", 8.0, 12.0, 4),
        Course("C2", "Course 2", 9.0, 11.0, 3),
        Course("C3", "Course 3", 10.0, 14.0, 5),
    ]
    
    selected, credits, gap = branch_and_bound_schedule(courses)
    
    # Apenas um curso pode ser selecionado
    assert len(selected) == 1
    # Deve selecionar C3 (5 créditos - o maior)
    assert selected[0].id == "C3"
    assert gap == 0.0


def test_bnb_schedule_combined_objective():
    """Testa função objetivo combinada."""
    courses = [
        Course("C1", "Course 1", 8.0, 10.0, 4),
        Course("C2", "Course 2", 10.0, 12.0, 3),
        Course("C3", "Course 3", 14.0, 16.0, 5),
    ]
    
    # Com penalidade de gap
    selected, credits, gap = branch_and_bound_schedule(courses, gap_penalty=0.1)
    
    assert len(selected) == 3
    assert credits == 12
    # Objetivo: 12 - 0.1 * 2.0 = 11.8
