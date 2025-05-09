// src/components/PrivateRoute.jsx
import React from "react";
import { Navigate } from "react-router-dom";

const PrivateRoute = ({ children }) => {
  const isAuthenticated = !!localStorage.getItem("token"); // adjust based on your token key

  return isAuthenticated ? children : <Navigate to="/login" />;
};

export default PrivateRoute;
