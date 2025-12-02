"""
Testes para o modelo de curso.
"""

import pytest
from src.course import Course


def test_course_creation():
    """Testa criação básica de um curso."""
    course = Course(
        id="MAT101",
        name="Cálculo I",
        start_time=8.0,
        end_time=10.0,
        credits=4
    )
    
    assert course.id == "MAT101"
    assert course.name == "Cálculo I"
    assert course.start_time == 8.0
    assert course.end_time == 10.0
    assert course.credits == 4
    assert course.prerequisites == []


def test_course_with_prerequisites():
    """Testa criação de curso com pré-requisitos."""
    course = Course(
        id="MAT102",
        name="Cálculo II",
        start_time=8.0,
        end_time=10.0,
        credits=4,
        prerequisites=["MAT101"]
    )
    
    assert course.prerequisites == ["MAT101"]


def test_course_invalid_time():
    """Testa validação de horários inválidos."""
    with pytest.raises(ValueError, match="Horário de início"):
        Course(
            id="TEST",
            name="Test",
            start_time=10.0,
            end_time=8.0,
            credits=4
        )


def test_course_invalid_credits():
    """Testa validação de créditos inválidos."""
    with pytest.raises(ValueError, match="Créditos devem ser positivos"):
        Course(
            id="TEST",
            name="Test",
            start_time=8.0,
            end_time=10.0,
            credits=0
        )


def test_course_duration():
    """Testa cálculo de duração do curso."""
    course = Course(
        id="TEST",
        name="Test",
        start_time=8.0,
        end_time=11.0,
        credits=4
    )
    
    assert course.duration() == 3.0


def test_course_conflicts():
    """Testa detecção de conflitos entre cursos."""
    course1 = Course("C1", "Course 1", 8.0, 10.0, 4)
    course2 = Course("C2", "Course 2", 9.0, 11.0, 4)
    course3 = Course("C3", "Course 3", 10.0, 12.0, 4)
    course4 = Course("C4", "Course 4", 14.0, 16.0, 4)
    
    # course1 e course2 se sobrepõem
    assert course1.conflicts_with(course2)
    assert course2.conflicts_with(course1)
    
    # course1 termina quando course3 começa (não conflita)
    assert not course1.conflicts_with(course3)
    assert not course3.conflicts_with(course1)
    
    # course1 e course4 não se sobrepõem
    assert not course1.conflicts_with(course4)
    assert not course4.conflicts_with(course1)


def test_course_gap():
    """Testa cálculo de intervalo entre cursos."""
    course1 = Course("C1", "Course 1", 8.0, 10.0, 4)
    course2 = Course("C2", "Course 2", 12.0, 14.0, 4)
    course3 = Course("C3", "Course 3", 10.0, 12.0, 4)
    
    # Gap de 2 horas entre course1 e course2
    assert course1.gap_to(course2) == 2.0
    
    # Sem gap entre course1 e course3
    assert course1.gap_to(course3) == 0.0
    
    # Gap negativo (course2 começa antes de course1 terminar) retorna 0
    assert course2.gap_to(course1) == 0.0


def test_course_repr():
    """Testa representação em string do curso."""
    course = Course("MAT101", "Cálculo I", 8.0, 10.0, 4)
    repr_str = repr(course)
    
    assert "MAT101" in repr_str
    assert "Cálculo I" in repr_str
    assert "8.0" in repr_str
    assert "10.0" in repr_str
    assert "4" in repr_str
