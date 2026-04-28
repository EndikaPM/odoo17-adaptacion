"""
Servicio helper para consumir la API de ausencias
Este módulo proporciona utilidades para interactuar con la API desde Odoo o Python
"""

import requests
import json
from datetime import datetime
from typing import Dict, List, Optional


class AusenciasAPIClient:
    """Cliente para consumir la API de ausencias"""

    def __init__(self, base_url: str = "http://localhost:8069"):
        """
        Inicializa el cliente

        Args:
            base_url: URL base del servidor Odoo
        """
        self.base_url = base_url.rstrip('/')
        self.timeout = 10

    def obtain_tipo_motivo_options(self) -> Dict:
        """
        Obtiene las opciones disponibles para tipo_motivo

        Returns:
            Diccionario con success y data

        Ejemplo:
            {
                "success": True,
                "data": [
                    {"value": "VACACIONES", "label": "Vacaciones"},
                    ...
                ]
            }
        """
        try:
            response = requests.get(
                f"{self.base_url}/api/ausencias/opciones-tipo-motivo",
                headers={"Content-Type": "application/json"},
                timeout=self.timeout
            )
            return response.json()
        except Exception as e:
            return {"success": False, "error": str(e)}

    def list_ausencias(self) -> Dict:
        """
        Obtiene todas las ausencias almacenadas

        Returns:
            Diccionario con success, data (lista de ausencias) y count

        Ejemplo:
            {
                "success": True,
                "data": [
                    {
                        "id": 1,
                        "employee_id": 5,
                        "employee_name": "Juan Pérez",
                        "fecha_inicio": "2024-05-10",
                        "fecha_fin": "2024-05-17",
                        "tipo_motivo": "VACACIONES",
                        ...
                    }
                ],
                "count": 1
            }
        """
        try:
            response = requests.get(
                f"{self.base_url}/api/ausencias/listar",
                headers={"Content-Type": "application/json"},
                timeout=self.timeout
            )
            return response.json()
        except Exception as e:
            return {"success": False, "error": str(e)}

    def create_ausencia(
        self,
        fecha_inicio: str,
        fecha_fin: str,
        tipo_motivo: str,
        descripcion_motivo: str,
        employee_id: Optional[int] = None,
        hora_inicio: float = 0.0,
        hora_fin: float = 0.0
    ) -> Dict:
        """
        Crea una nueva ausencia

        Args:
            fecha_inicio: Fecha de inicio (formato: YYYY-MM-DD)
            fecha_fin: Fecha de fin (formato: YYYY-MM-DD)
            tipo_motivo: Tipo de motivo (VACACIONES, MEDICO, ASUNTOS, OTROS)
            descripcion_motivo: Descripción detallada
            employee_id: ID del empleado (opcional)
            hora_inicio: Hora de inicio (formato decimal, ej: 9.0)
            hora_fin: Hora de fin (formato decimal, ej: 17.0)

        Returns:
            Diccionario con success, message y datos de la ausencia creada

        Ejemplo:
            {
                "success": True,
                "message": "Ausencia creada exitosamente",
                "ausencia": {
                    "id": 2,
                    "employee_id": 5,
                    ...
                }
            }
        """
        try:
            data = {
                "fecha_inicio": fecha_inicio,
                "fecha_fin": fecha_fin,
                "tipo_motivo": tipo_motivo,
                "descripcion_motivo": descripcion_motivo,
                "hora_inicio": hora_inicio,
                "hora_fin": hora_fin
            }

            if employee_id:
                data["employee_id"] = employee_id

            response = requests.post(
                f"{self.base_url}/api/ausencias/crear",
                json=data,
                headers={"Content-Type": "application/json"},
                timeout=self.timeout
            )
            return response.json()
        except Exception as e:
            return {"success": False, "error": str(e)}

    def create_vacaciones(
        self,
        fecha_inicio: str,
        fecha_fin: str,
        descripcion: str,
        employee_id: Optional[int] = None,
        hora_inicio: float = 8.0,
        hora_fin: float = 17.0
    ) -> Dict:
        """Crea una ausencia tipo VACACIONES"""
        return self.create_ausencia(
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
            tipo_motivo="VACACIONES",
            descripcion_motivo=descripcion,
            employee_id=employee_id,
            hora_inicio=hora_inicio,
            hora_fin=hora_fin
        )

    def create_permiso_medico(
        self,
        fecha_inicio: str,
        fecha_fin: str,
        descripcion: str,
        employee_id: Optional[int] = None,
        hora_inicio: float = 0.0,
        hora_fin: float = 0.0
    ) -> Dict:
        """Crea una ausencia tipo MEDICO"""
        return self.create_ausencia(
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
            tipo_motivo="MEDICO",
            descripcion_motivo=descripcion,
            employee_id=employee_id,
            hora_inicio=hora_inicio,
            hora_fin=hora_fin
        )

    def create_asuntos_propios(
        self,
        fecha_inicio: str,
        fecha_fin: str,
        descripcion: str,
        employee_id: Optional[int] = None,
        hora_inicio: float = 8.0,
        hora_fin: float = 17.0
    ) -> Dict:
        """Crea una ausencia tipo ASUNTOS PROPIOS"""
        return self.create_ausencia(
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
            tipo_motivo="ASUNTOS",
            descripcion_motivo=descripcion,
            employee_id=employee_id,
            hora_inicio=hora_inicio,
            hora_fin=hora_fin
        )

    def create_otros(
        self,
        fecha_inicio: str,
        fecha_fin: str,
        descripcion: str,
        employee_id: Optional[int] = None,
        hora_inicio: float = 0.0,
        hora_fin: float = 0.0
    ) -> Dict:
        """Crea una ausencia tipo OTROS"""
        return self.create_ausencia(
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
            tipo_motivo="OTROS",
            descripcion_motivo=descripcion,
            employee_id=employee_id,
            hora_inicio=hora_inicio,
            hora_fin=hora_fin
        )

    def get_ausencias_by_employee(self, employee_id: int) -> List[Dict]:
        """
        Obtiene todas las ausencias de un empleado específico

        Args:
            employee_id: ID del empleado

        Returns:
            Lista de ausencias del empleado
        """
        result = self.list_ausencias()
        if result.get("success"):
            return [
                ausencia for ausencia in result.get("data", [])
                if ausencia.get("employee_id") == employee_id
            ]
        return []

    def get_ausencias_by_tipo_motivo(self, tipo_motivo: str) -> List[Dict]:
        """
        Obtiene todas las ausencias de un tipo específico

        Args:
            tipo_motivo: Tipo de motivo (VACACIONES, MEDICO, ASUNTOS, OTROS)

        Returns:
            Lista de ausencias del tipo especificado
        """
        result = self.list_ausencias()
        if result.get("success"):
            return [
                ausencia for ausencia in result.get("data", [])
                if ausencia.get("tipo_motivo") == tipo_motivo
            ]
        return []

    def get_ausencias_between_dates(self, fecha_inicio: str, fecha_fin: str) -> List[Dict]:
        """
        Obtiene todas las ausencias en un rango de fechas

        Args:
            fecha_inicio: Fecha de inicio (YYYY-MM-DD)
            fecha_fin: Fecha de fin (YYYY-MM-DD)

        Returns:
            Lista de ausencias en el rango de fechas
        """
        result = self.list_ausencias()
        if result.get("success"):
            inicio = datetime.strptime(fecha_inicio, "%Y-%m-%d").date()
            fin = datetime.strptime(fecha_fin, "%Y-%m-%d").date()

            return [
                ausencia for ausencia in result.get("data", [])
                if (datetime.strptime(ausencia["fecha_inicio"], "%Y-%m-%d").date() >= inicio and
                    datetime.strptime(ausencia["fecha_fin"], "%Y-%m-%d").date() <= fin)
            ]
        return []


# Ejemplo de uso
if __name__ == "__main__":
    # Inicializar cliente
    client = AusenciasAPIClient()

    print("=" * 60)
    print("EJEMPLOS DE USO DEL CLIENTE API DE AUSENCIAS")
    print("=" * 60)

    # 1. Obtener opciones
    print("\n1. Obtener opciones de tipo_motivo:")
    opciones = client.obtain_tipo_motivo_options()
    if opciones.get("success"):
        for opcion in opciones.get("data", []):
            print(f"   - {opcion['value']}: {opcion['label']}")

    # 2. Listar todas las ausencias
    print("\n2. Listar todas las ausencias:")
    ausencias = client.list_ausencias()
    if ausencias.get("success"):
        print(f"   Total de ausencias: {ausencias.get('count')}")
        for ausencia in ausencias.get("data", []):
            print(f"   - {ausencia['employee_name']}: {ausencia['fecha_inicio']} al {ausencia['fecha_fin']} ({ausencia['tipo_motivo']})")

    # 3. Crear una vacación
    print("\n3. Crear una nueva vacación:")
    resultado = client.create_vacaciones(
        fecha_inicio="2024-07-01",
        fecha_fin="2024-07-07",
        descripcion="Vacaciones de verano",
        employee_id=5
    )
    if resultado.get("success"):
        print(f"   ✅ Ausencia creada con ID: {resultado['ausencia']['id']}")
    else:
        print(f"   ❌ Error: {resultado.get('error')}")

    # 4. Obtener ausencias de un empleado específico
    print("\n4. Ausencias del empleado 5:")
    ausencias_empleado = client.get_ausencias_by_employee(5)
    for ausencia in ausencias_empleado:
        print(f"   - {ausencia['fecha_inicio']} al {ausencia['fecha_fin']} ({ausencia['tipo_motivo']})")

    # 5. Obtener ausencias por tipo
    print("\n5. Todas las vacaciones:")
    vacaciones = client.get_ausencias_by_tipo_motivo("VACACIONES")
    print(f"   Total de vacaciones: {len(vacaciones)}")
    for vac in vacaciones:
        print(f"   - {vac['employee_name']}: {vac['fecha_inicio']} al {vac['fecha_fin']}")

    print("\n" + "=" * 60)

