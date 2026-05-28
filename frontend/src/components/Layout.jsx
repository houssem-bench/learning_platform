import { NavLink, useNavigate } from "react-router-dom";

import { useAuth } from "./AuthProvider.jsx";

function Layout({ children }) {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate("/login");
  };

  return (
    <>
      <header className="header">
        <div className="header-inner">
          <div className="brand">
            <strong>Learning Platform</strong>
            <span>Unity QCU Program</span>
          </div>
          <nav className="nav">
            {user ? (
              <>
                <NavLink to="/catalog">Catalog</NavLink>
                {user.role === "admin" ? <NavLink to="/admin">Admin</NavLink> : null}
                <button className="button ghost" onClick={handleLogout}>
                  Logout
                </button>
              </>
            ) : (
              <NavLink to="/login">Login</NavLink>
            )}
          </nav>
        </div>
      </header>
      <main className="page">{children}</main>
    </>
  );
}

export default Layout;
