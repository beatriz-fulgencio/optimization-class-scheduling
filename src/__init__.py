"""
Pacote de otimização de agendamento de cursos acadêmicos.

Este pacote fornece algoritmos para resolver o problema de agendamento
ponderado de intervalos (Weighted Interval Scheduling) no contexto acadêmico.
"""

from src.course import Course
from src.greedy_algorithm import greedy_schedule, greedy_schedule_with_info
from src.ilp_algorithm import ilp_schedule, ilp_schedule_with_info
from src.utils import (
    check_conflicts,
    has_conflicts,
    calculate_total_gap,
    calculate_total_credits,
    check_prerequisites,
    validate_schedule
)

__all__ = [
    'Course',
    'greedy_schedule',
    'greedy_schedule_with_info',
    'ilp_schedule',
    'ilp_schedule_with_info',
    'check_conflicts',
    'has_conflicts',
    'calculate_total_gap',
    'calculate_total_credits',
    'check_prerequisites',
    'validate_schedule',
]
