import React, { useEffect, useState } from "react";
import api from "../api/client";

export default function History() {
  const [history, setHistory] = useState<any[]>([]);

  const loadHistory = async () => {
    const res = await api.get("/history/");
    setHistory(res.data.history);
  };

  useEffect(() => {
    loadHistory();
  }, []);

  return (
    <div className="bg-white p-4 rounded shadow mt-4">
      <h2 className="text-lg font-semibold mb-2">Historique</h2>
      <ul className="list-disc pl-6">
        {history.map((entry, i) => (
          <li key={i}>{JSON.stringify(entry)}</li>
        ))}
      </ul>
    </div>
  );
}
