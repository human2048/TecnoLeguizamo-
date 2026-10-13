from __future__ import annotations

from typing import Optional

from models.reparacion import Reparacion
from models.taller_manager import TallerManager


class MostradorService:
    """Servicio interactivo para atención rápida en mostrador."""

    def __init__(self, manager: TallerManager) -> None:
        self.manager = manager

    @staticmethod
    def _mostrar_encabezado() -> None:
        print("\n==============================================")
        print("   🛠️  SISTEMA DE GESTIÓN TECNOLEGÍSAMO (POO)   ")
        print("==============================================")

    @staticmethod
    def _leer_texto(mensaje: str, obligatorio: bool = True) -> str:
        valor = input(mensaje).strip()
        if obligatorio and not valor:
            raise ValueError("Este campo es obligatorio.")
        return valor

    def registrar_nuevo_equipo(self) -> Optional[Reparacion]:
        try:
            cliente = self._leer_texto("Nombre del cliente: ")
            tipo_equipo = self._leer_texto("Tipo de equipo: ")
            modelo = self._leer_texto("Marca y modelo: ")
            falla = self._leer_texto("Descripción de la falla: ")

            reparacion = Reparacion(
                cliente=cliente,
                tipo_equipo=tipo_equipo,
                modelo=modelo,
                falla=falla,
                estado="Ingresado",
            )

            if not reparacion.es_valido():
                raise ValueError("Los datos del equipo no son válidos.")

            guardada = self.manager.registrar_equipo(reparacion)
            print(f"\n[ÉXITO] Equipo registrado: {guardada.cliente} | {guardada.tipo_equipo} | {guardada.modelo}")
            return guardada
        except ValueError as exc:
            print(f"\n[ADVERTENCIA] {exc}")
            return None
        except Exception as exc:
            print(f"\n[ERROR] No se pudo registrar el equipo: {exc}")
            return None

    def listar_registros(self) -> None:
        equipos = self.manager.listar_equipos()
        if not equipos:
            print("No hay equipos registrados todavía.")
            return

        for equipo in equipos:
            print(
                f"ID: {equipo.id} | Cliente: {equipo.cliente} | "
                f"[{equipo.tipo_equipo}] {equipo.modelo} | "
                f"Falla: {equipo.falla} | Estado: {equipo.estado} | Fecha: {equipo.fecha}"
            )

    def ejecutar_menu(self) -> None:
        while True:
            self._mostrar_encabezado()
            print("1. Registrar nuevo equipo (Ingreso rápido)")
            print("2. Listar equipos en taller")
            print("3. Buscar por texto")
            print("4. Salir")

            opcion = input("\nSeleccione una opción (1-4): ").strip()

            try:
                if opcion == "1":
                    print("\n--- NUEVO INGRESO ---")
                    self.registrar_nuevo_equipo()
                    input("\nPresione Enter para continuar...")
                elif opcion == "2":
                    print("\n--- REGISTROS EN EL TALLER ---")
                    self.listar_registros()
                    input("\nPresione Enter para continuar...")
                elif opcion == "3":
                    texto = input("Ingrese texto a buscar (cliente, equipo, modelo o falla): ").strip()
                    equipos = self.manager.buscar_equipos(texto)
                    if not equipos:
                        print("No se encontraron coincidencias.")
                    else:
                        for equipo in equipos:
                            print(
                                f"ID: {equipo.id} | Cliente: {equipo.cliente} | "
                                f"[{equipo.tipo_equipo}] {equipo.modelo} | "
                                f"Falla: {equipo.falla} | Estado: {equipo.estado}"
                            )
                    input("\nPresione Enter para continuar...")
                elif opcion == "4":
                    print("\nSaliendo del sistema... ¡Buen trabajo!")
                    break
                else:
                    print("\n[AVISO] Opción no válida. Intente nuevamente.")
                    input("\nPresione Enter para continuar...")
            except Exception as exc:
                print(f"\n[ERROR] {exc}")
                input("\nPresione Enter para continuar...")
