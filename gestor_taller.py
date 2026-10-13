from services.mostrador import MostradorService
from models.taller_manager import TallerManager


def ejecutar_interfaz_mostrador():
    """Punto de entrada compatible con el sistema anterior."""
    manager = TallerManager()
    servicio = MostradorService(manager)
    servicio.ejecutar_menu()


if __name__ == "__main__":
    ejecutar_interfaz_mostrador()