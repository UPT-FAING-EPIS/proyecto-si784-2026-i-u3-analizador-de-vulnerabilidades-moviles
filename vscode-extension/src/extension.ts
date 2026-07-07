import * as vscode from "vscode";
import { createHash } from "node:crypto";
import { collectFiles, collectSingleFile } from "./fileCollector";
import { analyzeFolder, AnzenCoreApiError, type AnalysisResult } from "./api";
import { ResultsPanel } from "./resultsPanel";
import { applyDiagnostics, createDiagnosticCollection } from "./diagnostics";
import { analyzeApk } from "./apkAnalyzer";
import { VulnerabilitiesPanel } from "./vulnerabilitiesPanel";

const APK_DETECTION_EXCLUDE = "{**/node_modules/**,**/.git/**}";

async function findApkFiles(root: vscode.Uri): Promise<vscode.Uri[]> {
  return vscode.workspace.findFiles(new vscode.RelativePattern(root, "**/*.apk"), APK_DETECTION_EXCLUDE);
}

async function analyzeApkFile(uri: vscode.Uri): Promise<void> {
  const fileName = uri.path.split("/").pop() ?? "app.apk";
  await vscode.window.withProgress(
    { location: vscode.ProgressLocation.Notification, title: `AnzenCore: analizando ${fileName}` },
    async () => {
      const bytes = await vscode.workspace.fs.readFile(uri);
      const result = analyzeApk(bytes);
      if (result.status === "failed") {
        vscode.window.showErrorMessage(`AnzenCore: ${result.errorMessage}`);
        return;
      }
      const sha256 = createHash("sha256").update(bytes).digest("hex");
      VulnerabilitiesPanel.show({
        fileName,
        sizeBytes: bytes.byteLength,
        sha256,
        summary: result.summary,
        severityMax: result.severityMax,
        findings: result.findings,
        artifacts: result.artifacts,
      });
    }
  );
}

async function offerApkAnalysis(root: vscode.Uri): Promise<void> {
  const apks = await findApkFiles(root);
  if (apks.length === 0) {
    return;
  }
  const choice = await vscode.window.showInformationMessage(
    `AnzenCore: se encontró${apks.length > 1 ? "n" : ""} ${apks.length} archivo(s) APK. ¿Analizar vulnerabilidades móviles?`,
    "Analizar APK"
  );
  if (choice !== "Analizar APK") {
    return;
  }
  if (apks.length === 1) {
    await analyzeApkFile(apks[0]);
    return;
  }
  const picked = await vscode.window.showQuickPick(
    apks.map((uri) => ({ label: vscode.workspace.asRelativePath(uri, false), uri })),
    { placeHolder: "Selecciona un APK a analizar" }
  );
  if (picked) {
    await analyzeApkFile(picked.uri);
  }
}

function getConfig() {
  const config = vscode.workspace.getConfiguration("anzencore");
  return {
    apiBaseUrl: config.get<string>("apiBaseUrl", "http://localhost:8000").replace(/\/$/, ""),
    excludeGlobs: config.get<string[]>("excludeGlobs", []),
    maxFileSizeKb: config.get<number>("maxFileSizeKb", 512),
  };
}

async function runAnalysis(
  root: vscode.Uri,
  projectName: string,
  diagnostics: vscode.DiagnosticCollection,
  collect: () => Thenable<{ relativePath: string; content: Uint8Array }[]>
): Promise<void> {
  const { apiBaseUrl } = getConfig();

  await vscode.window.withProgress(
    {
      location: vscode.ProgressLocation.Notification,
      title: `AnzenCore: analizando ${projectName}`,
      cancellable: true,
    },
    async (progress, token) => {
      const controller = new AbortController();
      token.onCancellationRequested(() => controller.abort());

      progress.report({ message: "Recolectando archivos..." });
      const files = await collect();
      if (files.length === 0) {
        vscode.window.showWarningMessage("AnzenCore: no se encontraron archivos para analizar.");
        return;
      }

      progress.report({ message: `Enviando ${files.length} archivo(s) a la API...` });
      let result: AnalysisResult;
      try {
        result = await analyzeFolder(apiBaseUrl, projectName, files, controller.signal);
      } catch (err) {
        if (controller.signal.aborted) {
          return;
        }
        const message = err instanceof AnzenCoreApiError ? err.message : `Error inesperado: ${err}`;
        const choice = await vscode.window.showErrorMessage(message, "Reintentar");
        if (choice === "Reintentar") {
          await runAnalysis(root, projectName, diagnostics, collect);
        }
        return;
      }

      applyDiagnostics(diagnostics, root, result.code_smells.files);
      ResultsPanel.show(root, result);
    }
  );
}

export function activate(context: vscode.ExtensionContext): void {
  const diagnostics = createDiagnosticCollection();

  const analyzeWorkspace = vscode.commands.registerCommand(
    "anzencore.analyzeWorkspace",
    async () => {
      const folder = vscode.workspace.workspaceFolders?.[0];
      if (!folder) {
        vscode.window.showErrorMessage("AnzenCore: abre una carpeta de trabajo primero.");
        return;
      }
      const { excludeGlobs, maxFileSizeKb } = getConfig();
      await runAnalysis(folder.uri, folder.name, diagnostics, () =>
        collectFiles(folder.uri, { excludeGlobs, maxFileSizeKb })
      );
      await offerApkAnalysis(folder.uri);
    }
  );

  const analyzeFolder = vscode.commands.registerCommand(
    "anzencore.analyzeFolder",
    async (uri?: vscode.Uri) => {
      if (!uri) {
        vscode.window.showErrorMessage("AnzenCore: selecciona una carpeta desde el Explorer.");
        return;
      }
      const { excludeGlobs, maxFileSizeKb } = getConfig();
      const projectName = uri.path.split("/").findLast(Boolean) ?? "carpeta";
      await runAnalysis(uri, projectName, diagnostics, () =>
        collectFiles(uri, { excludeGlobs, maxFileSizeKb })
      );
      await offerApkAnalysis(uri);
    }
  );

  const analyzeCurrentFile = vscode.commands.registerCommand(
    "anzencore.analyzeCurrentFile",
    async (uri?: vscode.Uri) => {
      const target = uri ?? vscode.window.activeTextEditor?.document.uri;
      if (!target) {
        vscode.window.showErrorMessage("AnzenCore: no hay un archivo activo para analizar.");
        return;
      }
      const workspaceFolder = vscode.workspace.getWorkspaceFolder(target);
      const root = workspaceFolder?.uri ?? vscode.Uri.joinPath(target, "..");
      const projectName = target.path.split("/").pop() ?? "archivo";
      await runAnalysis(root, projectName, diagnostics, () => collectSingleFile(target, root));
    }
  );

  const analyzeApkCommand = vscode.commands.registerCommand(
    "anzencore.analyzeApk",
    async (uri?: vscode.Uri) => {
      let target = uri;
      if (!target) {
        const picked = await vscode.window.showOpenDialog({
          canSelectMany: false,
          filters: { "Android APK": ["apk"] },
          openLabel: "Analizar APK",
        });
        target = picked?.[0];
      }
      if (!target) {
        return;
      }
      await analyzeApkFile(target);
    }
  );

  context.subscriptions.push(
    diagnostics,
    analyzeWorkspace,
    analyzeFolder,
    analyzeCurrentFile,
    analyzeApkCommand
  );
}

export function deactivate(): void {
  // No cleanup needed; diagnostics collection is disposed via context.subscriptions.
}
