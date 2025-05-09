import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";

function Login() {
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post("http://localhost:5000/api/login", {
        email,
        password,
      });

      if (response.data.message === "Login successful") {
        localStorage.setItem("user", JSON.stringify(response.data.user)); // optional
        alert("Login successful");
        navigate("/");
      } else {
        alert("Login failed");
      }
      
    } catch (err) {
      alert("Login failed");
      console.error(err);
    }
  };

  return (
    <form onSubmit={handleLogin}>
      <input type="email" placeholder="Email" onChange={(e) => setEmail(e.target.value)} /> <br />
      <input type="password" placeholder="Password" onChange={(e) => setPassword(e.target.value)} /> <br />
      <button type="submit">Login</button>
    </form>
  );
}

export default Login;
