import * as vscode from "vscode";
import type { AnalysisResult } from "./api";

function escapeHtml(value: string): string {
  return value
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

export class ResultsPanel {
  private static current: ResultsPanel | undefined;
  private readonly panel: vscode.WebviewPanel;
  private readonly root: vscode.Uri;

  private constructor(panel: vscode.WebviewPanel, root: vscode.Uri) {
    this.panel = panel;
    this.root = root;
    this.panel.webview.onDidReceiveMessage((message) => {
      if (message.command === "openFile") {
        const uri = vscode.Uri.joinPath(this.root, message.filePath);
        vscode.window.showTextDocument(uri);
      }
    });
    this.panel.onDidDispose(() => {
      ResultsPanel.current = undefined;
    });
  }

  static show(root: vscode.Uri, result: AnalysisResult): void {
    if (ResultsPanel.current) {
      ResultsPanel.current.panel.reveal();
    } else {
      const panel = vscode.window.createWebviewPanel(
        "anzencoreResults",
        "AnzenCore: Resultados",
        vscode.ViewColumn.Beside,
        { enableScripts: true, retainContextWhenHidden: true }
      );
      ResultsPanel.current = new ResultsPanel(panel, root);
    }
    ResultsPanel.current.render(result);
  }

  private render(result: AnalysisResult): void {
    this.panel.title = `AnzenCore: ${result.project_name}`;
    this.panel.webview.html = this.buildHtml(result);
  }

  private buildHtml(result: AnalysisResult): string {
    const rows = result.code_smells.files
      .map((file) => {
        const smells = file.smells.length
          ? `<ul>${file.smells.map((s) => `<li>${escapeHtml(s)}</li>`).join("")}</ul>`
          : "<span class=\"muted\">-</span>";
        return `<tr>
          <td><a href="#" class="file-link" data-path="${escapeHtml(file.file_path)}">${escapeHtml(
          file.file_path
        )}</a></td>
          <td>${file.loc}</td>
          <td>${file.complexity}</td>
          <td>${file.metrics.nom}</td>
          <td>${file.metrics.noa}</td>
          <td>${smells}</td>
        </tr>`;
      })
      .join("");

    return `<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8" />
<style>
  body { font-family: var(--vscode-font-family); color: var(--vscode-foreground); padding: 0 1rem; }
  h1 { font-size: 1.2rem; }
  .summary { display: flex; gap: 1.5rem; margin-bottom: 1rem; }
  .summary div { background: var(--vscode-editor-inactiveSelectionBackground); padding: 0.5rem 1rem; border-radius: 4px; }
  table { border-collapse: collapse; width: 100%; }
  th, td { text-align: left; padding: 0.4rem 0.6rem; border-bottom: 1px solid var(--vscode-panel-border); vertical-align: top; }
  th { position: sticky; top: 0; background: var(--vscode-editor-background); }
  ul { margin: 0; padding-left: 1.1rem; }
  .muted { color: var(--vscode-descriptionForeground); }
  a.file-link { color: var(--vscode-textLink-foreground); cursor: pointer; text-decoration: none; }
  a.file-link:hover { text-decoration: underline; }
</style>
</head>
<body>
  <h1>${escapeHtml(result.project_name)}</h1>
  <div class="summary">
    <div>LOC: <strong>${result.loc}</strong></div>
    <div>Complejidad: <strong>${result.complexity}</strong></div>
    <div>Smells: <strong>${result.code_smells.smells.length}</strong></div>
    <div>Archivos: <strong>${result.code_smells.files.length}</strong></div>
  </div>
  <table>
    <thead>
      <tr><th>Archivo</th><th>LOC</th><th>Complejidad</th><th>NOM</th><th>NOA</th><th>Smells</th></tr>
    </thead>
    <tbody>${rows}</tbody>
  </table>
  <script>
    const vscode = acquireVsCodeApi();
    document.querySelectorAll('.file-link').forEach((el) => {
      el.addEventListener('click', (event) => {
        event.preventDefault();
        vscode.postMessage({ command: 'openFile', filePath: el.dataset.path });
      });
    });
  </script>
</body>
</html>`;
  }
}
