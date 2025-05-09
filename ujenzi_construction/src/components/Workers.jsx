import React, { useEffect, useState } from 'react';

const Workers = () => {
  const [workers, setWorkers] = useState([]);

  useEffect(() => {
    fetch('http://127.0.0.1:5000/api/workers')
      .then(res => {
        if (!res.ok) {
          throw new Error('Failed to fetch workers');
        }
        return res.json();
      })
      .then(data => setWorkers(data || []))
      .catch(err => {
        console.error('Error fetching workers:', err);
        alert("Failed to load workers");
      });
  }, []);

  return (
    <div className="container mt-4">
      <h1>Ujenzi Construction</h1>
      <h2 className="mb-4 text-center">Our Workers</h2>
      {workers.length === 0 ? (
        <p className="text-center">No workers found.</p>
      ) : (
        <div className="row">
          {workers.map((worker, i) => (
            <div key={i} className="col-md-3 mb-4">
              <div className="card h-100 shadow-sm">
                <img
                  src={`/images2/${worker.worker_photo}`}
                  className="card-img-top"
                  alt={worker.name}
                  style={{ height: '200px', objectFit: 'cover' }}
                />
                <div className="card-body">
                  <h5 className="card-title">{worker.name}</h5>
                  <p className="card-text">Phone: {worker.phone}</p>
                  <span className="badge bg-secondary">{worker.role}</span>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default Workers;
