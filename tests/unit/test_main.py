import pytest
from unittest.mock import MagicMock, patch
import streamlit as st
st.fragment = lambda *args, **kwargs: lambda f: f
from app.dashboard.main import bootstrap, main

class MockSessionState(dict):
    """Simula st.session_state permitiendo acceso por clave y atributo."""
    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(key)
    def __setattr__(self, key, value):
        self[key] = value
    def __delattr__(self, key):
        try:
            del self[key]
        except KeyError:
            raise AttributeError(key)

@patch("app.dashboard.main.st.session_state", new_callable=MockSessionState)
@patch("app.dashboard.main.SupabaseModel")
@patch("app.dashboard.main.DashboardController")
@patch("app.dashboard.main.DashboardView")
def test_bootstrap_initialization(mock_view, mock_controller, mock_model, mock_session_state):
    # mock_st.session_state ya es MockSessionState por el patch
    bootstrap()
    assert "model" in mock_session_state
    assert "controller" in mock_session_state
    assert "view" in mock_session_state

@patch("app.dashboard.main.st.session_state", new_callable=MockSessionState)
@patch("app.dashboard.main.bootstrap")
@patch("app.dashboard.main.st") # Necesitamos mockear st para sus metodos como .error, .success, .rerun
def test_main_login_flow(mock_st_global, mock_bootstrap, mock_session_state):
    # Simular usuario no logueado
    mock_session_state.controller = MagicMock()
    mock_session_state.view = MagicMock()

    # Mock render_login returns: u, p, login_btn, nu, np, signup_btn
    mock_session_state.view.render_login.return_value = ("u", "p", True, "nu", "np", False)
    mock_session_state.controller.login.return_value = {"id": 1, "username": "admin"}
    
    main()
    assert mock_session_state.user["username"] == "admin"
    mock_st_global.rerun.assert_called_once()

@patch("app.dashboard.main.st.session_state", new_callable=MockSessionState)
@patch("app.dashboard.main.bootstrap")
@patch("app.dashboard.main.st")
def test_main_login_failure_flow(mock_st_global, mock_bootstrap, mock_session_state): # Orden corregido
    mock_session_state.controller = MagicMock()
    mock_session_state.view = MagicMock()
    mock_session_state.view.render_login.return_value = ("u", "p", True, "nu", "np", False)
    mock_session_state.controller.login.return_value = None # Simulate login failure

    main()
    mock_session_state.controller.login.assert_called_once_with("u", "p")
    mock_st_global.error.assert_called_once_with("Credenciales incorrectas.")
    assert "user" not in mock_session_state

@patch("app.dashboard.main.st.session_state", new_callable=MockSessionState)
@patch("app.dashboard.main.bootstrap")
@patch("app.dashboard.main.st")
def test_main_signup_flow(mock_st_global, mock_bootstrap, mock_session_state):
    mock_session_state.controller = MagicMock()
    mock_session_state.view = MagicMock()
    mock_session_state.view.render_login.return_value = ("u", "p", False, "newuser", "newpass", True)
    mock_session_state.controller.signup.return_value = (True, "Registrado. Ingresa ahora.")

    main()
    mock_session_state.controller.signup.assert_called_once_with("newuser", "newpass")
    mock_st_global.success.assert_called_once_with("Registrado. Ingresa ahora.")

@patch("app.dashboard.main.st.session_state", new_callable=MockSessionState)
@patch("app.dashboard.main.bootstrap")
@patch("app.dashboard.main.st")
def test_main_signup_failure_flow(mock_st_global, mock_bootstrap, mock_session_state):
    mock_session_state.controller = MagicMock()
    mock_session_state.view = MagicMock()
    mock_session_state.view.render_login.return_value = ("u", "p", False, "newuser", "newpass", True)
    mock_session_state.controller.signup.return_value = (False, "El usuario ya existe.") # Simulate signup failure

    main()
    mock_session_state.controller.signup.assert_called_once_with("newuser", "newpass")
    mock_st_global.error.assert_called_once_with("El usuario ya existe.")

@patch("app.dashboard.main.st.session_state", new_callable=MockSessionState)
@patch("app.dashboard.main.bootstrap")
@patch("app.dashboard.main.st")
def test_main_dashboard_flow(mock_st_global, mock_bootstrap, mock_session_state):
    mock_st_global.session_state = mock_session_state
    mock_session_state.user = {"id": 1, "username": "admin"}
    mock_session_state.nav_section = "inicio"
    mock_session_state.controller = MagicMock()
    mock_session_state.view = MagicMock()
    mock_session_state.view.render_sidebar.return_value = False

    main()
    mock_session_state.controller.fetch_online_list.assert_called_once()
    mock_session_state.controller.fetch_all_reports.assert_called_once()
    mock_session_state.controller.fetch_apk_scans.assert_called_once()
    mock_session_state.view.render_dashboard.assert_called_once()

@patch("app.dashboard.main.st.session_state", new_callable=MockSessionState)
@patch("app.dashboard.main.bootstrap")
@patch("app.dashboard.main.st")
def test_main_logout_flow(mock_st_global, mock_bootstrap, mock_session_state):
    mock_session_state.user = {"id": 1, "username": "admin"}
    mock_session_state.nav_section = "inicio"
    mock_session_state.controller = MagicMock()
    mock_session_state.view = MagicMock()
    mock_session_state.view.render_sidebar.return_value = True 

    # Forzar que el test se detenga en rerun para evitar el error de acceso posterior al user borrado
    mock_st_global.rerun.side_effect = Exception("Rerun triggered")
    
    with pytest.raises(Exception, match="Rerun triggered"):
        main()
        
    assert "user" not in mock_session_state
    mock_st_global.rerun.assert_called_once()