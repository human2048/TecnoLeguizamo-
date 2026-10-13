from __future__ import annotations

import argparse

from models.reparacion import Reparacion
from models.taller_manager import TallerManager
from services.mostrador import MostradorService


def construir_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Sistema de gestión del taller Tecnolegísamo")
    parser.add_argument("--cliente", type=str, help="Nombre del cliente")
    parser.add_argument("--tipo", type=str, help="Tipo de equipo (ej. Celular, Televisor, Parlante, PC/Portatil)")
    parser.add_argument("--modelo", type=str, help="Marca y modelo")
    parser.add_argument("--falla", type=str, help="Descripción de la falla")
    parser.add_argument("--estado", type=str, default="Ingresado", help="Estado del equipo")
    parser.add_argument("--listar", action="store_true", help="Lista todos los equipos")
    parser.add_argument("--buscar", type=str, help="Busca equipos por texto")
    return parser


def main() -> None:
    args = construir_parser().parse_args()
    manager = TallerManager()

    if args.listar:
        equipos = manager.listar_equipos()
        if not equipos:
            print("No hay equipos registrados todavía.")
            return
        for equipo in equipos:
            print(
                f"ID: {equipo.id} | Cliente: {equipo.cliente} | "
                f"[{equipo.tipo_equipo}] {equipo.modelo} | "
                f"Falla: {equipo.falla} | Estado: {equipo.estado} | Fecha: {equipo.fecha}"
            )
        return

    if args.buscar:
        resultados = manager.buscar_equipos(args.buscar)
        if not resultados:
            print("No se encontraron coincidencias.")
            return
        for equipo in resultados:
            print(
                f"ID: {equipo.id} | Cliente: {equipo.cliente} | "
                f"[{equipo.tipo_equipo}] {equipo.modelo} | "
                f"Falla: {equipo.falla} | Estado: {equipo.estado}"
            )
        return

    if args.cliente and args.tipo and args.modelo and args.falla:
        reparacion = Reparacion(
            cliente=args.cliente,
            tipo_equipo=args.tipo,
            modelo=args.modelo,
            falla=args.falla,
            estado=args.estado,
        )
        try:
            guardada = manager.registrar_equipo(reparacion)
            print(f"[ÉXITO] Equipo registrado con ID {guardada.id}.")
        except (TypeError, ValueError) as exc:
            print(f"[ERROR] {exc}")
        return

    MostradorService(manager).ejecutar_menu()


if __name__ == "__main__":
    main()
