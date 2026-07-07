import * as vscode from "vscode";

export interface CollectedFile {
  relativePath: string;
  content: Uint8Array;
}

export interface CollectOptions {
  excludeGlobs: string[];
  maxFileSizeKb: number;
}

function toExcludePattern(globs: string[]): string | undefined {
  if (globs.length === 0) {
    return undefined;
  }
  return globs.length === 1 ? globs[0] : `{${globs.join(",")}}`;
}

export async function collectFiles(
  root: vscode.Uri,
  options: CollectOptions
): Promise<CollectedFile[]> {
  const pattern = new vscode.RelativePattern(root, "**/*");
  const excludePattern = toExcludePattern(options.excludeGlobs);
  const uris = await vscode.workspace.findFiles(pattern, excludePattern);
  const maxBytes = options.maxFileSizeKb * 1024;

  const collected: CollectedFile[] = [];
  for (const uri of uris) {
    const stat = await vscode.workspace.fs.stat(uri);
    if (stat.type !== vscode.FileType.File || stat.size > maxBytes) {
      continue;
    }
    const content = await vscode.workspace.fs.readFile(uri);
    const relativePath = vscode.workspace.asRelativePath(uri, false).replace(/\\/g, "/");
    collected.push({ relativePath, content });
  }
  return collected;
}

export async function collectSingleFile(
  uri: vscode.Uri,
  root: vscode.Uri
): Promise<CollectedFile[]> {
  const content = await vscode.workspace.fs.readFile(uri);
  const relativePath = uri.path.startsWith(root.path)
    ? uri.path.slice(root.path.length).replace(/^\/+/, "")
    : (uri.path.split("/").pop() ?? "file");
  return [{ relativePath, content }];
}
