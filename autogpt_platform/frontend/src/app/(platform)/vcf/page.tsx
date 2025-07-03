"use client";
import { useState } from "react";
import { Button } from "@/components/ui/button";
import { useBackendAPI } from "@/lib/autogpt-server-api/context";

export default function VcfUploadPage() {
  const [file, setFile] = useState<File | null>(null);
  const [result, setResult] = useState<any>(null);
  const api = useBackendAPI();

  async function handleUpload() {
    if (!file) return;
    try {
      const res = await api.annotateVcf(file);
      setResult(res);
    } catch (e) {
      console.error(e);
      setResult({ error: String(e) });
    }
  }

  return (
    <div className="container mx-auto max-w-2xl space-y-4 p-4">
      <h1 className="text-2xl font-bold">VCF Annotation</h1>
      <input
        type="file"
        accept=".vcf"
        onChange={(e) => setFile(e.target.files?.[0] ?? null)}
        className="block"
      />
      <Button onClick={handleUpload} disabled={!file} className="mt-2">
        Upload
      </Button>
      {result && (
        <pre className="overflow-auto whitespace-pre-wrap rounded bg-neutral-100 p-4 text-xs">
          {JSON.stringify(result, null, 2)}
        </pre>
      )}
    </div>
  );
}
