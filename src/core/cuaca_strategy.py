# src/core/cuaca_strategy.py

from abc import ABC, abstractmethod
from typing import Dict
from .exceptions import CuacaTidakLayakError

class CuacaEvaluatorStrategy(ABC):
    @abstractmethod
    def evaluasi(self, parameter_cuaca: Dict[str, float]) -> bool:
        pass

class StrategiOptik(CuacaEvaluatorStrategy):
    def evaluasi(self, parameter_cuaca: Dict[str, float]) -> bool:
        tutupan_awan = parameter_cuaca.get('tutupan_awan', 100.0)
        
        if tutupan_awan > 30.0:
            raise CuacaTidakLayakError("Gagal evaluasi Optik: Tutupan awan terlalu tinggi.")
        return True

class StrategiRadio(CuacaEvaluatorStrategy):
    def evaluasi(self, parameter_cuaca: Dict[str, float]) -> bool:
        kelembaban = parameter_cuaca.get('kelembaban', 100.0)
        
        if kelembaban > 85.0:
            raise CuacaTidakLayakError("Gagal evaluasi Radio: Kelembaban udara ekstrem.")
        return True