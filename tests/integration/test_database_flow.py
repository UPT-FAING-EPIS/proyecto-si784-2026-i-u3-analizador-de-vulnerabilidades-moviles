import pytest
from app.dashboard.controllers.dashboard_controller import DashboardController

class MockSupabaseModel:
    def get_vulnerabilities(self, user_id=None):
        class Response:
            data = [{"id": 1, "vulnerabilidad": "Insecure Logging", "nivel": "Bajo"}]
        return Response()

def test_fetch_reports_integration():
    """
    Valida el flujo desde el controlador hasta la 'capa de datos'.
    """
    model = MockSupabaseModel()
    controller = DashboardController(model)
    
    reports = controller.fetch_all_reports("user-123")
    
    assert len(reports) > 0
    assert reports[0]["vulnerabilidad"] == "Insecure Logging"