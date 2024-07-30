import React from "react";
import ReactDOM from "react-dom/client";
import { Header } from "shared/ui";
import { HomePage } from "pages";
import "./global.css";

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <Header />
    <HomePage />
  </React.StrictMode>,
);
