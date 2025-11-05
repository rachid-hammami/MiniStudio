
import React, { useState, KeyboardEvent } from "react";
import axios from "axios";
import type { AxiosResponse } from "axios";

interface AnalyzeResponse {
  status: string;
  file?: string;
  count?: number;
  report?: unknown;
  message?: string;
}

const Analyzer: React.FC = () => {
  const [filename, setFilename] = useState<string>("");
  const [loading, setLoading] = useState<boolean>(false);
  const [result, setResult] = useState<AnalyzeResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleAnalyze = async (): Promise<void> => {
    if (!filename) {
      setError("Veuillez entrer le nom d’un fichier à analyser.");
      return;
    }

    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const response: AxiosResponse<AnalyzeResponse> = await axios.post(
        "http://127.0.0.1:8000/analyze",
        { filename }
      );

      if (response.data.status === "ok") {
        setResult(response.data);
      } else {
        setError(response.data.message || "Erreur lors de l’analyse du fichier.");
      }
    } catch (err: any) {
      setError(err.response?.data?.message || "Erreur de connexion au backend.");
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (e: KeyboardEvent<HTMLInputElement>): void => {
    if (e.key === "Enter") {
      handleAnalyze();
    }
  };

  return (
    <div
      className="analyzer-container"
      style={{ maxWidth: "600px", margin: "0 auto", textAlign: "center" }}
    >
      <h2>Analyseur de fichiers</h2>

      <input
        type="text"
        placeholder="Nom du fichier (ex : ai_engine.py)"
        value={filename}
        onChange={(e) => setFilename(e.target.value)}
        onKeyDown={handleKeyDown}
        style={{
          width: "100%",
          padding: "10px",
          marginBottom: "10px",
          borderRadius: "8px",
          border: "1px solid #ccc",
          fontSize: "16px",
        }}
      />

      <button
        onClick={handleAnalyze}
        disabled={loading}
        style={{
          padding: "10px 20px",
          borderRadius: "8px",
          backgroundColor: "#0078d7",
          color: "white",
          border: "none",
          cursor: "pointer",
          fontSize: "16px",
        }}
      >
        {loading ? "Analyse en cours..." : "Analyser le fichier"}
      </button>

      {error && (
        <p style={{ color: "red", marginTop: "20px" }}>⚠️ {error}</p>
      )}

      {result && (
        <div style={{ marginTop: "20px", textAlign: "left" }}>
          <h3>Résultat de l’analyse</h3>
          <pre
            style={{
              background: "#f4f4f4",
              padding: "10px",
              borderRadius: "8px",
              fontSize: "14px",
              maxHeight: "300px",
              overflowY: "auto",
            }}
          >
            {JSON.stringify(result, null, 2)}
          </pre>
        </div>
      )}
    </div>
  );
};

export default Analyzer;
