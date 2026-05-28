import { Navigate, Route, Routes } from "react-router-dom";

import Layout from "./components/Layout.jsx";
import RequireAuth from "./components/RequireAuth.jsx";
import Admin from "./pages/Admin.jsx";
import Attempt from "./pages/Attempt.jsx";
import Catalog from "./pages/Catalog.jsx";
import Login from "./pages/Login.jsx";
import Register from "./pages/Register.jsx";
import Results from "./pages/Results.jsx";

function App() {
  return (
    <Layout>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route
          path="/"
          element={
            <RequireAuth>
              <Navigate to="/catalog" replace />
            </RequireAuth>
          }
        />
        <Route
          path="/catalog"
          element={
            <RequireAuth>
              <Catalog />
            </RequireAuth>
          }
        />
        <Route
          path="/attempts/:attemptId"
          element={
            <RequireAuth>
              <Attempt />
            </RequireAuth>
          }
        />
        <Route
          path="/attempts/:attemptId/results"
          element={
            <RequireAuth>
              <Results />
            </RequireAuth>
          }
        />
        <Route
          path="/admin"
          element={
            <RequireAuth>
              <Admin />
            </RequireAuth>
          }
        />
        <Route path="*" element={<Navigate to="/catalog" replace />} />
      </Routes>
    </Layout>
  );
}

export default App;
