import React from "react";

export default function Navbar() {
  return (
    <nav className="bg-blue-700 text-white p-3">
      <div className="max-w-5xl mx-auto flex justify-between items-center">
        <h1 className="text-lg font-bold">MiniStudio Dashboard</h1>
        <button
          className="text-sm underline"
          onClick={() => {
            localStorage.removeItem("apiKey");
            window.location.reload();
          }}
        >
          Déconnexion
        </button>
      </div>
    </nav>
  );
}
