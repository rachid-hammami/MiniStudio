import React, { useState } from "react";
import FileList from "./components/FileList";
import History from "./components/History";
import Analyzer from "./components/Analyzer";
import Login from "./components/Login";
import Navbar from "./components/Navbar";

export default function App() {
  const [authorized, setAuthorized] = useState(
    !!localStorage.getItem("apiKey")
  );

  return (
    <div className="min-h-screen bg-gray-100">
      <Navbar />
      <div className="max-w-5xl mx-auto p-4">
        {!authorized ? (
          <Login onSuccess={() => setAuthorized(true)} />
        ) : (
          <>
            <FileList />
            <Analyzer />
            <History />
          </>
        )}
      </div>
    </div>
  );
}
