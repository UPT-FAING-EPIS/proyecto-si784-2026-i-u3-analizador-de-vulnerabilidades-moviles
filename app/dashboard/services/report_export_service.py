import json
from datetime import datetime, timezone
import html

from app.dashboard.config.kb import APK_FINDING_KB, APK_ARTIFACT_KB


class ReportExportService:
    def build_filename(self, scan, extension):
        scan_id = str(scan.get("id", "scan"))[:8]
        base_name = scan.get("file_name", "apk_scan").replace(".apk", "")
        safe_name = "".join(
            char if char.isalnum() or char in ("-", "_") else "_"
            for char in base_name
        )
        return f"anzencore_{safe_name}_{scan_id}.{extension}"

    def build_export_log(self, scan, user_id, export_format, file_name):
        return {
            "scan_id": scan["id"],
            "user_id": user_id,
            "export_format": export_format,
            "file_name": file_name,
        }

    def build_pdf(self, scan, findings, artifacts):
        from reportlab.lib.pagesizes import letter
        from reportlab.lib import colors
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
        from app.dashboard.config.kb import APK_FINDING_KB, APK_ARTIFACT_KB
        from io import BytesIO
        
        def safe_str(val, default="N/A", escape=True, newline_to_br=False):
            if val is None:
                return default
            s = str(val).strip()
            if not s:
                return default
            if escape:
                s = html.escape(s)
            if newline_to_br:
                s = s.replace("\n", "<br/>")
            return s

        buffer = BytesIO()
        
        # Tamaño de página y márgenes
        doc = SimpleDocTemplate(
            buffer,
            pagesize=letter,
            rightMargin=54,
            leftMargin=54,
            topMargin=54,
            bottomMargin=60
        )
        
        styles = getSampleStyleSheet()
        
        # Estilos tipográficos personalizados
        title_style = ParagraphStyle(
            "ReportTitle",
            parent=styles["Title"],
            fontName="Helvetica-Bold",
            fontSize=22,
            textColor=colors.HexColor("#0284c7"),
            alignment=TA_LEFT,
            spaceAfter=15
        )
        
        subtitle_style = ParagraphStyle(
            "ReportSubtitle",
            parent=styles["Normal"],
            fontName="Helvetica",
            fontSize=10,
            textColor=colors.HexColor("#64748b"),
            spaceAfter=20
        )
        
        h1_style = ParagraphStyle(
            "SectionH1",
            parent=styles["Heading1"],
            fontName="Helvetica-Bold",
            fontSize=14,
            textColor=colors.HexColor("#0f172a"),
            spaceBefore=15,
            spaceAfter=10
        )

        h2_style = ParagraphStyle(
            "SectionH2",
            parent=styles["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=11,
            textColor=colors.HexColor("#0284c7"),
            spaceBefore=10,
            spaceAfter=5
        )

        body_style = ParagraphStyle(
            "BodyTextCustom",
            parent=styles["BodyText"],
            fontName="Helvetica",
            fontSize=9,
            textColor=colors.HexColor("#334155"),
            leading=13,
            spaceAfter=8
        )
        
        bold_style = ParagraphStyle(
            "BoldTextCustom",
            parent=body_style,
            fontName="Helvetica-Bold"
        )

        code_style = ParagraphStyle(
            "MonospaceCode",
            parent=styles["Normal"],
            fontName="Courier",
            fontSize=8,
            textColor=colors.HexColor("#0f172a"),
            leading=10,
            spaceAfter=10
        )
        
        # Colores para severidades (esquema de alto contraste)
        sev_colors = {
            "Critico": "#dc2626",
            "Crítico": "#dc2626",
            "Alto": "#ea580c",
            "Medio": "#d97706",
            "Bajo": "#16a34a",
            "Info": "#2563eb"
        }
        
        story = []
        
        # 1. Cabecera principal
        story.append(Paragraph("AnzenCore", title_style))
        story.append(Paragraph("Reporte de Auditoría de Seguridad de Aplicación Móvil", subtitle_style))
        story.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor("#0284c7"), spaceBefore=0, spaceAfter=20))
        
        # 2. Resumen General (Metadata del análisis)
        story.append(Paragraph("Resumen del Escaneo", h1_style))
        
        file_size = scan.get("file_size_bytes")
        if file_size is None:
            file_size = 0
        file_size_mb = file_size / (1024 * 1024)
        
        meta_data = [
            [Paragraph("<b>Aplicación:</b>", body_style), Paragraph(safe_str(scan.get("app_name"), "N/A"), body_style)],
            [Paragraph("<b>Paquete:</b>", body_style), Paragraph(safe_str(scan.get("package_name"), "N/A"), body_style)],
            [Paragraph("<b>Versión:</b>", body_style), Paragraph(f"{safe_str(scan.get('version_name'), 'N/A')} (Código: {safe_str(scan.get('version_code'), 'N/A')})", body_style)],
            [Paragraph("<b>Nombre de archivo:</b>", body_style), Paragraph(safe_str(scan.get("file_name"), "N/A"), body_style)],
            [Paragraph("<b>Tamaño de archivo:</b>", body_style), Paragraph(f"{file_size_mb:.2f} MB", body_style)],
            [Paragraph("<b>Hash SHA-256:</b>", body_style), Paragraph(safe_str(scan.get("file_hash_sha256"), "N/A"), body_style)],
            [Paragraph("<b>Fecha de análisis:</b>", body_style), Paragraph(safe_str(scan.get("created_at"), "N/A")[:19].replace("T", " "), body_style)],
            [Paragraph("<b>Máxima Severidad:</b>", body_style), Paragraph(f"<font color='{sev_colors.get(safe_str(scan.get('severity_max'), 'N/A'), '#334155')}'><b>{safe_str(scan.get('severity_max'), 'N/A')}</b></font>", body_style)],
            [Paragraph("<b>Hallazgos totales:</b>", body_style), Paragraph(str(scan.get("findings_count") if scan.get("findings_count") is not None else 0), body_style)]
        ]
        
        meta_table = Table(meta_data, colWidths=[140, 364])
        meta_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#f8fafc")),
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('PADDING', (0,0), (-1,-1), 6),
            ('BOTTOMPADDING', (0,0), (-1,-1), 6),
            ('TOPPADDING', (0,0), (-1,-1), 6),
            ('LEFTPADDING', (0,0), (-1,-1), 10),
            ('RIGHTPADDING', (0,0), (-1,-1), 10),
            ('LINEBELOW', (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")),
            ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#0284c7"))
        ]))
        
        story.append(meta_table)
        story.append(Spacer(1, 20))
        
        # 3. Hallazgos Detallados
        story.append(PageBreak())
        story.append(Paragraph("Hallazgos de Seguridad", h1_style))
        story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#e2e8f0"), spaceBefore=0, spaceAfter=15))
        
        if not findings:
            story.append(Paragraph("No se encontraron hallazgos registrados para esta aplicación.", body_style))
        else:
            severity_order = {"Critico": 0, "Crítico": 0, "Alto": 1, "Medio": 2, "Bajo": 3, "Info": 4}
            sorted_findings = sorted(findings, key=lambda i: severity_order.get(i.get("severity"), 99))
            
            for finding in sorted_findings:
                severity = safe_str(finding.get("severity"), "Info")
                color_hex = sev_colors.get(severity, "#334155")
                
                finding_flowables = []
                
                # Encabezado del hallazgo
                title = safe_str(finding.get("title"), "Hallazgo")
                finding_flowables.append(Paragraph(
                    f"<b>[{severity.upper()}] {title}</b>",
                    ParagraphStyle("FindingTitle", parent=h2_style, textColor=colors.HexColor(color_hex))
                ))
                
                # Datos del hallazgo
                finding_type = safe_str(finding.get("finding_type"), "N/A")
                meta_finding_text = f"<b>Tipo:</b> {finding_type}"
                source_file = safe_str(finding.get("source_file"), "")
                if source_file:
                    meta_finding_text += f"  |  <b>Fuente:</b> {source_file}"
                
                cwe_val = safe_str(finding.get("cwe"), "")
                owasp_val = safe_str(finding.get("owasp_mobile"), "")
                refs = [v for v in [cwe_val, owasp_val] if v]
                if refs:
                    meta_finding_text += f"  |  <b>Referencias:</b> {' / '.join(refs)}"
                    
                finding_flowables.append(Paragraph(meta_finding_text, ParagraphStyle("FindingMeta", parent=body_style, fontSize=8, textColor=colors.HexColor("#64748b"))))
                finding_flowables.append(Spacer(1, 4))
                
                # Explicación
                finding_flowables.append(Paragraph(f"<b>Explicación:</b>", bold_style))
                description = safe_str(finding.get("description"), "Sin descripción.", newline_to_br=True)
                finding_flowables.append(Paragraph(description, body_style))
                
                # Implicación
                f_type = safe_str(finding.get("finding_type"), "")
                kb_info = APK_FINDING_KB.get(f_type, {})
                implicacion = safe_str(kb_info.get("implicacion"), "")
                if implicacion:
                    finding_flowables.append(Paragraph(f"<b>Lo que implica (Riesgo):</b>", bold_style))
                    finding_flowables.append(Paragraph(implicacion, body_style))
                    
                # Recomendación
                rec_val = finding.get("recommendation")
                if rec_val is None or not str(rec_val).strip():
                    rec_val = kb_info.get("recommendation")
                rec_safe = safe_str(rec_val, "", newline_to_br=True)
                if rec_safe:
                    finding_flowables.append(Paragraph(f"<b>Recomendación:</b>", bold_style))
                    finding_flowables.append(Paragraph(rec_safe, body_style))
                    
                # Evidencia (código monoespacio)
                evidence_raw = finding.get("evidence")
                if evidence_raw and str(evidence_raw).strip():
                    finding_flowables.append(Paragraph(f"<b>Evidencia encontrada:</b>", bold_style))
                    evidence_safe = safe_str(evidence_raw, "", escape=True, newline_to_br=True)
                    evidence_html = evidence_safe.replace(" ", "&nbsp;")
                    evidence_p = Paragraph(evidence_html, code_style)
                    evidence_table = Table([[evidence_p]], colWidths=[504])
                    evidence_table.setStyle(TableStyle([
                        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#f8fafc")),
                        ('PADDING', (0,0), (-1,-1), 8),
                        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0"))
                    ]))
                    finding_flowables.append(evidence_table)
                    finding_flowables.append(Spacer(1, 5))
                
                finding_flowables.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#e2e8f0"), spaceBefore=10, spaceAfter=15))
                
                # Agregar el bloque agrupado en KeepTogether para prevenir saltos de página partidos
                story.append(KeepTogether(finding_flowables))
                
        # 4. Artefactos Extraídos
        story.append(PageBreak())
        story.append(Paragraph("Artefactos de la Aplicación", h1_style))
        story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#e2e8f0"), spaceBefore=0, spaceAfter=15))
        
        if not artifacts:
            story.append(Paragraph("No se registraron artefactos en esta aplicación.", body_style))
        else:
            art_data = [[Paragraph("<b>Tipo</b>", bold_style), Paragraph("<b>Valor</b>", bold_style), Paragraph("<b>Fuente</b>", bold_style)]]
            for artifact in artifacts:
                art_type = safe_str(artifact.get("artifact_type"), "N/A")
                art_value = safe_str(artifact.get("artifact_value"), "N/A", newline_to_br=True)
                art_source = safe_str(artifact.get("source_file"), "None")
                art_data.append([
                    Paragraph(art_type, body_style),
                    Paragraph(art_value, body_style),
                    Paragraph(art_source, body_style)
                ])
                
            art_table = Table(art_data, colWidths=[100, 244, 160])
            art_table.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#f8fafc")),
                ('VALIGN', (0,0), (-1,-1), 'TOP'),
                ('PADDING', (0,0), (-1,-1), 5),
                ('LEFTPADDING', (0,0), (-1,-1), 8),
                ('LINEBELOW', (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")),
                ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0"))
            ]))
            story.append(art_table)
            story.append(Spacer(1, 20))
            
            # Guía técnica de artefactos
            story.append(Paragraph("Guía Técnica de Artefactos Extraídos", h1_style))
            story.append(Spacer(1, 8))
            
            unique_types = sorted(list({safe_str(a.get("artifact_type"), "") for a in artifacts if a.get("artifact_type")}))
            for a_type in unique_types:
                if not a_type:
                    continue
                kb_info = APK_ARTIFACT_KB.get(a_type)
                if kb_info:
                    art_flow = []
                    art_title = safe_str(kb_info.get("titulo"), "Artefacto")
                    art_desc = safe_str(kb_info.get("descripcion"), "")
                    art_rec = safe_str(kb_info.get("recommendation"), "")
                    
                    art_flow.append(Paragraph(f"<b>📁 {art_title} ({a_type})</b>", h2_style))
                    if art_desc:
                        art_flow.append(Paragraph(f"<b>Explicación:</b> {art_desc}", body_style))
                    if art_rec:
                        art_flow.append(Paragraph(f"<b>Recomendación:</b> {art_rec}", body_style))
                    art_flow.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#e2e8f0"), spaceBefore=5, spaceAfter=10))
                    story.append(KeepTogether(art_flow))
                    
        # Callback para pintar pie de página y cabecera
        def add_header_footer(canvas, doc):
            canvas.saveState()
            
            # Cabecera
            canvas.setStrokeColor(colors.HexColor("#0284c7"))
            canvas.setLineWidth(0.5)
            canvas.line(54, 750, 558, 750)
            
            canvas.setFont("Helvetica-Bold", 8)
            canvas.setFillColor(colors.HexColor("#0284c7"))
            canvas.drawString(54, 755, "AnzenCore Security Audit Report")
            
            # Pie de página
            canvas.setStrokeColor(colors.HexColor("#e2e8f0"))
            canvas.line(54, 50, 558, 50)
            
            canvas.setFont("Helvetica", 8)
            canvas.setFillColor(colors.HexColor("#64748b"))
            canvas.drawString(54, 38, f"Generado el: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
            canvas.drawRightString(558, 38, f"Página {doc.page}")
            
            canvas.restoreState()
            
        # Generar el PDF
        doc.build(story, onFirstPage=add_header_footer, onLaterPages=add_header_footer)
        
        pdf_bytes = buffer.getvalue()
        buffer.close()
        return pdf_bytes
