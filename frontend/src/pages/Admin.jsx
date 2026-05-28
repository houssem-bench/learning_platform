import { useEffect, useState } from "react";

import { createUser, listUsers, reloadSeed } from "../api.js";
import { useAuth } from "../components/AuthProvider.jsx";

function Admin() {
  const { user } = useAuth();
  const [users, setUsers] = useState([]);
  const [error, setError] = useState("");
  const [notice, setNotice] = useState("");
  const [form, setForm] = useState({ username: "", password: "", role: "student" });

  useEffect(() => {
    listUsers()
      .then((data) => setUsers(data))
      .catch((err) => setError(err.message || "Failed to load users"));
  }, []);

  if (!user || user.role !== "admin") {
    return <div className="card">Admin access required.</div>;
  }

  const handleCreate = async (event) => {
    event.preventDefault();
    setError("");
    setNotice("");
    try {
      const created = await createUser(form);
      setUsers((prev) => [...prev, created]);
      setForm({ username: "", password: "", role: "student" });
      setNotice("User created.");
    } catch (err) {
      setError(err.message || "Failed to create user");
    }
  };

  const handleReload = async () => {
    setError("");
    setNotice("");
    try {
      const result = await reloadSeed();
      setNotice(`Seed imported: ${result.imported_quizzes}`);
    } catch (err) {
      setError(err.message || "Failed to reload content");
    }
  };

  return (
    <div>
      <h1>Admin dashboard</h1>
      {error ? <p className="notice">{error}</p> : null}
      {notice ? <p className="notice">{notice}</p> : null}

      <div className="grid" style={{ marginTop: 20 }}>
        <div className="card">
          <h3>Create user</h3>
          <form onSubmit={handleCreate}>
            <div className="field">
              <label>Username</label>
              <input
                value={form.username}
                onChange={(event) =>
                  setForm((prev) => ({ ...prev, username: event.target.value }))
                }
                required
              />
            </div>
            <div className="field">
              <label>Password</label>
              <input
                type="password"
                value={form.password}
                onChange={(event) =>
                  setForm((prev) => ({ ...prev, password: event.target.value }))
                }
                required
              />
            </div>
            <div className="field">
              <label>Role</label>
              <select
                value={form.role}
                onChange={(event) =>
                  setForm((prev) => ({ ...prev, role: event.target.value }))
                }
              >
                <option value="student">Student</option>
                <option value="admin">Admin</option>
              </select>
            </div>
            <button className="button" type="submit">
              Create user
            </button>
          </form>
        </div>

        <div className="card">
          <h3>Content tools</h3>
          <p className="notice">
            Re-imports quiz content from seed files. Existing attempts will block
            the reload.
          </p>
          <button className="button ghost" onClick={handleReload}>
            Reload seed content
          </button>
        </div>
      </div>

      <div style={{ marginTop: 24 }}>
        <div className="card">
          <h3>Users</h3>
          <ul>
            {users.map((item) => (
              <li key={item.id}>
                {item.username} ({item.role})
              </li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
}

export default Admin;
