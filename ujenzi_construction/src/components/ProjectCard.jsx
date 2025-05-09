import React, { useEffect, useState } from 'react';

const Projects = () => {
  const [projects, setProjects] = useState([]);

  useEffect(() => {
    fetch('http://127.0.0.1:5000/api/projects')
      .then(res => {
        if (!res.ok) {
          throw new Error('Network response was not ok');
        }
        return res.json();
      })
      .then(data => setProjects(data))
      .catch(err => {
        console.error('Error fetching projects:', err);
        alert("Failed to load projects");
      });
  }, []);

  return (
    <div className="container mt-4">
      <h1>Ujenzi Construction</h1>
      <h2 className="mb-4 text-center">Projects</h2>
      {projects.length === 0 ? (
        <p className="text-center">No projects found.</p>
      ) : (
        <div className="row">
          {projects.map((project, index) => (
            <div className="col-md-3 mb-4" key={index}>
              <div className="card h-100 shadow-sm">
                <img
                  src={`/${project.blueprint}`}
                  className="card-img-top"
                  alt={project.name}
                  style={{ height: "180px", objectFit: "cover" }}
                />
                <div className="card-body">
                  <h5 className="card-title">{project.name}</h5>
                  <p className="card-text">{project.description}</p>
                  <span className="badge bg-primary">{project.status}</span>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default Projects;
