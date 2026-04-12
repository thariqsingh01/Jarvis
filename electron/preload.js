const { contextBridge } = require('electron');

const API_URL = "http://127.0.0.1:8000"; // Your FastAPI backend

contextBridge.exposeInMainWorld("JarvisAPI", {
  listen: async () => {
    const res = await fetch(`${API_URL}/listen`, { method: "POST" });
    return await res.json();
  },
  speak: async (text) => {
    const res = await fetch(`${API_URL}/speak`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text }),
    });
    return await res.json();
  },
  command: async (text) => {
    const res = await fetch(`${API_URL}/command`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text }),
    });
    return await res.json();
  }
});