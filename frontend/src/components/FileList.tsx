import React, { useEffect, useState } from "react";
import api from "../api/client";

export default function FileList() {
  const [files, setFiles] = useState<string[]>([]);

  const loadFiles = async () => {
    const res = await api.get("/files/");
    setFiles(res.data.files);
  };

  useEffect(() => {
    loadFiles();
  }, []);

  return (
    <div className="bg-white p-4 rounded shadow mt-4">
      <h2 className="text-lg font-semibold mb-2">Fichiers disponibles</h2>
      <ul className="list-disc pl-6">
        {files.map((f) => (
          <li key={f}>{f}</li>
        ))}
      </ul>
    </div>
  );
}
