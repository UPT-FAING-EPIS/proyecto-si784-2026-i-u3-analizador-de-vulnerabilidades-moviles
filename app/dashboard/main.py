import streamlit as st

from app.dashboard.config.settings import DashboardSettings
from app.dashboard.config.styles import inject_css
from app.dashboard.controllers.dashboard_controller import DashboardController
from app.dashboard.models.supabase_model import SupabaseModel
from app.dashboard.views.dashboard_view import DashboardView


st.set_page_config(
    page_title=DashboardSettings.page_title,
    page_icon="🛡️",
    layout=DashboardSettings.layout,
)

inject_css()


def bootstrap():
    if "model" not in st.session_state:
        st.session_state.model = SupabaseModel()
        st.session_state.controller = DashboardController(st.session_state.model)
        st.session_state.view = DashboardView()
    # Sección activa por defecto
    if "nav_section" not in st.session_state:
        st.session_state.nav_section = "inicio"


@st.fragment(run_every=DashboardSettings.ping_interval_s)
def _ping_fragment(controller):
    """
    Actualiza el ping y guarda usuarios online en session_state.
    Solo este bloque se refresca cada N segundos — sin parpadeo de página completa.
    La lista de usuarios se muestra en la página Comunidad, no en el sidebar.
    """
    if "user" not in st.session_state:
        return
    user_id = st.session_state.user["id"]
    controller.update_user_ping(user_id)
    online_users = controller.fetch_online_list()
    st.session_state.online_users = online_users


def main():
    bootstrap()
    controller = st.session_state.controller
    view = st.session_state.view

    # ── Pantalla de login ──────────────────────────────────────────────────
    if "user" not in st.session_state:
        username, password, login_button, new_username, new_password, signup_button = (
            view.render_login(controller)
        )
        if login_button:
            user = controller.login(username, password)
            if user:
                st.session_state.user = user
                st.rerun()
            else:
                st.error("Credenciales incorrectas.")

        if signup_button:
            ok, message = controller.signup(new_username, new_password)
            if ok:
                st.success(message)
            else:
                st.error(message)
        return

    # ── Dashboard ──────────────────────────────────────────────────────────
    user_id = st.session_state.user["id"]

    # Sidebar con nav — devuelve True si se presionó logout
    if view.render_sidebar(st.session_state.user):
        del st.session_state.user
        del st.session_state.nav_section
        st.rerun()

    # Datos de la sección activa
    reports = controller.fetch_all_reports(user_id)
    apk_scans = controller.fetch_apk_scans(user_id)

    # Contenido principal según sección seleccionada
    view.render_dashboard(
        st.session_state.user,
        reports,
        apk_scans,
        controller,
    )

    # Fragment aislado: actualiza ping y online_users sin rerender de página
    _ping_fragment(controller)


if __name__ == "__main__":
    main()
