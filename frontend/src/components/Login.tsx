import React, { useState } from "react";
import api from "../api/client";

export default function Login({ onSuccess }: { onSuccess: () => void }) {
  const [key, setKey] = useState("");
  const [error, setError] = useState("");

  const checkKey = async () => {
    try {
      const res = await api.get("/auth/check", {
        headers: { "x-api-key": key },
      });
      if (res.data.status === "authorized") {
        localStorage.setItem("apiKey", key);
        onSuccess();
      }
    } catch {
      setError("Clé invalide");
    }
  };

  return (
    <div className="bg-white p-6 rounded shadow text-center">
      <h1 className="text-xl mb-4 font-semibold">Connexion à MiniStudio</h1>
      <input
        className="border p-2 rounded w-64"
        placeholder="Entrez votre clé API"
        value={key}
        onChange={(e) => setKey(e.target.value)}
      />
      <button
        onClick={checkKey}
        className="ml-2 px-4 py-2 bg-blue-600 text-white rounded"
      >
        Se connecter
      </button>
      {error && <p className="text-red-500 mt-2">{error}</p>}
    </div>
  );
}
