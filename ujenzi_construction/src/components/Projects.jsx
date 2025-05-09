// src/pages/Projects.jsx
import React, { useEffect, useState } from 'react';
import axios from 'axios';

const Projects = () => {
  const [projects, setProjects] = useState([]);

  useEffect(() => {
    axios.get('http://127.0.0.1:5000/api/projects')
      .then(res => {
        setProjects(res.data);
      })
      .catch(err => {
        console.error('Error fetching projects:', err);
      });
  }, []);

  return (
    <div className="p-4">
      <h1>Ujenzi Construction</h1>
      <h2 className="text-2xl font-bold mb-4">Projects</h2>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {projects.map(project => (
          <div key={project.id} className="border p-4 rounded shadow">
            <img src={project.image_url} alt={project.name} className="w-full h-48 object-cover rounded mb-2" />
            <h3 className="text-xl font-semibold">{project.name}</h3>
            <p className="text-gray-600">{project.status}</p>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Projects;
