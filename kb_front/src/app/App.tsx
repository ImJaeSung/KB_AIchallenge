import React from "react";
import ReactDOM from "react-dom/client";
import { HomePage } from "pages";
import "./global.css";

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <h1>Hello, World!</h1>
    <HomePage />
  </React.StrictMode>,
);
