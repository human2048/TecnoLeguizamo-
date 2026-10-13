from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import List, Optional

from .reparacion import Reparacion


class TallerManager:
    """Gestor central de persistencia y lógica del negocio del taller."""

    def __init__(self, db_path: Optional[str | Path] = None) -> None:
        base_dir = Path(__file__).resolve().parents[1]
        self.db_path = Path(db_path) if db_path else base_dir / "data" / "taller.db"
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._inicializar_bd()

    def _conectar(self) -> sqlite3.Connection:
        conn = sqlite3.connect(str(self.db_path), timeout=5.0)
        conn.row_factory = sqlite3.Row
        return conn

    def _inicializar_bd(self) -> None:
        with self._conectar() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS reparaciones (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    cliente TEXT NOT NULL,
                    tipo_equipo TEXT NOT NULL,
                    modelo TEXT NOT NULL,
                    falla TEXT NOT NULL,
                    estado TEXT NOT NULL,
                    fecha TEXT NOT NULL
                )
                """
            )
            conn.commit()

    def registrar_equipo(self, reparacion: Reparacion) -> Reparacion:
        if not isinstance(reparacion, Reparacion):
            raise TypeError("Se esperaba una instancia de Reparacion.")
        if not reparacion.es_valido():
            raise ValueError("Todos los campos obligatorios deben estar completos.")

        with self._conectar() as conn:
            cursor = conn.execute(
                """
                INSERT INTO reparaciones (cliente, tipo_equipo, modelo, falla, estado, fecha)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                reparacion.tupla_para_bd(),
            )
            reparacion.id = cursor.lastrowid
            conn.commit()

        return reparacion

    def listar_equipos(self) -> List[Reparacion]:
        with self._conectar() as conn:
            filas = conn.execute(
                "SELECT id, cliente, tipo_equipo, modelo, falla, estado, fecha FROM reparaciones ORDER BY id DESC"
            ).fetchall()

        return [Reparacion.desde_fila(tuple(fila)) for fila in filas]

    def buscar_equipos(self, filtro: str) -> List[Reparacion]:
        texto = (filtro or "").strip()
        if not texto:
            return self.listar_equipos()

        patron = f"%{texto}%"
        with self._conectar() as conn:
            filas = conn.execute(
                """
                SELECT id, cliente, tipo_equipo, modelo, falla, estado, fecha
                FROM reparaciones
                WHERE cliente LIKE ? OR tipo_equipo LIKE ? OR modelo LIKE ? OR falla LIKE ?
                ORDER BY id DESC
                """,
                (patron, patron, patron, patron),
            ).fetchall()

        return [Reparacion.desde_fila(tuple(fila)) for fila in filas]

    def obtener_por_id(self, equipo_id: int) -> Optional[Reparacion]:
        with self._conectar() as conn:
            fila = conn.execute(
                "SELECT id, cliente, tipo_equipo, modelo, falla, estado, fecha FROM reparaciones WHERE id = ?",
                (equipo_id,),
            ).fetchone()

        if fila is None:
            return None
        return Reparacion.desde_fila(tuple(fila))

    def actualizar_estado(self, equipo_id: int, nuevo_estado: str) -> bool:
        estado = (nuevo_estado or "").strip()
        if not estado:
            raise ValueError("El nuevo estado no puede estar vacío.")

        with self._conectar() as conn:
            cursor = conn.execute(
                "UPDATE reparaciones SET estado = ? WHERE id = ?",
                (estado, equipo_id),
            )
            conn.commit()
        return cursor.rowcount > 0
