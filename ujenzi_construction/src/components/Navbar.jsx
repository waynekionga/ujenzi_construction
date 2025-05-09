// src/components/Navbar.jsx
import React from 'react';
import { Link } from 'react-router-dom';

const Navbar = () => {
  return (
    <nav className="bg-blue-600 text-white p-4 flex justify-between items-center">
      <div className="text-xl font-bold"><h1>Ujenzi Construction</h1></div>
      <div className="space-x-4">
       <button><Link to="/">Home</Link></button> 

       <button><Link to="/projects">Projects</Link></button> 

       <button><Link to="/apply">Apply</Link></button> 

        
        <button><Link to="/workers">Workers</Link></button>

        <button><Link to="/login">Login</Link></button>

        <button><Link to="/signup">Signup</Link></button>
      </div>
    </nav>
  );
};

export default Navbar;
