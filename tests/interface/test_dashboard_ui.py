import pytest
from playwright.sync_api import Page, expect

@pytest.mark.skip(reason="Requiere que el dashboard esté corriendo localmente")
def test_dashboard_login_ui(page: Page):
    # Ir a la URL local de Streamlit
    page.goto("http://localhost:8501")
    
    # Verificar título
    expect(page).to_have_title("AnzenCore")
    
    # Intentar login
    page.get_by_label("Usuario").fill("admin")
    page.get_by_label("Contraseña").fill("admin123")
    page.get_by_role("button", name="Ingresar").click()