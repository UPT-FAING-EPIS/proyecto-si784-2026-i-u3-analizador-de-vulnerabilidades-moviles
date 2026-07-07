import * as vscode from "vscode";
import type { ApkArtifact, ApkFinding, Severity } from "./apkAnalyzer";

export interface ApkReport {
  fileName: string;
  sizeBytes: number;
  sha256: string;
  summary: string;
  severityMax: Severity;
  findings: ApkFinding[];
  artifacts: ApkArtifact[];
}

const SEVERITY_ORDER: Record<Severity, number> = {
  Info: 0,
  Bajo: 1,
  Medio: 2,
  Alto: 3,
  Critico: 4,
};

const SEVERITY_COLOR_VAR: Record<Severity, string> = {
  Critico: "--vscode-editorError-foreground",
  Alto: "--vscode-editorError-foreground",
  Medio: "--vscode-editorWarning-foreground",
  Bajo: "--vscode-editorInfo-foreground",
  Info: "--vscode-descriptionForeground",
};

function escapeHtml(value: string): string {
  return value
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

function renderInline(text: string): string {
  return text.replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>").replace(/\n/g, "<br>");
}

function renderMarkdownLite(raw: string): string {
  const escaped = escapeHtml(raw);
  const codeBlockRegex = /```(\w*)\n([\s\S]*?)```/g;
  let result = "";
  let lastIndex = 0;
  let match: RegExpExecArray | null;
  while ((match = codeBlockRegex.exec(escaped))) {
    result += renderInline(escaped.slice(lastIndex, match.index));
    result += `<pre><code>${match[2]}</code></pre>`;
    lastIndex = codeBlockRegex.lastIndex;
  }
  result += renderInline(escaped.slice(lastIndex));
  return result;
}

export class VulnerabilitiesPanel {
  private static current: VulnerabilitiesPanel | undefined;
  private readonly panel: vscode.WebviewPanel;

  private constructor(panel: vscode.WebviewPanel) {
    this.panel = panel;
    this.panel.onDidDispose(() => {
      VulnerabilitiesPanel.current = undefined;
    });
  }

  static show(report: ApkReport): void {
    if (VulnerabilitiesPanel.current) {
      VulnerabilitiesPanel.current.panel.reveal();
    } else {
      const panel = vscode.window.createWebviewPanel(
        "anzencoreVulnerabilities",
        "AnzenCore: Vulnerabilidades",
        vscode.ViewColumn.Beside,
        { enableScripts: true, retainContextWhenHidden: true }
      );
      VulnerabilitiesPanel.current = new VulnerabilitiesPanel(panel);
    }
    VulnerabilitiesPanel.current.render(report);
  }

  private render(report: ApkReport): void {
    this.panel.title = `AnzenCore: ${report.fileName}`;
    this.panel.webview.html = this.buildHtml(report);
  }

  private buildHtml(report: ApkReport): string {
    const conteo: Record<Severity, number> = { Critico: 0, Alto: 0, Medio: 0, Bajo: 0, Info: 0 };
    for (const f of report.findings) {
      conteo[f.severity] += 1;
    }

    const sorted = [...report.findings].sort(
      (a, b) => SEVERITY_ORDER[b.severity] - SEVERITY_ORDER[a.severity]
    );

    const chips = (Object.keys(conteo) as Severity[])
      .filter((sev) => conteo[sev] > 0)
      .map(
        (sev) =>
          `<span class="chip" style="border-color: var(${SEVERITY_COLOR_VAR[sev]}); color: var(${SEVERITY_COLOR_VAR[sev]})">${sev}: ${conteo[sev]}</span>`
      )
      .join(" ");

    const findingsHtml = sorted
      .map((f) => {
        const badges = [
          f.cwe ? `<span class="badge">${escapeHtml(f.cwe)}</span>` : "",
          f.owaspMobile ? `<span class="badge">OWASP ${escapeHtml(f.owaspMobile)}</span>` : "",
          f.sourceFile ? `<span class="badge muted">${escapeHtml(f.sourceFile)}</span>` : "",
        ].join(" ");

        return `<details class="finding">
          <summary>
            <span class="severity" style="color: var(${SEVERITY_COLOR_VAR[f.severity]})">${f.severity}</span>
            <span class="title">${escapeHtml(f.title)}</span>
          </summary>
          <div class="finding-body">
            <div class="badges">${badges}</div>
            <p>${escapeHtml(f.description)}</p>
            ${f.evidence ? `<h4>Evidencia</h4><div class="markdown">${renderMarkdownLite(f.evidence)}</div>` : ""}
            ${f.recommendation ? `<h4>Recomendación</h4><div class="markdown">${renderMarkdownLite(f.recommendation)}</div>` : ""}
          </div>
        </details>`;
      })
      .join("");

    const dexCount = report.artifacts.find((a) => a.artifactType === "dex_count")?.artifactValue ?? "0";
    const fileCount = report.artifacts.find((a) => a.artifactType === "file_count")?.artifactValue ?? "0";
    const nativeLibs = report.artifacts.filter((a) => a.artifactType === "native_library");
    const urls = report.artifacts.filter((a) => a.artifactType === "url");

    const artifactListHtml = (items: ApkArtifact[], emptyLabel: string) => {
      if (items.length === 0) {
        return `<p class="muted">${emptyLabel}</p>`;
      }
      const listItems = items.slice(0, 100).map((a) => `<li><code>${escapeHtml(a.artifactValue)}</code></li>`);
      const remainder = items.length > 100 ? `<li>… (+${items.length - 100} más)</li>` : "";
      return `<ul>${listItems.join("")}${remainder}</ul>`;
    };

    const artifactsHtml = `<details class="finding">
      <summary><span class="title">Artefactos extraídos (${report.artifacts.length})</span></summary>
      <div class="finding-body">
        <div class="summary" style="margin-bottom:0.8rem;">
          <div>Archivos DEX: <strong>${escapeHtml(dexCount)}</strong></div>
          <div>Archivos totales: <strong>${escapeHtml(fileCount)}</strong></div>
          <div>Librerías nativas: <strong>${nativeLibs.length}</strong></div>
          <div>URLs encontradas: <strong>${urls.length}</strong></div>
        </div>
        <h4>Librerías nativas</h4>
        ${artifactListHtml(nativeLibs, "Ninguna.")}
        <h4>URLs</h4>
        ${artifactListHtml(urls, "Ninguna.")}
      </div>
    </details>`;

    return `<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8" />
<style>
  body { font-family: var(--vscode-font-family); color: var(--vscode-foreground); padding: 0 1rem 2rem; }
  h1 { font-size: 1.2rem; word-break: break-all; }
  .summary { display: flex; gap: 0.75rem; flex-wrap: wrap; margin-bottom: 1rem; }
  .summary div { background: var(--vscode-editor-inactiveSelectionBackground); padding: 0.4rem 0.8rem; border-radius: 4px; }
  .chip { border: 1px solid; border-radius: 999px; padding: 0.15rem 0.6rem; font-size: 0.85rem; }
  .finding { border: 1px solid var(--vscode-panel-border); border-radius: 6px; margin-bottom: 0.6rem; padding: 0.4rem 0.7rem; }
  .finding summary { cursor: pointer; display: flex; gap: 0.6rem; align-items: baseline; }
  .finding summary .severity { font-weight: 700; min-width: 4.5rem; }
  .finding-body { margin-top: 0.6rem; }
  .badges { margin-bottom: 0.4rem; }
  .badge { display: inline-block; background: var(--vscode-badge-background); color: var(--vscode-badge-foreground); border-radius: 4px; padding: 0.1rem 0.5rem; font-size: 0.75rem; margin-right: 0.3rem; }
  .badge.muted { background: transparent; border: 1px solid var(--vscode-panel-border); color: var(--vscode-descriptionForeground); }
  pre { background: var(--vscode-textCodeBlock-background); padding: 0.6rem; border-radius: 4px; overflow-x: auto; }
  code { font-family: var(--vscode-editor-font-family); }
  .markdown pre { margin: 0.4rem 0; }
  .muted { color: var(--vscode-descriptionForeground); }
  .hash { font-size: 0.8rem; color: var(--vscode-descriptionForeground); word-break: break-all; margin-bottom: 0.8rem; }
</style>
</head>
<body>
  <h1>${escapeHtml(report.fileName)}</h1>
  <p class="hash">SHA-256: <code>${escapeHtml(report.sha256)}</code></p>
  <div class="summary">
    <div>Tamaño: <strong>${(report.sizeBytes / 1024).toFixed(1)} KB</strong></div>
    <div>Severidad máxima: <strong>${report.severityMax}</strong></div>
    <div>Hallazgos: <strong>${report.findings.length}</strong></div>
    ${chips}
  </div>
  ${report.summary ? `<p class="muted">${escapeHtml(report.summary)}</p>` : ""}
  ${artifactsHtml}
  ${findingsHtml || "<p>No se encontraron hallazgos.</p>"}
</body>
</html>`;
  }
}
