import * as vscode from "vscode";
import type { FileResult } from "./api";

export function createDiagnosticCollection(): vscode.DiagnosticCollection {
  return vscode.languages.createDiagnosticCollection("anzencore");
}

export function applyDiagnostics(
  collection: vscode.DiagnosticCollection,
  root: vscode.Uri,
  files: FileResult[]
): void {
  collection.clear();
  for (const file of files) {
    if (file.smells.length === 0) {
      continue;
    }
    const uri = vscode.Uri.joinPath(root, file.file_path);
    const range = new vscode.Range(0, 0, 0, 0);
    const diagnostics = file.smells.map((smell) => {
      const diagnostic = new vscode.Diagnostic(range, smell, vscode.DiagnosticSeverity.Warning);
      diagnostic.source = "AnzenCore";
      return diagnostic;
    });
    collection.set(uri, diagnostics);
  }
}
