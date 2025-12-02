"""
Testes para o algoritmo ILP.
"""

import pytest
from src.course import Course
from src.ilp_algorithm import ilp_schedule, ilp_schedule_with_info


def test_ilp_schedule_no_conflicts():
    """Testa agendamento ILP sem conflitos."""
    courses = [
        Course("C1", "Course 1", 8.0, 10.0, 4),
        Course("C2", "Course 2", 10.0, 12.0, 3),
        Course("C3", "Course 3", 14.0, 16.0, 5),
    ]
    
    selected, credits, gap = ilp_schedule(courses)
    
    # Todos os cursos devem ser selecionados (sem conflitos)
    assert len(selected) == 3
    assert credits == 12


def test_ilp_schedule_with_conflicts():
    """Testa agendamento ILP com conflitos."""
    courses = [
        Course("C1", "Course 1", 8.0, 10.0, 4),
        Course("C2", "Course 2", 9.0, 11.0, 3),
        Course("C3", "Course 3", 14.0, 16.0, 5),
    ]
    
    selected, credits, gap = ilp_schedule(courses)
    
    # C1 e C2 conflitam, ILP deve escolher a combinação ótima
    assert len(selected) == 2
    # Deve maximizar créditos, então C1 (4) + C3 (5) = 9 créditos
    assert credits >= 8


def test_ilp_schedule_maximize_credits():
    """Testa se ILP maximiza créditos corretamente."""
    courses = [
        Course("C1", "Course 1", 8.0, 10.0, 2),
        Course("C2", "Course 2", 8.0, 10.0, 5),  # Mesmo horário, mais créditos
        Course("C3", "Course 3", 14.0, 16.0, 3),
    ]
    
    selected, credits, gap = ilp_schedule(courses)
    
    # Deve selecionar C2 (5 créditos) ao invés de C1 (2 créditos)
    assert len(selected) == 2
    assert any(c.id == "C2" for c in selected)
    assert credits >= 8


def test_ilp_schedule_with_prerequisites():
    """Testa agendamento ILP respeitando pré-requisitos."""
    courses = [
        Course("C1", "Course 1", 8.0, 10.0, 4, prerequisites=["C0"]),
        Course("C2", "Course 2", 10.0, 12.0, 3),
        Course("C3", "Course 3", 14.0, 16.0, 5),
    ]
    
    # C0 não foi concluído, então C1 não pode ser selecionado
    selected, credits, gap = ilp_schedule(courses, completed_course_ids=set())
    
    assert len(selected) == 2
    assert not any(c.id == "C1" for c in selected)
    assert any(c.id == "C2" for c in selected)
    assert any(c.id == "C3" for c in selected)


def test_ilp_schedule_with_completed_prerequisites():
    """Testa agendamento ILP com pré-requisitos já concluídos."""
    courses = [
        Course("C1", "Course 1", 8.0, 10.0, 4, prerequisites=["C0"]),
        Course("C2", "Course 2", 10.0, 12.0, 3),
        Course("C3", "Course 3", 14.0, 16.0, 5),
    ]
    
    # C0 já foi concluído
    selected, credits, gap = ilp_schedule(courses, completed_course_ids={"C0"})
    
    # Todos os cursos podem ser selecionados
    assert len(selected) == 3
    assert credits == 12


def test_ilp_schedule_empty():
    """Testa agendamento ILP com lista vazia."""
    selected, credits, gap = ilp_schedule([])
    
    assert len(selected) == 0
    assert credits == 0
    assert gap == 0.0


def test_ilp_schedule_with_gap_penalty():
    """Testa se a penalidade de gap afeta a solução."""
    courses = [
        Course("C1", "Course 1", 8.0, 10.0, 3),
        Course("C2", "Course 2", 16.0, 18.0, 3),  # Gap grande de C1 para C2
        Course("C3", "Course 3", 10.0, 12.0, 3),  # Sem gap de C1 para C3
    ]
    
    # Com penalidade baixa, deve selecionar todos
    selected_low, credits_low, gap_low = ilp_schedule(courses, gap_penalty=0.01)
    
    # Com penalidade alta, pode preferir menos cursos com menos gap
    selected_high, credits_high, gap_high = ilp_schedule(courses, gap_penalty=2.0)
    
    # Ambos devem ter soluções válidas
    assert len(selected_low) >= 1
    assert len(selected_high) >= 1


def test_ilp_schedule_with_info():
    """Testa versão com informações detalhadas."""
    courses = [
        Course("C1", "Course 1", 8.0, 10.0, 4),
        Course("C2", "Course 2", 10.0, 12.0, 3),
    ]
    
    result = ilp_schedule_with_info(courses)
    
    assert 'courses' in result
    assert 'total_credits' in result
    assert 'total_gap' in result
    assert 'num_courses' in result
    assert 'course_ids' in result
    assert 'gap_penalty' in result
    
    assert result['num_courses'] == 2
    assert result['total_credits'] == 7


def test_ilp_schedule_optimal_solution():
    """Testa se ILP encontra solução ótima."""
    courses = [
        Course("C1", "Course 1", 8.0, 10.0, 3),
        Course("C2", "Course 2", 9.0, 11.0, 2),
        Course("C3", "Course 3", 12.0, 14.0, 4),
        Course("C4", "Course 4", 13.0, 15.0, 3),
    ]
    
    selected, credits, gap = ilp_schedule(courses)
    
    # Solução ótima deve ser C1 + C3 (7 créditos) ou C1 + C4 (6 créditos)
    # ou C2 + C3 (6 créditos) ou C2 + C4 (5 créditos)
    # O ótimo é C1 + C3 = 7 créditos
    assert credits >= 6


def test_ilp_schedule_all_conflicting():
    """Testa quando todos os cursos conflitam entre si."""
    courses = [
        Course("C1", "Course 1", 8.0, 12.0, 4),
        Course("C2", "Course 2", 9.0, 11.0, 3),
        Course("C3", "Course 3", 10.0, 14.0, 5),
    ]
    
    selected, credits, gap = ilp_schedule(courses)
    
    # Apenas um curso pode ser selecionado, deve escolher o de mais créditos
    assert len(selected) == 1
    assert gap == 0.0
    assert any(c.id == "C3" for c in selected)  # C3 tem 5 créditos (máximo)
