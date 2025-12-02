"""
Testes para o algoritmo guloso.
"""

import pytest
from src.course import Course
from src.greedy_algorithm import greedy_schedule, greedy_schedule_with_info


def test_greedy_schedule_no_conflicts():
    """Testa agendamento guloso sem conflitos."""
    courses = [
        Course("C1", "Course 1", 8.0, 10.0, 4),
        Course("C2", "Course 2", 10.0, 12.0, 3),
        Course("C3", "Course 3", 14.0, 16.0, 5),
    ]
    
    selected, credits, gap = greedy_schedule(courses)
    
    # Todos os cursos devem ser selecionados (sem conflitos)
    assert len(selected) == 3
    assert credits == 12
    assert gap == 2.0  # Gap entre C2 (12h) e C3 (14h)


def test_greedy_schedule_with_conflicts():
    """Testa agendamento guloso com conflitos."""
    courses = [
        Course("C1", "Course 1", 8.0, 10.0, 4),
        Course("C2", "Course 2", 9.0, 11.0, 3),
        Course("C3", "Course 3", 14.0, 16.0, 5),
    ]
    
    selected, credits, gap = greedy_schedule(courses)
    
    # C1 e C2 conflitam, o algoritmo deve escolher o melhor
    assert len(selected) == 2
    # Deve incluir C3 (5 créditos)
    assert any(c.id == "C3" for c in selected)


def test_greedy_schedule_ordering():
    """Testa se o algoritmo guloso ordena corretamente por end_time/credits."""
    courses = [
        Course("C1", "Course 1", 8.0, 12.0, 2),  # ratio: 12/2 = 6.0
        Course("C2", "Course 2", 8.0, 10.0, 4),  # ratio: 10/4 = 2.5 (melhor)
        Course("C3", "Course 3", 14.0, 16.0, 3),  # ratio: 16/3 = 5.33
    ]
    
    selected, credits, gap = greedy_schedule(courses)
    
    # C2 deve ser selecionado primeiro (menor ratio)
    # C1 e C2 conflitam, então apenas C2 e C3 devem ser selecionados
    assert len(selected) == 2
    assert any(c.id == "C2" for c in selected)
    assert any(c.id == "C3" for c in selected)


def test_greedy_schedule_with_prerequisites():
    """Testa agendamento guloso respeitando pré-requisitos."""
    courses = [
        Course("C1", "Course 1", 8.0, 10.0, 4, prerequisites=["C0"]),
        Course("C2", "Course 2", 10.0, 12.0, 3),
        Course("C3", "Course 3", 14.0, 16.0, 5, prerequisites=[]),
    ]
    
    # C0 não foi concluído, então C1 não pode ser selecionado
    selected, credits, gap = greedy_schedule(courses, completed_course_ids=set())
    
    assert len(selected) == 2
    assert not any(c.id == "C1" for c in selected)
    assert any(c.id == "C2" for c in selected)
    assert any(c.id == "C3" for c in selected)


def test_greedy_schedule_with_completed_prerequisites():
    """Testa agendamento guloso com pré-requisitos já concluídos."""
    courses = [
        Course("C1", "Course 1", 8.0, 10.0, 4, prerequisites=["C0"]),
        Course("C2", "Course 2", 10.0, 12.0, 3),
        Course("C3", "Course 3", 14.0, 16.0, 5),
    ]
    
    # C0 já foi concluído
    selected, credits, gap = greedy_schedule(courses, completed_course_ids={"C0"})
    
    # Todos os cursos podem ser selecionados
    assert len(selected) == 3
    assert credits == 12


def test_greedy_schedule_empty():
    """Testa agendamento guloso com lista vazia."""
    selected, credits, gap = greedy_schedule([])
    
    assert len(selected) == 0
    assert credits == 0
    assert gap == 0.0


def test_greedy_schedule_with_info():
    """Testa versão com informações detalhadas."""
    courses = [
        Course("C1", "Course 1", 8.0, 10.0, 4),
        Course("C2", "Course 2", 10.0, 12.0, 3),
    ]
    
    result = greedy_schedule_with_info(courses)
    
    assert 'courses' in result
    assert 'total_credits' in result
    assert 'total_gap' in result
    assert 'num_courses' in result
    assert 'course_ids' in result
    
    assert result['num_courses'] == 2
    assert result['total_credits'] == 7
    assert result['course_ids'] == ['C1', 'C2'] or result['course_ids'] == ['C2', 'C1']


def test_greedy_schedule_maximize_credits():
    """Testa se o algoritmo maximiza créditos adequadamente."""
    courses = [
        Course("C1", "Course 1", 8.0, 10.0, 2),
        Course("C2", "Course 2", 8.0, 10.0, 5),  # Mesmo horário, mais créditos
        Course("C3", "Course 3", 14.0, 16.0, 3),
    ]
    
    selected, credits, gap = greedy_schedule(courses)
    
    # Deve selecionar C2 (5 créditos, melhor ratio) ao invés de C1
    assert len(selected) == 2
    assert any(c.id == "C2" for c in selected)
    assert credits >= 8


def test_greedy_schedule_all_conflicting():
    """Testa quando todos os cursos conflitam entre si."""
    courses = [
        Course("C1", "Course 1", 8.0, 12.0, 4),
        Course("C2", "Course 2", 9.0, 11.0, 3),
        Course("C3", "Course 3", 10.0, 14.0, 5),
    ]
    
    selected, credits, gap = greedy_schedule(courses)
    
    # Apenas um curso pode ser selecionado
    assert len(selected) == 1
    # O gap deve ser 0 (apenas um curso)
    assert gap == 0.0
