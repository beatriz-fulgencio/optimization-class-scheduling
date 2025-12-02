"""
Modelo de curso acadêmico para otimização de agendamento.

Este módulo define a estrutura de dados para representar cursos acadêmicos
com seus horários, créditos e pré-requisitos.
"""

from dataclasses import dataclass
from typing import List, Optional


@dataclass
class Course:
    """
    Representa um curso acadêmico com informações de agendamento.
    
    Attributes:
        id: Identificador único do curso
        name: Nome do curso
        start_time: Horário de início (em horas, ex: 8.0 para 8h00)
        end_time: Horário de término (em horas, ex: 10.0 para 10h00)
        credits: Número de créditos do curso
        prerequisites: Lista de IDs de cursos que são pré-requisitos
    """
    id: str
    name: str
    start_time: float
    end_time: float
    credits: int
    prerequisites: Optional[List[str]] = None
    
    def __post_init__(self) -> None:
        """Valida os dados do curso após inicialização."""
        if self.start_time >= self.end_time:
            raise ValueError(f"Horário de início ({self.start_time}) deve ser anterior ao término ({self.end_time})")
        if self.credits <= 0:
            raise ValueError(f"Créditos devem ser positivos, recebido: {self.credits}")
        if self.prerequisites is None:
            self.prerequisites = []
    
    def duration(self) -> float:
        """
        Calcula a duração do curso em horas.
        
        Returns:
            Duração do curso em horas
        """
        return self.end_time - self.start_time
    
    def conflicts_with(self, other: 'Course') -> bool:
        """
        Verifica se este curso tem conflito de horário com outro curso.
        
        Args:
            other: Outro curso para verificar conflito
            
        Returns:
            True se há conflito de horário, False caso contrário
        """
        # Verifica se há sobreposição de intervalos
        return not (self.end_time <= other.start_time or self.start_time >= other.end_time)
    
    def gap_to(self, other: 'Course') -> float:
        """
        Calcula o intervalo (gap) entre o fim deste curso e o início de outro.
        
        Se o outro curso começa antes deste terminar, retorna 0.
        
        Args:
            other: Curso seguinte
            
        Returns:
            Intervalo em horas entre os cursos
        """
        if other.start_time < self.end_time:
            return 0.0
        return other.start_time - self.end_time
    
    def __repr__(self) -> str:
        """Representação em string do curso."""
        return f"Course(id='{self.id}', name='{self.name}', {self.start_time}-{self.end_time}, {self.credits} créditos)"
