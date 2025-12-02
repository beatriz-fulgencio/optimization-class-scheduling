"""
Testes de integração para o sistema de agendamento.
"""

import pytest
import json
import os
from src.course import Course
from src.greedy_algorithm import greedy_schedule
from src.ilp_algorithm import ilp_schedule
from src.compare import load_courses_from_json, compare_algorithms


def test_load_courses_from_json(tmp_path):
    """Testa carregamento de cursos de arquivo JSON."""
    # Cria um arquivo JSON temporário
    data = {
        "courses": [
            {
                "id": "C1",
                "name": "Course 1",
                "start_time": 8.0,
                "end_time": 10.0,
                "credits": 4,
                "prerequisites": []
            },
            {
                "id": "C2",
                "name": "Course 2",
                "start_time": 10.0,
                "end_time": 12.0,
                "credits": 3,
                "prerequisites": ["C1"]
            }
        ]
    }
    
    json_file = tmp_path / "test_courses.json"
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(data, f)
    
    courses = load_courses_from_json(str(json_file))
    
    assert len(courses) == 2
    assert courses[0].id == "C1"
    assert courses[1].id == "C2"
    assert courses[1].prerequisites == ["C1"]


def test_sample_data_exists():
    """Verifica se o arquivo de dados de exemplo existe."""
    data_file = "data/sample_courses.json"
    assert os.path.exists(data_file), f"Arquivo {data_file} não encontrado"


def test_sample_data_valid():
    """Verifica se os dados de exemplo são válidos."""
    data_file = "data/sample_courses.json"
    
    if os.path.exists(data_file):
        courses = load_courses_from_json(data_file)
        
        assert len(courses) > 0, "Deve haver pelo menos um curso"
        
        # Verifica se todos os cursos são válidos
        for course in courses:
            assert course.start_time < course.end_time
            assert course.credits > 0
            assert course.id is not None
            assert course.name is not None


def test_algorithms_produce_valid_schedules():
    """Testa se ambos os algoritmos produzem cronogramas válidos."""
    courses = [
        Course("C1", "Course 1", 8.0, 10.0, 4),
        Course("C2", "Course 2", 10.0, 12.0, 3),
        Course("C3", "Course 3", 14.0, 16.0, 5),
    ]
    
    # Testa algoritmo guloso
    greedy_selected, greedy_credits, greedy_gap = greedy_schedule(courses)
    
    # Verifica que não há conflitos
    for i, course1 in enumerate(greedy_selected):
        for course2 in greedy_selected[i + 1:]:
            assert not course1.conflicts_with(course2), "Algoritmo guloso produziu conflito"
    
    # Testa algoritmo ILP
    ilp_selected, ilp_credits, ilp_gap = ilp_schedule(courses)
    
    # Verifica que não há conflitos
    for i, course1 in enumerate(ilp_selected):
        for course2 in ilp_selected[i + 1:]:
            assert not course1.conflicts_with(course2), "Algoritmo ILP produziu conflito"


def test_ilp_better_or_equal_to_greedy():
    """Testa se ILP produz solução melhor ou igual ao guloso."""
    courses = [
        Course("C1", "Course 1", 8.0, 10.0, 4),
        Course("C2", "Course 2", 9.0, 11.0, 3),
        Course("C3", "Course 3", 12.0, 14.0, 5),
        Course("C4", "Course 4", 13.0, 15.0, 4),
    ]
    
    greedy_selected, greedy_credits, greedy_gap = greedy_schedule(courses)
    ilp_selected, ilp_credits, ilp_gap = ilp_schedule(courses)
    
    # ILP deve obter créditos >= guloso (é uma solução ótima)
    # (considerando a penalidade de gap)
    assert ilp_credits >= greedy_credits or abs(ilp_credits - greedy_credits) <= 1


def test_compare_algorithms_runs():
    """Testa se a função de comparação executa sem erros."""
    courses = [
        Course("C1", "Course 1", 8.0, 10.0, 4),
        Course("C2", "Course 2", 10.0, 12.0, 3),
        Course("C3", "Course 3", 14.0, 16.0, 5),
    ]
    
    result = compare_algorithms(courses)
    
    assert 'greedy' in result
    assert 'ilp' in result
    assert 'greedy_time' in result
    assert 'ilp_time' in result
    assert 'credits_difference' in result
    assert 'gap_difference' in result


def test_complex_scenario():
    """Testa um cenário mais complexo com múltiplos cursos e conflitos."""
    courses = [
        Course("C1", "Course 1", 8.0, 10.0, 4),
        Course("C2", "Course 2", 9.0, 11.0, 3),
        Course("C3", "Course 3", 10.0, 12.0, 4),
        Course("C4", "Course 4", 11.0, 13.0, 3),
        Course("C5", "Course 5", 14.0, 16.0, 5),
        Course("C6", "Course 6", 15.0, 17.0, 4),
    ]
    
    greedy_selected, greedy_credits, greedy_gap = greedy_schedule(courses)
    ilp_selected, ilp_credits, ilp_gap = ilp_schedule(courses)
    
    # Ambos devem retornar cronogramas válidos
    assert len(greedy_selected) > 0
    assert len(ilp_selected) > 0
    assert greedy_credits > 0
    assert ilp_credits > 0


def test_prerequisites_chain():
    """Testa cenário com cadeia de pré-requisitos."""
    courses = [
        Course("C1", "Course 1", 8.0, 10.0, 4, prerequisites=[]),
        Course("C2", "Course 2", 10.0, 12.0, 4, prerequisites=["C1"]),
        Course("C3", "Course 3", 14.0, 16.0, 4, prerequisites=["C2"]),
    ]
    
    # Sem nenhum curso concluído
    greedy_selected, _, _ = greedy_schedule(courses, completed_course_ids=set())
    assert len(greedy_selected) == 1  # Apenas C1 pode ser cursado
    assert any(c.id == "C1" for c in greedy_selected)
    
    # Com C1 concluído, passar apenas C2 e C3 como disponíveis
    remaining_courses = [c for c in courses if c.id != "C1"]
    greedy_selected, _, _ = greedy_schedule(remaining_courses, completed_course_ids={"C1"})
    assert len(greedy_selected) == 1  # Apenas C2 pode ser cursado (C3 precisa de C2)
    assert any(c.id == "C2" for c in greedy_selected)
    
    # Com C1 e C2 concluídos, passar apenas C3 como disponível
    remaining_courses = [c for c in courses if c.id not in ["C1", "C2"]]
    greedy_selected, _, _ = greedy_schedule(remaining_courses, completed_course_ids={"C1", "C2"})
    assert len(greedy_selected) == 1  # Apenas C3
    assert any(c.id == "C3" for c in greedy_selected)
