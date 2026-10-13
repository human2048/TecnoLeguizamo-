from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class Reparacion:
    cliente: str
    tipo_equipo: str
    modelo: str
    falla: str
    estado: str = "Ingresado"
    fecha: str = field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    id: Optional[int] = None

    def __post_init__(self) -> None:
        self.cliente = self._normalizar(self.cliente)
        self.tipo_equipo = self._normalizar(self.tipo_equipo)
        self.modelo = self._normalizar(self.modelo)
        self.falla = self._normalizar(self.falla)
        self.estado = self._normalizar(self.estado) or "Ingresado"
        if not self.fecha:
            self.fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    @staticmethod
    def _normalizar(valor: Optional[str]) -> str:
        if valor is None:
            return ""
        return str(valor).strip()

    def es_valido(self) -> bool:
        return bool(self.cliente and self.tipo_equipo and self.modelo and self.falla)

    @classmethod
    def desde_fila(cls, fila: tuple) -> "Reparacion":
        if len(fila) < 7:
            raise ValueError("La fila de base de datos no tiene la estructura esperada.")
        id_registro, cliente, tipo_equipo, modelo, falla, estado, fecha = fila
        return cls(
            cliente=cliente,
            tipo_equipo=tipo_equipo,
            modelo=modelo,
            falla=falla,
            estado=estado,
            fecha=fecha,
            id=id_registro,
        )

    def tupla_para_bd(self) -> tuple:
        return (self.cliente, self.tipo_equipo, self.modelo, self.falla, self.estado, self.fecha)
