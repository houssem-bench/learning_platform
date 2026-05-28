import React, { createContext, useContext, useEffect, useMemo, useState } from "react";

import { fetchMe, login as apiLogin, register as apiRegister, tokenStorage } from "../api.js";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [token, setToken] = useState(() => tokenStorage.get());
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(Boolean(token));

  useEffect(() => {
    if (!token) {
      setUser(null);
      setLoading(false);
      return;
    }
    setLoading(true);
    fetchMe()
      .then((data) => setUser(data))
      .catch(() => {
        tokenStorage.clear();
        setToken("");
        setUser(null);
      })
      .finally(() => setLoading(false));
  }, [token]);

  const login = async (username, password) => {
    const response = await apiLogin(username, password);
    tokenStorage.set(response.access_token);
    setToken(response.access_token);
    const me = await fetchMe();
    setUser(me);
    return me;
  };

  const register = async (username, password) => {
    const response = await apiRegister(username, password);
    tokenStorage.set(response.access_token);
    setToken(response.access_token);
    const me = await fetchMe();
    setUser(me);
    return me;
  };

  const logout = () => {
    tokenStorage.clear();
    setToken("");
    setUser(null);
  };

  const value = useMemo(
    () => ({ token, user, loading, login, register, logout }),
    [token, user, loading]
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  return useContext(AuthContext);
}
