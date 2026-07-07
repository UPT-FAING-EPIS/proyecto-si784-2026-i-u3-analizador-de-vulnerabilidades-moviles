import type { CollectedFile } from "./fileCollector";

export interface FileMetrics {
  nom: number;
  noa: number;
}

export interface FileResult {
  file_path: string;
  loc: number;
  complexity: number;
  metrics: FileMetrics;
  smells: string[];
}

export interface AnalysisResult {
  status: string;
  project_name: string;
  loc: number;
  complexity: number;
  code_smells: {
    smells: string[];
    metrics: { nom: number; noa: number };
    files: FileResult[];
  };
}

export class AnzenCoreApiError extends Error {}

export async function analyzeFolder(
  apiBaseUrl: string,
  projectName: string,
  files: CollectedFile[],
  signal: AbortSignal
): Promise<AnalysisResult> {
  const form = new FormData();
  form.append("project_name", projectName);
  for (const file of files) {
    const blob = new Blob([file.content]);
    form.append("files", blob, file.relativePath);
  }

  let response: Response;
  try {
    response = await fetch(`${apiBaseUrl}/api/analysis/external/upload_folder`, {
      method: "POST",
      body: form,
      signal,
    });
  } catch (err) {
    throw new AnzenCoreApiError(
      `No se pudo contactar la API de AnzenCore en ${apiBaseUrl}: ${(err as Error).message}`
    );
  }

  if (!response.ok) {
    const detail = await response.text().catch(() => "");
    throw new AnzenCoreApiError(
      `La API respondió ${response.status}${detail ? `: ${detail}` : ""}`
    );
  }

  return (await response.json()) as AnalysisResult;
}
