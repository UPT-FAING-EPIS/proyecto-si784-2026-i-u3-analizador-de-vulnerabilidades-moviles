import os

import pandas as pd
import plotly.express as px
import streamlit as st

from app.dashboard.config.settings import DashboardSettings
from app.dashboard.config.styles import severity_icon

# ── Definición del menú de navegación ─────────────────────────────────────────
NAV_ITEMS = [
    {"key": "inicio",     "icon": "🏠", "label": "Inicio"},
    {"key": "metricas",   "icon": "📊", "label": "Métricas"},
    {"key": "escanear",   "icon": "📤", "label": "Escanear APK"},
    {"key": "historial",  "icon": "📋", "label": "Historial APK"},
    {"key": "comunidad",  "icon": "🌐", "label": "Comunidad"},
    {"key": "agente",     "icon": "🤖", "label": "Agente Móvil"},
    {"key": "manual",     "icon": "🔎", "label": "Escaneo Manual"},
    {"key": "repo_calidad", "icon": "📦", "label": "Analizador Estático"},
    {"key": "api_externa", "icon": "🔗", "label": "OWASP Verificator"},
]


from app.dashboard.config.kb import APK_FINDING_KB, APK_ARTIFACT_KB


@st.fragment
def _file_detail_frag(view, files):
    view._render_file_detail(files)


class DashboardView:
    _CLOSE_DIV = "</div>"
    _BTN_ANALIZAR = "🔍 Analizar"

    # ── APK download ──────────────────────────────────────────────────────────
    def render_apk_download(self, apk_path, filename):
        with open(apk_path, "rb") as apk_file:
            st.download_button(
                label="⬇️  Descargar AnzenCore APK",
                data=apk_file,
                file_name=filename,
                mime="application/vnd.android.package-archive",
                use_container_width=True,
            )

    @st.fragment(run_every=10)
    def _render_global_dash(self, controller):
        global_scans = controller.fetch_global_apk_scans()
        if not global_scans:
            st.info("Aún no hay análisis en la plataforma.")
            return

        df_global = pd.DataFrame(global_scans)
        c1, c2 = st.columns(2)
        c1.metric("📱 Total de APKs analizados", len(df_global))
        total_hallazgos = df_global["findings_count"].sum() if "findings_count" in df_global.columns else 0
        c2.metric("🔍 Hallazgos detectados globalmente", total_hallazgos)
        
        st.markdown("### Distribución de Riesgos Globales")
        if "severity_max" in df_global.columns:
            severity_counts = df_global["severity_max"].fillna("Info").value_counts().reset_index()
            severity_counts.columns = ["Severidad", "Cantidad"]
            
            col_pie, col_bar = st.columns(2)
            with col_pie:
                fig_pie = px.pie(severity_counts, names="Severidad", values="Cantidad", hole=0.4, title="Proporción de Riesgos")
                st.plotly_chart(fig_pie, use_container_width=True)
            with col_bar:
                fig_bar = px.bar(severity_counts, x="Severidad", y="Cantidad", color="Severidad", title="Cantidad por Nivel de Riesgo")
                st.plotly_chart(fig_bar, use_container_width=True)

    # ── Login ─────────────────────────────────────────────────────────────────
    def render_login(self, controller):
        st.markdown(
            """
            <div class="login-card">
                <div class="login-logo">🛡️</div>
                <div class="login-title">AnzenCore</div>
                <div class="login-subtitle">Plataforma de seguridad móvil</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        tab_dash, tab_login, tab_signup = st.tabs(["📊 Dashboard General", "🔑 Iniciar sesión", "✨ Crear cuenta"])
        
        username, password, login_button = None, None, None
        new_username, new_password, signup_button = None, None, None

        with tab_dash:
            self._render_global_dash(controller)

        _, col, _ = st.columns([1, 3, 1])
        with col:
            with tab_login:
                username = st.text_input("Usuario", key="l_u", placeholder="Tu usuario")
                password = st.text_input(
                    "Contraseña", type="password", key="l_p", placeholder="••••••••"
                )
                login_button = st.button(
                    "Iniciar sesión", use_container_width=True, key="login_btn"
                )
            with tab_signup:
                new_username = st.text_input(
                    "Nuevo usuario", key="r_u", placeholder="Elige un usuario"
                )
                new_password = st.text_input(
                    "Nueva contraseña", type="password", key="r_p", placeholder="••••••••"
                )
                signup_button = st.button(
                    "Crear cuenta", use_container_width=True, key="signup_btn"
                )

        return username, password, login_button, new_username, new_password, signup_button

    # ── Sidebar con navegación ────────────────────────────────────────────────
    def render_sidebar(self, user):
        active = st.session_state.get("nav_section", "inicio")

        with st.sidebar:
            # Branding
            st.markdown(
                """
                <div style="text-align:center; padding: 1rem 0 .5rem;">
                    <div style="font-size:2.5rem;">🛡️</div>
                    <div style="font-size:1.1rem; font-weight:700; color:#00d4ff; margin:.3rem 0 .1rem;">
                        AnzenCore
                    </div>
                    <div style="font-size:.75rem; color:#64748b; letter-spacing:.06em; text-transform:uppercase;">
                        Security Dashboard
                    </div>
                </div>
                <hr style="margin:.75rem 0;"/>
                """,
                unsafe_allow_html=True,
            )

            # Info de usuario (compacta, arriba)
            st.markdown(
                f"""
                <div style="background:rgba(0,212,255,.06); border:1px solid rgba(0,212,255,.18);
                            border-radius:10px; padding:.6rem .9rem; margin-bottom:.75rem;">
                    <div style="font-size:.65rem; color:#64748b; text-transform:uppercase;
                                letter-spacing:.08em; margin-bottom:.2rem;">Usuario activo</div>
                    <div style="font-weight:700; color:#e2e8f0; font-size:.9rem;">
                        👤 {user['username']}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            # Menú de navegación
            st.markdown(
                '<div class="nav-section-label">Navegación</div>',
                unsafe_allow_html=True,
            )
            for item in NAV_ITEMS:
                is_active = active == item["key"]
                css_class = "nav-btn-active" if is_active else "nav-btn"
                st.markdown(f'<div class="{css_class}">', unsafe_allow_html=True)
                if st.button(
                    f"{item['icon']}  {item['label']}",
                    key=f"nav_{item['key']}",
                    use_container_width=True,
                ):
                    st.session_state.nav_section = item["key"]
                    st.rerun()
                st.markdown(self._CLOSE_DIV, unsafe_allow_html=True)

            # Separador y botón de cierre de sesión (siempre visible)
            st.markdown("<hr/>", unsafe_allow_html=True)
            st.markdown(
                """
                <style>
                div[data-testid="stSidebar"] div[data-testid="stButton"]:last-of-type > button {
                    background: rgba(255,71,87,.12) !important;
                    border: 1px solid rgba(255,71,87,.5) !important;
                    color: #ff4757 !important;
                    font-weight: 600 !important;
                    width: 100% !important;
                }
                div[data-testid="stSidebar"] div[data-testid="stButton"]:last-of-type > button:hover {
                    background: rgba(255,71,87,.25) !important;
                    box-shadow: 0 0 16px rgba(255,71,87,.3) !important;
                }
                </style>
                """,
                unsafe_allow_html=True,
            )
            logout = st.button(
                "🚪  Cerrar sesión",
                use_container_width=True,
                key="logout_btn",
            )

            st.markdown(
                """
                <div style="font-size:.68rem; color:#64748b; text-align:center; margin-top:.6rem;">
                    AnzenCore v1.0 · Seguridad Móvil
                </div>
                """,
                unsafe_allow_html=True,
            )

        return logout

    # ── Router principal ──────────────────────────────────────────────────────
    def render_dashboard(self, user, reports, apk_scans, controller):
        section = st.session_state.get("nav_section", "inicio")
        nav_meta = next((n for n in NAV_ITEMS if n["key"] == section), NAV_ITEMS[0])

        # Breadcrumb de sección
        st.markdown(
            f"""
            <div class="page-header">
                🛡️ AnzenCore &nbsp;›&nbsp; <span>{nav_meta['icon']} {nav_meta['label']}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if section == "inicio":
            self._render_inicio(user, reports, apk_scans)
        elif section == "metricas":
            self.render_user_metrics(user, controller)
        elif section == "escanear":
            self.render_apk_scanner(user, controller)
        elif section == "historial":
            self.render_apk_scan_history(apk_scans, controller)
        elif section == "comunidad":
            self.render_comunidad()
        elif section == "agente":
            self.render_vulnerability_history(reports)
        elif section == "manual":
            self.render_manual_scan(controller)
        elif section == "repo_calidad":
            self.render_repo_quality(controller)
        elif section == "api_externa":
            self.render_api_externa(controller)

    # ── Inicio / Overview ─────────────────────────────────────────────────────
    def _render_inicio(self, user, reports, apk_scans):
        st.markdown(
            f"""
            <div style="margin-bottom:1.5rem;">
                <h1 style="margin:0;">Bienvenido, {user['username']} 👋</h1>
                <div style="color:#64748b; font-size:.9rem; margin-top:.25rem;">
                    Resumen de actividad de seguridad
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("📱 APKs analizados", len(apk_scans) if apk_scans else 0)

        # Total de hallazgos = suma de findings_count en todos los escaneos del usuario
        total_findings = sum(s.get("findings_count", 0) for s in apk_scans) if apk_scans else 0
        c2.metric("🔍 Hallazgos totales", total_findings)

        # Usuarios online (desde session_state, actualizado por el fragment)
        online_users = st.session_state.get("online_users", [])
        c3.metric("🌐 Online ahora", len(online_users))

        # Reportes del agente móvil
        agent_reports = len(reports) if reports else 0
        scan_results = len(st.session_state.get("scan_results", []))
        c4.metric("🤖 Reportes del agente", agent_reports + scan_results)

        st.divider()

        # Descarga APK agente
        col_apk, col_info = st.columns([1, 2])
        with col_apk:
            st.markdown("### 📲 Agente móvil")
            apk_path = DashboardSettings.apk_path
            if os.path.exists(apk_path) and os.path.getsize(apk_path) > 0:
                self.render_apk_download(apk_path, DashboardSettings.apk_filename)
            else:
                st.error("APK no disponible en /assets")

        with col_info:
            st.markdown("### 📊 Últimos escaneos")
            if apk_scans:
                df = pd.DataFrame(apk_scans[:5])
                display_cols = [c for c in ["file_name", "status", "severity_max", "created_at"] if c in df.columns]
                st.dataframe(
                    df[display_cols].rename(columns={
                        "file_name": "APK", "status": "Estado",
                        "severity_max": "Severidad", "created_at": "Fecha",
                    }),
                    use_container_width=True, hide_index=True,
                )
            else:
                st.markdown(
                    """
                    <div style="text-align:center; padding:1.5rem; background:rgba(17,24,39,.6);
                                border:1px dashed rgba(0,212,255,.2); border-radius:12px; color:#64748b;">
                        <div style="font-size:1.5rem;">📭</div>
                        <div style="margin-top:.4rem;">Sin escaneos aún. Ve a <b>Escanear APK</b>.</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

    # ── User Metrics Dashboard ────────────────────────────────────────────────
    @st.fragment(run_every=10)
    def render_user_metrics(self, user, controller):
        apk_scans = controller.fetch_apk_scans(user["id"])
        
        st.markdown(f"## 📊 Métricas Detalladas de {user['username']}")
        if not apk_scans:
            st.info("Aún no has analizado ningún APK. Ve a 'Escanear APK' para comenzar.")
            return

        df = pd.DataFrame(apk_scans)
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("📦 Tus APKs analizados", len(df))
        total_hallazgos = df["findings_count"].sum() if "findings_count" in df.columns else 0
        c2.metric("🔍 Tus hallazgos totales", total_hallazgos)
        promedio = round(total_hallazgos / len(df), 1) if len(df) > 0 else 0
        c3.metric("⚖️ Promedio Hallazgos/APK", promedio)
        
        # Calcular tamaño total analizado si existe el campo
        if "file_size_bytes" in df.columns:
            total_mb = df["file_size_bytes"].sum() / (1024 * 1024)
            c4.metric("💾 Datos Analizados (MB)", f"{total_mb:.1f}")
        else:
            c4.metric("💾 Datos Analizados", "N/A")

        st.divider()
        st.markdown("### 🎯 Análisis de Riesgos de tus APKs")

        if "severity_max" in df.columns:
            severity_counts = df["severity_max"].fillna("Info").value_counts().reset_index()
            severity_counts.columns = ["Severidad", "Cantidad"]
            
            # Asignar colores fijos a los riesgos para mantener la coherencia
            color_map = {
                "Critico": "#ff4757", "Alto": "#ffa502", 
                "Medio": "#ffdd59", "Bajo": "#00ff88", "Info": "#00d4ff"
            }
            
            col_pie, col_bar = st.columns(2)
            with col_pie:
                fig_pie = px.pie(
                    severity_counts, names="Severidad", values="Cantidad", hole=0.45, 
                    title="Proporción de Severidad", color="Severidad", color_discrete_map=color_map,
                    template="plotly_dark"
                )
                fig_pie.update_traces(hoverinfo='label+percent', textfont_size=14, marker=dict(line=dict(color='#0a0e1a', width=2)))
                st.plotly_chart(fig_pie, use_container_width=True)
            with col_bar:
                fig_bar = px.bar(
                    severity_counts, x="Severidad", y="Cantidad", color="Severidad", 
                    title="Volumen Absoluto por Nivel", color_discrete_map=color_map,
                    template="plotly_dark"
                )
                fig_bar.update_layout(showlegend=False)
                st.plotly_chart(fig_bar, use_container_width=True)

        col_line, col_ranking = st.columns([1.5, 1])
        with col_line:
            if "created_at" in df.columns:
                st.markdown("### 📈 Evolución en el Tiempo")
                df["Fecha"] = pd.to_datetime(df["created_at"]).dt.date
                date_counts = df["Fecha"].value_counts().reset_index()
                date_counts.columns = ["Fecha", "Cantidad de APKs"]
                date_counts = date_counts.sort_values("Fecha")
                fig_line = px.line(
                    date_counts, x="Fecha", y="Cantidad de APKs", markers=True, 
                    title="Actividad de Escaneo por Día", template="plotly_dark"
                )
                fig_line.update_traces(line_color="#00d4ff", marker=dict(size=8, color="#00ff88"))
                st.plotly_chart(fig_line, use_container_width=True)

        with col_ranking:
            st.markdown("### 🏆 Top 5 APKs Vulnerables")
            if "findings_count" in df.columns:
                top_apks = df.sort_values("findings_count", ascending=False).head(5)
                display_cols = ["file_name", "findings_count", "severity_max"]
                display_cols = [c for c in display_cols if c in top_apks.columns]
                
                # Función para colorear según severidad
                def color_severity(val):
                    color_dict = {"Critico": "#ff4757", "Alto": "#ffa502", "Medio": "#ffdd59", "Bajo": "#00ff88", "Info": "#00d4ff"}
                    color = color_dict.get(val, "white")
                    return f'color: {color}; font-weight: bold'
                
                styled_df = top_apks[display_cols].rename(columns={
                    "file_name": "Nombre APK", "findings_count": "Hallazgos", "severity_max": "Nivel"
                }).style.map(color_severity, subset=['Nivel'])
                
                st.dataframe(styled_df, use_container_width=True, hide_index=True)

    # ── APK scanner ───────────────────────────────────────────────────────────
    def render_apk_scanner(self, user, controller):
        st.markdown("## 📤 Escanear APK")
        st.markdown(
            "<div style='color:#64748b; font-size:.88rem; margin-bottom:1rem;'>"
            "Sube un archivo APK para analizarlo por ingeniería inversa y detectar vulnerabilidades.</div>",
            unsafe_allow_html=True,
        )
        col_upload, col_btn = st.columns([3, 1])
        with col_upload:
            uploaded_file = st.file_uploader(
                "Selecciona un archivo APK",
                type=["apk"],
                label_visibility="collapsed",
            )
        with col_btn:
            st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
            scan_btn = st.button("🔍  Analizar", use_container_width=True)

        if scan_btn:
            with st.spinner("⚙️  Analizando APK por ingeniería inversa..."):
                ok, result = controller.create_apk_scan(user["id"], uploaded_file)
            if ok:
                st.success(f"✅ {result['message']}")
                st.markdown("### 📊 Resultados del análisis")
                
                scan_id = result["scan_id"]
                apk_scans = controller.fetch_apk_scans(user["id"])
                selected_scan = next((s for s in apk_scans if s.get("id") == scan_id), None)
                
                if selected_scan:
                    findings = controller.fetch_apk_findings(scan_id)
                    artifacts = controller.fetch_apk_artifacts(scan_id)
                    self.render_scan_detail(selected_scan, findings, artifacts, controller)
            else:
                st.error(f"❌ {result}")

    # ── APK scan history ──────────────────────────────────────────────────────
    def render_apk_scan_history(self, apk_scans, controller):
        st.markdown("## 📋 Historial de escaneos APK")

        if not apk_scans:
            st.markdown(
                """
                <div style="text-align:center; padding:2rem; background:rgba(17,24,39,.6);
                            border:1px dashed rgba(0,212,255,.2); border-radius:12px; color:#64748b;">
                    <div style="font-size:2rem; margin-bottom:.5rem;">📭</div>
                    <div>Todavía no hay APKs analizados.</div>
                    <div style="font-size:.8rem; margin-top:.25rem;">Sube un APK en <b>Escanear APK</b>.</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            return

        df = pd.DataFrame(apk_scans)

        if "severity_max" in df.columns:
            severity_counts = df["severity_max"].fillna("Info").value_counts().to_dict()
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("🔴 Críticos", severity_counts.get("Critico", 0))
            c2.metric("🟠 Altos", severity_counts.get("Alto", 0))
            c3.metric("🟡 Medios", severity_counts.get("Medio", 0))
            c4.metric(
                "🟢 Bajos / Info",
                severity_counts.get("Bajo", 0) + severity_counts.get("Info", 0),
            )

        display_columns = [
            col for col in
            ["file_name", "package_name", "app_name", "status", "severity_max", "findings_count", "created_at"]
            if col in df.columns
        ]
        history_df = df[display_columns].copy().rename(
            columns={
                "file_name": "APK", "package_name": "Paquete", "app_name": "App",
                "status": "Estado", "severity_max": "Severidad",
                "findings_count": "Hallazgos", "created_at": "Fecha",
            }
        )
        st.dataframe(history_df, use_container_width=True, hide_index=True)

        scan_options = {
            (
                f"{severity_icon(row.get('severity_max', ''))}  "
                f"{row.get('file_name', 'APK')}  ·  "
                f"{row.get('findings_count', 0)} hallazgos  ·  "
                f"{str(row.get('created_at', ''))[:16]}"
            ): row["id"]
            for row in apk_scans
            if row.get("id")
        }
        if not scan_options:
            return

        selected_label = st.selectbox("🔎  Ver detalle de escaneo", options=list(scan_options.keys()))
        selected_scan_id = scan_options[selected_label]
        selected_scan = next(scan for scan in apk_scans if scan.get("id") == selected_scan_id)
        findings = controller.fetch_apk_findings(selected_scan_id)
        artifacts = controller.fetch_apk_artifacts(selected_scan_id)
        self.render_scan_detail(selected_scan, findings, artifacts, controller)

    # ── Scan detail ───────────────────────────────────────────────────────────
    def _render_finding_expander(self, finding):
        severity = finding.get("severity", "Info")
        icon = severity_icon(severity)
        f_type = finding.get("finding_type", "")
        kb_info = APK_FINDING_KB.get(f_type, {})
        with st.expander(
            f"{icon}  [{severity}]  {finding.get('title', 'Hallazgo')}  —  {f_type or 'general'}"
        ):
            st.markdown(f"**📝 Explicación:**\n{finding.get('description', 'Sin descripción.')}")
            implicacion = kb_info.get("implicacion")
            if implicacion:
                st.markdown(f"**⚠️ Lo que implica (Riesgo):**\n{implicacion}")
            if finding.get("evidence"):
                st.markdown("**🔍 Evidencia / Código vulnerable:**")
                st.markdown(finding["evidence"])
            cols = st.columns(2)
            if finding.get("source_file"):
                cols[0].caption(f"📄 Fuente: `{finding['source_file']}`")
            refs = [v for v in [finding.get("cwe"), finding.get("owasp_mobile")] if v]
            if refs:
                cols[1].caption("🔗 " + "  /  ".join(refs))
            rec = finding.get("recommendation") or kb_info.get("recommendation")
            if rec:
                st.info(f"💡 **Recomendación:** {rec}")

    def _render_findings_tab(self, findings):
        if not findings:
            st.info("Este escaneo no tiene hallazgos registrados.")
            return
        severity_order = {"Critico": 0, "Alto": 1, "Medio": 2, "Bajo": 3, "Info": 4}
        sorted_findings = sorted(findings, key=lambda i: severity_order.get(i.get("severity"), 99))
        for finding in sorted_findings:
            self._render_finding_expander(finding)

    def _render_artifacts_tab(self, artifacts):
        if not artifacts:
            st.info("Este escaneo no tiene artefactos registrados.")
            return
        artifact_df = pd.DataFrame(artifacts)
        display_cols = [c for c in ["artifact_type", "artifact_value", "source_file"] if c in artifact_df.columns]
        st.dataframe(
            artifact_df[display_cols].rename(columns={
                "artifact_type": "Tipo", "artifact_value": "Valor", "source_file": "Fuente"
            }),
            use_container_width=True, hide_index=True,
        )
        st.markdown("<div style='height:15px'></div>", unsafe_allow_html=True)
        st.markdown("### 💡 Guía de análisis de artefactos")
        unique_types = sorted({a.get("artifact_type") for a in artifacts if a.get("artifact_type")})
        for a_type in unique_types:
            kb_info = APK_ARTIFACT_KB.get(a_type)
            if kb_info:
                with st.expander(f"📁  {kb_info['titulo']} ({a_type})"):
                    st.markdown(f"**📝 Explicación:**\n{kb_info['descripcion']}")
                    st.info(f"💡 **Recomendación:** {kb_info['recommendation']}")

    def render_scan_detail(self, scan, findings, artifacts, controller):
        tab_findings, tab_artifacts, tab_exports = st.tabs(
            ["🔍  Hallazgos", "🗂️  Artefactos", "📤  Exportar"]
        )
        with tab_findings:
            self._render_findings_tab(findings)
        with tab_artifacts:
            self._render_artifacts_tab(artifacts)
        with tab_exports:
            st.markdown("**Exporta el resultado del escaneo seleccionado**")
            pdf_name, pdf_data = controller.build_report_export(scan, findings, artifacts, "pdf")
            st.download_button("📕  Descargar PDF", data=pdf_data, file_name=pdf_name, mime="application/pdf", use_container_width=True)

    # ── Comunidad ─────────────────────────────────────────────────────────────
    def render_comunidad(self):
        online_users = st.session_state.get("online_users", [])
        total = len(online_users)

        st.markdown(
            """
            <div style="margin-bottom:1.5rem;">
                <h1 style="margin:0;">Comunidad</h1>
                <div style="color:#64748b; font-size:.9rem; margin-top:.25rem;">
                    Usuarios activos en los últimos 30 segundos
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Métrica principal
        col_m, col_info = st.columns([1, 3])
        col_m.metric("🌐 Usuarios online", total)
        with col_info:
            st.markdown(
                """
                <div style="background:rgba(0,255,136,.05); border:1px solid rgba(0,255,136,.15);
                            border-radius:10px; padding:.75rem 1.1rem; font-size:.85rem; color:#64748b;
                            display:flex; align-items:center; gap:.6rem; height:100%;">
                    <span class="online-dot"></span>
                    La lista se actualiza automáticamente cada 30 segundos sin recargar la página.
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.divider()

        if not online_users:
            st.markdown(
                """
                <div style="text-align:center; padding:3rem 2rem; background:rgba(17,24,39,.6);
                            border:1px dashed rgba(0,255,136,.2); border-radius:14px; color:#64748b;">
                    <div style="font-size:2.5rem; margin-bottom:.75rem;">🌐</div>
                    <div style="font-size:1rem; font-weight:600; color:#e2e8f0;">
                        Solo tú estás conectado ahora mismo
                    </div>
                    <div style="font-size:.85rem; margin-top:.4rem;">
                        Cuando otros usuarios inicien sesión aparecerán aquí.
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            return

        # Grid de tarjetas de usuarios
        cols_per_row = 3
        rows = [online_users[i:i + cols_per_row] for i in range(0, len(online_users), cols_per_row)]

        for row in rows:
            cols = st.columns(cols_per_row)
            for idx, u in enumerate(row):
                with cols[idx]:
                    # Iniciales del usuario para el avatar
                    initials = u["username"][:2].upper()
                    st.markdown(
                        f"""
                        <div style="
                            background: linear-gradient(135deg, rgba(17,24,39,.95), rgba(26,34,53,.95));
                            border: 1px solid rgba(0,255,136,.25);
                            border-radius: 14px;
                            padding: 1.25rem 1rem;
                            text-align: center;
                            transition: transform .2s, border-color .2s;
                            margin-bottom: .5rem;
                        ">
                            <div style="
                                width: 52px; height: 52px;
                                background: linear-gradient(135deg, #00d4ff22, #00ff8822);
                                border: 2px solid rgba(0,255,136,.4);
                                border-radius: 50%;
                                display: flex; align-items: center; justify-content: center;
                                font-size: 1.1rem; font-weight: 700;
                                color: #00ff88;
                                margin: 0 auto .75rem;
                                font-family: 'JetBrains Mono', monospace;
                            ">{initials}</div>
                            <div style="font-weight:700; font-size:.95rem; color:#e2e8f0; margin-bottom:.4rem;">
                                {u['username']}
                            </div>
                            <div style="
                                display: inline-flex; align-items: center; gap: .35rem;
                                background: rgba(0,255,136,.08);
                                border: 1px solid rgba(0,255,136,.2);
                                border-radius: 20px;
                                padding: .2rem .65rem;
                                font-size: .72rem; color: #00ff88; font-weight: 600;
                            ">
                                <span class="online-dot" style="width:6px;height:6px;"></span>
                                Activo
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

    # ── Online users (usado por el fragment en main.py) ───────────────────────
    def render_online_users(self, online_users):
        st.markdown(
            '<div class="nav-section-label" style="padding:.4rem .2rem .6rem;">🌐 Usuarios online ahora</div>',
            unsafe_allow_html=True,
        )
        if not online_users:
            st.markdown(
                '<span class="online-dot"></span><span style="color:#64748b; font-size:.82rem;"> Solo tú estás online.</span>',
                unsafe_allow_html=True,
            )
            return
        for u in online_users:
            st.markdown(
                f"""
                <div style="display:flex; align-items:center; gap:.5rem; padding:.35rem .5rem;
                            border-radius:7px; margin:.15rem 0; background:rgba(0,255,136,.05);
                            border:1px solid rgba(0,255,136,.15);">
                    <span class="online-dot"></span>
                    <span style="font-size:.82rem; font-weight:500;">{u['username']}</span>
                </div>
                """,
                unsafe_allow_html=True,
            )

    # ── Vulnerability history ─────────────────────────────────────────────────
    def _merge_vuln_reports(self, reports):
        combined = reports.copy() if reports else []
        saved_keys = {(r.get("vulnerabilidad"), r.get("dispositivo")) for r in combined}
        for sr in st.session_state.get("scan_results", []):
            key = (sr.get("vulnerabilidad"), sr.get("dispositivo"))
            if key not in saved_keys:
                combined.append(sr)
        severity_order = {"Critico": 0, "Crítico": 0, "Alto": 1, "Medio": 2, "Bajo": 3, "Info": 4}
        return sorted(combined, key=lambda r: (severity_order.get(r.get("nivel", "Info"), 99), r.get("fecha", "")))

    def _render_vuln_expander(self, vuln):
        nivel = vuln.get("nivel", "Info")
        icon = severity_icon(nivel)
        raw_fecha = vuln.get("fecha", "")
        fecha_str = str(raw_fecha)[:16].replace("T", " ") if raw_fecha else "Fecha no registrada"
        with st.expander(
            f"{icon}  [{nivel}]  {vuln.get('vulnerabilidad', 'Vulnerabilidad')}  ·  "
            f"📱 {vuln.get('dispositivo', 'Dispositivo')}  ·  📅 {fecha_str}"
        ):
            if vuln.get("categoria"):
                st.caption(f"📂 Categoría: **{vuln['categoria']}**")
            st.markdown(f"**📝 Explicación:**\n{vuln.get('descripcion', 'Sin descripción.')}")
            if vuln.get("implicacion"):
                st.markdown(f"**⚠️ Lo que implica (Riesgo):**\n{vuln['implicacion']}")
            if vuln.get("recommendation"):
                st.info(f"💡 **Recomendación:** {vuln['recommendation']}")
            refs = [v for v in [vuln.get("cwe"), vuln.get("owasp")] if v]
            if refs:
                st.caption("🔗 " + "  /  ".join(refs))

    def render_vulnerability_history(self, reports):
        st.markdown("## 🤖 Historial del agente móvil")
        st.markdown(
            "<div style='color:#64748b; font-size:.88rem; margin-bottom:1rem;'>"
            "Reportes de seguridad de dispositivos y análisis de red auxiliar.</div>",
            unsafe_allow_html=True,
        )
        combined_reports = self._merge_vuln_reports(reports)

        if not combined_reports:
            st.markdown(
                """
                <div style="text-align:center; padding:2rem; background:rgba(17,24,39,.6);
                            border:1px dashed rgba(0,212,255,.2); border-radius:12px; color:#64748b;">
                    <div style="font-size:2rem; margin-bottom:.5rem;">📡</div>
                    <div>Esperando reportes del agente móvil o escaneos manuales...</div>
                    <div style="font-size:.8rem; margin-top:.25rem;">
                        Realiza un escaneo manual o instala el APK en tu dispositivo para comenzar a recibir datos.
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            return

        df = pd.DataFrame(combined_reports)

        # ── Métricas rápidas ──────────────────────────────────────────────────
        total = len(df)
        criticos = len(df[df["nivel"].isin(["Critico", "Crítico"])]) if "nivel" in df.columns else 0
        altos    = len(df[df["nivel"] == "Alto"])                     if "nivel" in df.columns else 0
        dispositivos = df["dispositivo"].nunique()                    if "dispositivo" in df.columns else 0
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Total hallazgos",  total)
        m2.metric("Críticos",         criticos)
        m3.metric("Altos",            altos)
        m4.metric("Dispositivos",     dispositivos)

        st.divider()

        # ── Gráficos ──────────────────────────────────────────────────────────
        st.markdown("### 📊 Análisis visual")
        col_pie, col_bar = st.columns(2)

        severity_order = ["Critico", "Crítico", "Alto", "Medio", "Bajo", "Info"]
        severity_colors = {
            "Critico": "#ef4444", "Crítico": "#ef4444",
            "Alto":    "#f97316",
            "Medio":   "#eab308",
            "Bajo":    "#22c55e",
            "Info":    "#3b82f6",
        }

        if "nivel" in df.columns:
            nivel_counts = (
                df["nivel"]
                .value_counts()
                .reindex([s for s in severity_order if s in df["nivel"].values], fill_value=0)
                .reset_index()
            )
            nivel_counts.columns = ["Severidad", "Cantidad"]

            with col_pie:
                fig_pie = px.pie(
                    nivel_counts,
                    names="Severidad",
                    values="Cantidad",
                    title="Distribución por severidad",
                    color="Severidad",
                    color_discrete_map=severity_colors,
                    hole=0.4,
                )
                fig_pie.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    font_color="#e2e8f0",
                    legend=dict(font=dict(color="#e2e8f0")),
                )
                st.plotly_chart(fig_pie, use_container_width=True)

            with col_bar:
                fig_bar = px.bar(
                    nivel_counts,
                    x="Severidad",
                    y="Cantidad",
                    title="Hallazgos por nivel de riesgo",
                    color="Severidad",
                    color_discrete_map=severity_colors,
                    text="Cantidad",
                )
                fig_bar.update_traces(textposition="outside")
                fig_bar.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    font_color="#e2e8f0",
                    showlegend=False,
                    xaxis=dict(color="#e2e8f0"),
                    yaxis=dict(color="#e2e8f0", gridcolor="rgba(255,255,255,0.05)"),
                )
                st.plotly_chart(fig_bar, use_container_width=True)

        if "categoria" in df.columns and df["categoria"].str.strip().ne("").any():
            st.markdown("#### Hallazgos por categoría")
            cat_counts = (
                df[df["categoria"].str.strip().ne("")]
                ["categoria"]
                .value_counts()
                .reset_index()
            )
            cat_counts.columns = ["Categoría", "Cantidad"]
            fig_cat = px.bar(
                cat_counts,
                x="Cantidad",
                y="Categoría",
                orientation="h",
                title="Vulnerabilidades por categoría de análisis",
                color="Cantidad",
                color_continuous_scale=["#22c55e", "#eab308", "#ef4444"],
                text="Cantidad",
            )
            fig_cat.update_traces(textposition="outside")
            fig_cat.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font_color="#e2e8f0",
                xaxis=dict(color="#e2e8f0", gridcolor="rgba(255,255,255,0.05)"),
                yaxis=dict(color="#e2e8f0"),
                coloraxis_showscale=False,
            )
            st.plotly_chart(fig_cat, use_container_width=True)

        st.divider()

        # ── Tabla ─────────────────────────────────────────────────────────────
        display_cols = [c for c in ["dispositivo", "vulnerabilidad", "nivel", "categoria", "fecha"] if c in df.columns]
        st.markdown("### 📋 Vista general de hallazgos")
        st.dataframe(
            df[display_cols].rename(columns={
                "dispositivo": "Dispositivo",
                "vulnerabilidad": "Vulnerabilidad",
                "nivel": "Severidad",
                "categoria": "Categoría",
                "fecha": "Fecha",
            }),
            use_container_width=True,
            hide_index=True,
        )
        st.markdown("### 🔍 Detalle técnico y remediación")
        for vuln in combined_reports:
            self._render_vuln_expander(vuln)

    # ── Manual scan ───────────────────────────────────────────────────────────
    def render_manual_scan(self, controller):
        st.markdown("## 🔎 Escaneo manual auxiliar")
        st.markdown(
            "<div style='color:#64748b; font-size:.88rem; margin-bottom:1rem;'>"
            "Escanea una URL, IP o el dispositivo local en busca de vulnerabilidades de red.</div>",
            unsafe_allow_html=True,
        )
        col_input, col_btn = st.columns([3, 1])
        with col_input:
            target = st.text_input(
                "Objetivo",
                key="scan_target",
                placeholder="https://ejemplo.com · 192.168.1.1 · (vacío = local)",
                label_visibility="collapsed",
            )
        with col_btn:
            scan_btn = st.button("⚡  Escanear", key="scan_btn", use_container_width=True)

        if scan_btn:
            with st.spinner("🔍  Escaneando..."):
                user_id = st.session_state.user["id"]
                st.session_state.scan_results = controller.scan_vulnerabilities(
                    user_id, target if target else None
                )
                st.session_state.manual_scan_success = True
            st.rerun()

        if st.session_state.get("manual_scan_success") and st.session_state.get("scan_results"):
            st.success("✅ Análisis realizado correctamente y guardado en el historial del agente móvil.")
            st.markdown("### 📊 Resultados del escaneo")
            df = pd.DataFrame(st.session_state.scan_results)
            display_cols = [c for c in ["dispositivo", "vulnerabilidad", "nivel", "categoria"] if c in df.columns]
            if display_cols:
                st.dataframe(
                    df[display_cols].rename(columns={
                        "dispositivo": "Dispositivo",
                        "vulnerabilidad": "Vulnerabilidad",
                        "nivel": "Severidad",
                        "categoria": "Categoría",
                    }),
                    use_container_width=True,
                    hide_index=True,
                )
            st.markdown("#### Detalle técnico")
            for vuln in st.session_state.scan_results:
                self._render_vuln_expander(vuln)

    # ── Calidad de repositorio (GitHub) ──────────────────────────────────────
    def _render_file_card(self, fdata: dict) -> None:
        fname = fdata["file_path"].split("/")[-1]
        fpath = fdata["file_path"]
        metrics = fdata.get("metrics", {})
        smells = fdata.get("smells", [])
        loc = fdata.get("loc", 0)
        complexity = fdata.get("complexity", 0)
        nom = metrics.get("nom", 0)
        noa = metrics.get("noa", 0)
        smell_color = "#ffa502" if smells else "#00ff88"
        smell_icon = "⚠️" if smells else "✅"
        smell_label = f"{len(smells)} problema{'s' if len(smells) != 1 else ''}"

        st.markdown(
            f"""
            <div style="background:rgba(17,24,39,.9);border:1px solid rgba(0,212,255,.2);
                        border-radius:10px;padding:.75rem 1rem;">
              <div style="font-weight:700;font-size:.88rem;color:#e2e8f0;
                          white-space:nowrap;overflow:hidden;text-overflow:ellipsis;"
                   title="{fpath}">{fname}</div>
              <div style="font-size:.65rem;color:#64748b;margin:.1rem 0 .6rem;
                          white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">{fpath}</div>
              <div style="display:grid;grid-template-columns:1fr 1fr;gap:3px;">
                <div style="background:rgba(0,150,180,.12);border-radius:5px;
                            padding:.25rem .45rem;display:flex;justify-content:space-between;">
                  <span style="color:#64748b;font-size:.72rem;">LOC</span>
                  <span style="color:#00d4ff;font-weight:700;font-size:.78rem;">{loc}</span>
                </div>
                <div style="background:rgba(255,71,87,.1);border-radius:5px;
                            padding:.25rem .45rem;display:flex;justify-content:space-between;">
                  <span style="color:#64748b;font-size:.72rem;">Complejidad</span>
                  <span style="color:#ff4757;font-weight:700;font-size:.78rem;">{complexity}</span>
                </div>
                <div style="background:rgba(0,150,180,.12);border-radius:5px;
                            padding:.25rem .45rem;display:flex;justify-content:space-between;">
                  <span style="color:#64748b;font-size:.72rem;">Métodos</span>
                  <span style="color:#00d4ff;font-weight:700;font-size:.78rem;">{nom}</span>
                </div>
                <div style="background:rgba(255,165,2,.08);border-radius:5px;
                            padding:.25rem .45rem;display:flex;justify-content:space-between;">
                  <span style="color:#64748b;font-size:.72rem;">Atributos</span>
                  <span style="color:#ffa502;font-weight:700;font-size:.78rem;">{noa}</span>
                </div>
              </div>
              <div style="margin-top:.5rem;font-size:.72rem;color:{smell_color};font-weight:600;">
                {smell_icon} {smell_label}
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if smells:
            with st.expander(f"Problemas ({len(smells)})", expanded=False):
                for smell in smells[:10]:
                    st.caption(f"• {smell}")

    def _filter_sort_files(self, files: list, search: str, sort_opt: str) -> list:
        visible = [f for f in files if search.lower() in f["file_path"].lower()] if search else files[:]
        if sort_opt == "A-Z":
            visible.sort(key=lambda x: x["file_path"].split("/")[-1].lower())
        elif sort_opt == "Z-A":
            visible.sort(key=lambda x: x["file_path"].split("/")[-1].lower(), reverse=True)
        elif sort_opt == "LOC ↑":
            visible.sort(key=lambda x: x.get("loc", 0))
        else:
            visible.sort(key=lambda x: x.get("loc", 0), reverse=True)
        return visible

    def _render_file_row(self, f: dict, is_checked: bool, is_disabled: bool) -> bool:
        fpath = f["file_path"]
        c_cb, c_name, c_loc = st.columns([1, 6, 2])
        with c_cb:
            val = st.checkbox(
                "", value=is_checked, disabled=is_disabled,
                key=f"rcb__{fpath}", label_visibility="collapsed",
            )
        with c_name:
            if is_checked:
                color = "#00d4ff"
            elif is_disabled:
                color = "#475569"
            else:
                color = "#cbd5e1"
            st.markdown(
                f"<div style='font-size:.8rem;padding-top:.3rem;color:{color};'>"
                f"{fpath.split('/')[-1]}</div>",
                unsafe_allow_html=True,
            )
        with c_loc:
            st.markdown(
                f"<div style='font-size:.75rem;padding-top:.32rem;color:#64748b;text-align:right;'>"
                f"{f.get('loc', 0)}</div>",
                unsafe_allow_html=True,
            )
        return val

    def _render_file_detail(self, files: list) -> None:
        st.markdown("---")
        st.markdown(
            f"<div style='display:flex;align-items:center;gap:.5rem;margin-bottom:.5rem;'>"
            f"<span style='font-size:.95rem;font-weight:700;color:#e2e8f0;'>📁 Detalle por archivos</span>"
            f"<span style='background:rgba(0,212,255,.1);color:#00d4ff;border:1px solid rgba(0,212,255,.2);"
            f"border-radius:20px;padding:1px 8px;font-size:.68rem;font-weight:600;'>{len(files)}</span>"
            f"<span style='color:#64748b;font-size:.7rem;'>Selecciona hasta 2 para comparar</span>"
            f"</div>",
            unsafe_allow_html=True,
        )

        if "repo_sel_paths" not in st.session_state:
            st.session_state.repo_sel_paths = set()

        left, right = st.columns([1, 3])

        with left:
            col_s, col_o = st.columns([3, 2])
            search = col_s.text_input(
                "Filtrar", placeholder="🔍 Filtrar...",
                key="repo_file_search", label_visibility="collapsed",
            )
            sort_opt = col_o.selectbox(
                "Orden", ["A-Z", "Z-A", "LOC ↑", "LOC ↓"],
                key="repo_file_sort", label_visibility="collapsed",
            )
            visible = self._filter_sort_files(files, search, sort_opt)
            sel_paths = st.session_state.repo_sel_paths
            max_reached = len(sel_paths) >= 2

            table_height = min(420, max(150, len(visible) * 35 + 40))
            with st.container(height=table_height):
                for f in visible:
                    fpath = f["file_path"]
                    is_checked = fpath in sel_paths
                    val = self._render_file_row(f, is_checked, max_reached and not is_checked)
                    if val and not is_checked:
                        st.session_state.repo_sel_paths.add(fpath)
                        st.rerun()
                    elif not val and is_checked:
                        st.session_state.repo_sel_paths.discard(fpath)
                        st.rerun()

            selected = [f for f in visible if f["file_path"] in st.session_state.repo_sel_paths]

        with right:
            if not selected:
                st.markdown(
                    "<div style='height:140px;display:flex;align-items:center;justify-content:center;"
                    "background:rgba(17,24,39,.4);border:1px dashed rgba(0,212,255,.12);"
                    "border-radius:10px;color:#64748b;font-size:.82rem;text-align:center;'>"
                    "👈 Selecciona un archivo de la lista para ver su detalle</div>",
                    unsafe_allow_html=True,
                )
            else:
                card_cols = st.columns(len(selected))
                for i, fdata in enumerate(selected):
                    with card_cols[i]:
                        self._render_file_card(fdata)

    def render_repo_quality(self, controller):
        st.markdown("## 📦 Analizador Estático")
        tab_archivo, tab_carpeta, tab_repo = st.tabs(["📄 Archivo Local", "📂 Carpeta Local", "🐙 Repositorio GitHub"])

        with tab_archivo:
            self._render_repo_archivo_local(controller)

        with tab_carpeta:
            self._render_repo_carpeta_local(controller)

        with tab_repo:
            self._render_repo_github(controller)

        result = st.session_state.get("repo_quality_result")
        if result:
            st.success(f"✅ Análisis completado: {result.get('proyecto') or '-'}")
            c1, c2, c3 = st.columns(3)
            c1.metric("📏 Líneas de código", result.get("lineas_codigo", "-"))
            c2.metric("🧩 Complejidad", result.get("complejidad", "-"))
            c3.metric("🐞 Code smells", result.get("code_smells", "-"))
            files = result.get("files", [])
            if files:
                _file_detail_frag(self, files)

    def _render_repo_archivo_local(self, controller):
        st.markdown(
            "<div style='color:#64748b; font-size:.88rem; margin-bottom:.8rem;'>"
            "Sube un archivo de código para analizar su calidad y detectar code smells.</div>",
            unsafe_allow_html=True,
        )
        uploaded = st.file_uploader("Seleccionar archivo", key="repo_archivo_upload", label_visibility="collapsed")
        analizar_btn = st.button(self._BTN_ANALIZAR, key="repo_archivo_btn", use_container_width=True, disabled=uploaded is None)
        if analizar_btn and uploaded:
            with st.spinner("⚙️ Analizando archivo... (puede tardar si el servicio está inactivo)"):
                ok, result = controller.analizar_carpeta_local(uploaded.name, [uploaded])
            if ok:
                st.session_state.repo_quality_result = result
                st.session_state.repo_sel_paths = set()
            else:
                st.session_state.repo_quality_result = None
                st.error(f"❌ {result}")

    def _render_repo_carpeta_local(self, controller):
        st.markdown(
            "<div style='color:#64748b; font-size:.88rem; margin-bottom:.8rem;'>"
            "Sube múltiples archivos de un proyecto para analizar la calidad del conjunto.</div>",
            unsafe_allow_html=True,
        )
        project_name = st.text_input(
            "Nombre del proyecto", key="repo_project_name",
            placeholder="Mi Proyecto", label_visibility="collapsed",
        )
        uploaded_files = st.file_uploader(
            "Seleccionar archivos o arrastra una carpeta", key="repo_carpeta_upload",
            accept_multiple_files=True, label_visibility="collapsed",
        )
        import streamlit.components.v1 as components
        components.html("""<script>
(function(){
    function applyDir(){
        var inputs=window.parent.document.querySelectorAll('input[type="file"][multiple]');
        inputs.forEach(function(el){
            el.setAttribute('webkitdirectory','');
            el.setAttribute('directory','');
        });
    }
    applyDir();
    new MutationObserver(applyDir).observe(window.parent.document.body,{childList:true,subtree:true});
})();
</script>""", height=0)
        analizar_btn = st.button(self._BTN_ANALIZAR, key="repo_carpeta_btn", use_container_width=True, disabled=not uploaded_files)
        if analizar_btn and uploaded_files:
            name = project_name.strip() or "Proyecto"
            with st.spinner(f"⚙️ Analizando {len(uploaded_files)} archivos... (puede tardar si el servicio está inactivo)"):
                ok, result = controller.analizar_carpeta_local(name, uploaded_files)
            if ok:
                st.session_state.repo_quality_result = result
                st.session_state.repo_sel_paths = set()
            else:
                st.session_state.repo_quality_result = None
                st.error(f"❌ {result}")

    def _render_repo_github(self, controller):
        st.markdown(
            "<div style='color:#64748b; font-size:.88rem; margin-bottom:.8rem;'>"
            "Analiza un repositorio público de GitHub consumiendo el servicio externo.</div>",
            unsafe_allow_html=True,
        )
        col_input, col_btn = st.columns([3, 1])
        with col_input:
            repo_url = st.text_input(
                "Repositorio de GitHub", key="repo_github_url",
                placeholder="https://github.com/usuario/repo", label_visibility="collapsed",
            )
        with col_btn:
            analizar_btn = st.button(self._BTN_ANALIZAR, key="repo_github_btn", use_container_width=True)
        if analizar_btn:
            if not repo_url:
                st.warning("Ingresa la URL de un repositorio de GitHub.")
            else:
                with st.spinner("⚙️ Analizando repositorio... (puede tardar hasta 3 min si el servicio está inactivo)"):
                    ok, result = controller.analizar_repo_github(repo_url)
                if ok:
                    st.session_state.repo_quality_result = result
                    st.session_state.repo_sel_paths = set()
                else:
                    st.session_state.repo_quality_result = None
                    st.error(f"❌ {result}")

    # ── API de Seguridad Externa ──────────────────────────────────────────────
    def render_api_externa(self, controller):
        st.markdown("## 🔗 OWASP Verificator")
        st.markdown(
            "<div style='color:#64748b; font-size:.88rem; margin-bottom:1.5rem;'>"
            "Analiza código, URLs, archivos o repositorios mediante el servicio externo de seguridad."
            "</div>",
            unsafe_allow_html=True,
        )

        tab_nuevo, tab_historial = st.tabs(["🆕 Nuevo análisis", "📋 Historial de reportes"])

        with tab_nuevo:
            self._render_ext_new_analysis(controller)

        with tab_historial:
            self._render_ext_reports(controller)

    def _ext_get_target_value(self, tipo: str) -> str:
        if tipo == "code":
            return st.text_area(
                "Código", placeholder="Pega tu código aquí...", height=160,
                key="ext_code_input", label_visibility="collapsed",
            ) or ""
        if tipo == "url":
            return st.text_input(
                "URL", placeholder="https://example.com",
                key="ext_url_input", label_visibility="collapsed",
            ) or ""
        if tipo == "archivo":
            uploaded = st.file_uploader("Archivo", key="ext_file_input", label_visibility="collapsed")
            return uploaded.read().decode("utf-8", errors="replace") if uploaded else ""
        return st.text_input(
            "Repositorio", placeholder="https://github.com/usuario/repo",
            key="ext_repo_input", label_visibility="collapsed",
        ) or ""

    def _render_ext_new_analysis(self, controller):
        st.markdown(
            "<div style='font-size:.75rem; color:#64748b; text-transform:uppercase;"
            " letter-spacing:.08em; margin:.75rem 0 .4rem;'>TIPO DE OBJETIVO</div>",
            unsafe_allow_html=True,
        )

        tipo_map = {"Código": "code", "URL": "url", "Archivo": "archivo", "Repositorio de GitHub": "github_repo"}
        tipo_label = st.selectbox(
            "Tipo de objetivo", list(tipo_map.keys()), key="ext_tipo", label_visibility="collapsed",
        )
        tipo = tipo_map[tipo_label]
        target_value = self._ext_get_target_value(tipo)

        st.markdown("<div style='height:.5rem'></div>", unsafe_allow_html=True)
        if st.button("Analizar", key="ext_analizar_btn", use_container_width=True):
            if not target_value:
                st.warning("Ingresa el objetivo a analizar.")
            else:
                with st.spinner("Analizando..."):
                    ok, result = controller.analizar_con_api_externa(tipo, target_value)
                if ok:
                    st.session_state.ext_analysis_result = result
                else:
                    st.error(f"❌ {result}")

        result = st.session_state.get("ext_analysis_result")
        if result:
            self._render_ext_result(result)

    def _render_ext_result(self, result):
        st.divider()
        st.markdown("### Resultado del análisis")

        score = result.get("score", 0)
        status = result.get("status", "-")
        findings = result.get("findings", [])

        if score >= 80:
            color = "#00ff88"
        elif score >= 50:
            color = "#ffa502"
        else:
            color = "#ff4757"
        c1, c2, c3 = st.columns(3)
        c1.markdown(
            f"""
            <div style="background:rgba(0,0,0,.3); border:1px solid rgba(255,255,255,.08);
                        border-radius:10px; padding:1rem; text-align:center;">
                <div style="font-size:.75rem; color:#64748b; text-transform:uppercase;
                            letter-spacing:.06em; margin-bottom:.4rem;">Score de seguridad</div>
                <div style="font-size:2rem; font-weight:800; color:{color};">{score}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        c2.metric("Estado", status.capitalize())
        c3.metric("Hallazgos", len(findings))

        if not findings:
            st.success("No se encontraron hallazgos de seguridad.")
            return

        st.markdown("#### Hallazgos")
        for f in findings:
            self._render_ext_finding_expander(f)

    _SEV_ICON = {"critical": "🔴", "high": "🔴", "medium": "🟡", "low": "🟢"}
    _SEV_COLOR = {"critical": "#ff4757", "high": "#ff6b81", "medium": "#ffa502", "low": "#00ff88"}

    @staticmethod
    def _score_color(score: int) -> str:
        if score >= 80:
            return "#00ff88"
        if score >= 50:
            return "#ffa502"
        return "#ff4757"

    def _render_ext_finding_expander(self, f: dict) -> None:
        sev = f.get("severity", "info").lower()
        icon = self._SEV_ICON.get(sev, "⚪")
        color_sev = self._SEV_COLOR.get(sev, "#94a3b8")
        rule = f.get("rule_id", "")
        title = f.get("title", "Hallazgo")
        rule_prefix = f"[{rule}] " if rule else ""
        with st.expander(f"{icon} **{rule_prefix}{title}**"):
            st.markdown(
                f"<span style='color:{color_sev}; font-weight:700;"
                f" text-transform:uppercase; font-size:.75rem;'>{sev}</span>",
                unsafe_allow_html=True,
            )
            if f.get("description"):
                st.markdown(f["description"])
            if f.get("evidence"):
                st.code(f["evidence"])

    def _render_ext_finding_line(self, f: dict) -> None:
        sev = f.get("severity", "info").lower()
        icon = self._SEV_ICON.get(sev, "⚪")
        col_sev = self._SEV_COLOR.get(sev, "#94a3b8")
        rule = f.get("rule_id", "")
        title = f.get("title", "")
        rule_prefix = f"[{rule}] " if rule else ""
        st.markdown(
            f"{icon} <span style='color:{col_sev};font-weight:700;"
            f"text-transform:uppercase;font-size:.72rem;'>{sev}</span> "
            f"**{rule_prefix}{title}** — {f.get('description', '')}",
            unsafe_allow_html=True,
        )

    def _render_ext_report_card(self, rep: dict) -> None:
        score = rep.get("score", 0)
        tipo = rep.get("target_type", "-")
        status = rep.get("status", "-")
        rid = rep.get("id", "")
        findings = rep.get("findings", [])
        color = self._score_color(score)

        with st.expander(f"#{rid} — {tipo.upper()} — Score: {score} — {len(findings)} hallazgos"):
            col_s, col_t, col_f = st.columns(3)
            col_s.markdown(
                f"<div style='text-align:center;'>"
                f"<div style='font-size:.7rem;color:#64748b;'>Score</div>"
                f"<div style='font-size:1.6rem;font-weight:800;color:{color};'>{score}</div></div>",
                unsafe_allow_html=True,
            )
            col_t.metric("Tipo", tipo)
            col_f.metric("Estado", status.capitalize())

            target_val = rep.get("target_value", "")
            if target_val:
                st.markdown("**Objetivo:**")
                if tipo in ("url", "github_repo"):
                    st.markdown(f"`{target_val}`")
                else:
                    preview = target_val[:300] + ("..." if len(target_val) > 300 else "")
                    st.code(preview)

            if findings:
                st.markdown("**Hallazgos:**")
                for f in findings:
                    self._render_ext_finding_line(f)

    def _render_ext_reports(self, controller):
        if st.button("🔄 Cargar reportes", key="ext_load_reports"):
            with st.spinner("Cargando reportes..."):
                ok, data = controller.get_reportes_api_externa()
            if ok:
                st.session_state.ext_reports = data
            else:
                st.error(f"❌ {data}")

        reports = st.session_state.get("ext_reports")
        if reports is None:
            st.info("Presiona 'Cargar reportes' para ver el historial.")
            return
        if not reports:
            st.info("No hay reportes disponibles aún.")
            return

        for rep in reports:
            self._render_ext_report_card(rep)
