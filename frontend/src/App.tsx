import React from "react";
import { BrowserRouter as Router } from "react-router-dom";
import { CssBaseline } from "@mui/material";
import Layout from "./components/Layout";

function App() {
  return (
    <Router>
      <CssBaseline />
      <Layout />
    </Router>
  );
}

export default App;
