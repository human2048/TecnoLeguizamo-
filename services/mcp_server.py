from __future__ import annotations

import json
import sys

from models.taller_manager import TallerManager

manager = TallerManager()


def responder(peticion: dict) -> dict:
    metodo = peticion.get("method")
    msg_id = peticion.get("id")

    if metodo == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": msg_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "tecno-mcp-server", "version": "1.0"},
            },
        }

    if metodo == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": msg_id,
            "result": {
                "tools": [
                    {
                        "name": "consultar_taller",
                        "description": "Consulta equipos del taller o filtra por texto.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "filtro": {"type": "string", "description": "Texto opcional para buscar por cliente, modelo, equipo o falla."}
                            },
                        },
                    }
                ]
            },
        }

    if metodo == "tools/call":
        params = peticion.get("params", {})
        nombre_herramienta = params.get("name")
        argumentos = params.get("arguments", {})

        if nombre_herramienta == "consultar_taller":
            filtro = (argumentos.get("filtro") or "").strip()
            equipos = manager.buscar_equipos(filtro)
            texto_resultado = "Registros encontrados en Tecnolegísamo:\n" + str([
                (equipo.id, equipo.cliente, equipo.tipo_equipo, equipo.modelo, equipo.falla, equipo.estado, equipo.fecha)
                for equipo in equipos
            ])
            return {
                "jsonrpc": "2.0",
                "id": msg_id,
                "result": {"content": [{"type": "text", "text": texto_resultado}]},
            }

        return {
            "jsonrpc": "2.0",
            "id": msg_id,
            "error": {"code": -32601, "message": "Herramienta no encontrada"},
        }

    return {
        "jsonrpc": "2.0",
        "id": msg_id,
        "error": {"code": -32603, "message": "Método no soportado"},
    }


def main() -> None:
    for linea in sys.stdin:
        try:
            peticion = json.loads(linea)
            respuesta = responder(peticion)
        except Exception:
            respuesta = {
                "jsonrpc": "2.0",
                "id": None,
                "error": {"code": -32700, "message": "Solicitud inválida"},
            }
        sys.stdout.write(json.dumps(respuesta) + "\n")
        sys.stdout.flush()


if __name__ == "__main__":
    main()
