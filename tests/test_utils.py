"""
Testes para as funções utilitárias.
"""

import pytest
from src.course import Course
from src.utils import (
    check_conflicts,
    has_conflicts,
    calculate_total_gap,
    calculate_total_credits,
    check_prerequisites,
    validate_schedule
)


def test_check_conflicts_no_conflicts():
    """Testa detecção de conflitos quando não há conflitos."""
    courses = [
        Course("C1", "Course 1", 8.0, 10.0, 4),
        Course("C2", "Course 2", 10.0, 12.0, 4),
        Course("C3", "Course 3", 14.0, 16.0, 4),
    ]
    
    conflicts = check_conflicts(courses)
    assert len(conflicts) == 0


def test_check_conflicts_with_conflicts():
    """Testa detecção de conflitos quando há conflitos."""
    courses = [
        Course("C1", "Course 1", 8.0, 10.0, 4),
        Course("C2", "Course 2", 9.0, 11.0, 4),
        Course("C3", "Course 3", 14.0, 16.0, 4),
    ]
    
    conflicts = check_conflicts(courses)
    assert len(conflicts) == 1
    assert (courses[0], courses[1]) in conflicts or (courses[1], courses[0]) in conflicts


def test_has_conflicts():
    """Testa verificação booleana de conflitos."""
    courses_no_conflict = [
        Course("C1", "Course 1", 8.0, 10.0, 4),
        Course("C2", "Course 2", 10.0, 12.0, 4),
    ]
    
    courses_with_conflict = [
        Course("C1", "Course 1", 8.0, 10.0, 4),
        Course("C2", "Course 2", 9.0, 11.0, 4),
    ]
    
    assert not has_conflicts(courses_no_conflict)
    assert has_conflicts(courses_with_conflict)


def test_calculate_total_gap():
    """Testa cálculo de gap total."""
    courses = [
        Course("C1", "Course 1", 8.0, 10.0, 4),
        Course("C2", "Course 2", 12.0, 14.0, 4),
        Course("C3", "Course 3", 15.0, 17.0, 4),
    ]
    
    # Gap de 2h (10-12) + 1h (14-15) = 3h
    total_gap = calculate_total_gap(courses)
    assert total_gap == 3.0


def test_calculate_total_gap_no_gap():
    """Testa cálculo de gap quando não há intervalos."""
    courses = [
        Course("C1", "Course 1", 8.0, 10.0, 4),
        Course("C2", "Course 2", 10.0, 12.0, 4),
        Course("C3", "Course 3", 12.0, 14.0, 4),
    ]
    
    total_gap = calculate_total_gap(courses)
    assert total_gap == 0.0


def test_calculate_total_gap_single_course():
    """Testa cálculo de gap com um único curso."""
    courses = [Course("C1", "Course 1", 8.0, 10.0, 4)]
    
    total_gap = calculate_total_gap(courses)
    assert total_gap == 0.0


def test_calculate_total_gap_empty():
    """Testa cálculo de gap com lista vazia."""
    total_gap = calculate_total_gap([])
    assert total_gap == 0.0


def test_calculate_total_gap_unordered():
    """Testa cálculo de gap com cursos desordenados."""
    courses = [
        Course("C3", "Course 3", 15.0, 17.0, 4),
        Course("C1", "Course 1", 8.0, 10.0, 4),
        Course("C2", "Course 2", 12.0, 14.0, 4),
    ]
    
    # Deve ordenar automaticamente
    total_gap = calculate_total_gap(courses)
    assert total_gap == 3.0


def test_calculate_total_credits():
    """Testa cálculo de créditos totais."""
    courses = [
        Course("C1", "Course 1", 8.0, 10.0, 4),
        Course("C2", "Course 2", 10.0, 12.0, 3),
        Course("C3", "Course 3", 14.0, 16.0, 5),
    ]
    
    total_credits = calculate_total_credits(courses)
    assert total_credits == 12


def test_calculate_total_credits_empty():
    """Testa cálculo de créditos com lista vazia."""
    total_credits = calculate_total_credits([])
    assert total_credits == 0


def test_check_prerequisites_satisfied():
    """Testa verificação de pré-requisitos satisfeitos."""
    courses = [
        Course("C2", "Course 2", 10.0, 12.0, 4, prerequisites=["C1"]),
        Course("C3", "Course 3", 14.0, 16.0, 4, prerequisites=["C1", "C2"]),
    ]
    
    available = {"C1", "C2", "C3"}
    assert check_prerequisites(courses, available)


def test_check_prerequisites_not_satisfied():
    """Testa verificação de pré-requisitos não satisfeitos."""
    courses = [
        Course("C2", "Course 2", 10.0, 12.0, 4, prerequisites=["C1"]),
        Course("C3", "Course 3", 14.0, 16.0, 4, prerequisites=["C1", "C2"]),
    ]
    
    available = {"C1"}  # C2 não está disponível
    assert not check_prerequisites(courses, available)


def test_check_prerequisites_no_prerequisites():
    """Testa verificação quando não há pré-requisitos."""
    courses = [
        Course("C1", "Course 1", 8.0, 10.0, 4),
        Course("C2", "Course 2", 10.0, 12.0, 4),
    ]
    
    available = set()
    assert check_prerequisites(courses, available)


def test_validate_schedule_valid():
    """Testa validação de cronograma válido."""
    courses = [
        Course("C1", "Course 1", 8.0, 10.0, 4),
        Course("C2", "Course 2", 10.0, 12.0, 4),
    ]
    
    is_valid, message = validate_schedule(courses)
    assert is_valid
    assert "válido" in message


def test_validate_schedule_conflicts():
    """Testa validação de cronograma com conflitos."""
    courses = [
        Course("C1", "Course 1", 8.0, 10.0, 4),
        Course("C2", "Course 2", 9.0, 11.0, 4),
    ]
    
    is_valid, message = validate_schedule(courses)
    assert not is_valid
    assert "Conflitos" in message


def test_validate_schedule_prerequisites():
    """Testa validação de cronograma com pré-requisitos não satisfeitos."""
    courses = [
        Course("C2", "Course 2", 10.0, 12.0, 4, prerequisites=["C1"]),
    ]
    
    is_valid, message = validate_schedule(courses, completed_course_ids=set())
    assert not is_valid
    assert "Pré-requisitos" in message


def test_validate_schedule_prerequisites_with_completed():
    """Testa validação com pré-requisitos satisfeitos por cursos concluídos."""
    courses = [
        Course("C2", "Course 2", 10.0, 12.0, 4, prerequisites=["C1"]),
    ]
    
    is_valid, message = validate_schedule(courses, completed_course_ids={"C1"})
    assert is_valid
    assert "válido" in message
