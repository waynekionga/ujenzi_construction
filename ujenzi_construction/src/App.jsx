import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Home from './components/Home';
import Navbar from './components/Navbar';
import Footer from './components/Footer';
import Login from './components/Login';
import PrivateRoute from "./components/PrivateRoute";
import Workers from './components/Workers';
import Signup from './components/Signup';
import Projects from './components/ProjectCard';
import ApplicationForm from './components/ApplicationForm';



<Route path="/apply" element={<ApplicationForm />} />


export default function App() {
  return (
    <Router>
      <div className="min-h-screen flex flex-col">
        <Navbar />
        <main className="flex-grow p-4">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/login" element={<Login />} />
            <Route path="/signup" element={<Signup />} />
            <Route path="/workers" element={<Workers />} />
            <Route path="/projects" element={<Projects />} />
            {/* Only authenticated users can access /apply */}
            <Route path="/apply" element={<ApplicationForm />} />
          </Routes>
        </main>
        <Footer />
      </div>
    </Router>
  );
}
