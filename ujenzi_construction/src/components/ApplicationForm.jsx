import React, { useState } from "react";
import axios from "axios";

function ApplicationForm() {
  const [serviceType, setServiceType] = useState("");
  const [design, setDesign] = useState("");
  const [material, setMaterial] = useState("");
  const [rooms, setRooms] = useState("");
  const [phone, setPhone] = useState("");
  const [submitting, setSubmitting] = useState(false);

  const handleApply = async () => {
    if (
      !serviceType ||
      (serviceType === "construction" && (!design || !material || !rooms)) ||
      !phone
    ) {
      alert("Please fill out all fields.");
      return;
    }

    let total = 0;

    if (serviceType === "renovation") {
      total = 100000;
    } else if (serviceType === "construction") {
      total += design === "storey" ? 1000000 : 500000;
      total += material === "high" ? 80000 : 50000;

      const roomCount = parseInt(rooms);
      if (roomCount <= 5) total += 40000;
      else if (roomCount <= 10) total += 90000;
      else total += 140000;
    }

    try {
      setSubmitting(true);
      console.log("Initiating payment with:", { amount: total, phone });

      const response = await axios.post("http://127.0.0.1:5000/api/mpesa_payment", {
        amount: total,
        phone: phone,
      });

      console.log("M-Pesa response:", response.data);
      alert("Payment initiated. Check your phone.");

    } catch (err) {
      console.error("Payment error:", err);

      if (err.response) {
        alert(`Payment failed: ${err.response.data.message || "Please try again."}`);
      } else {
        alert("Payment failed. Could not reach backend.");
      }

    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="p-4 max-w-md mx-auto bg-white shadow-md rounded-lg">
      <h2 className="text-xl font-bold mb-4">Apply for a Service</h2>

      <select
        className="w-full mb-3 p-2 border rounded"
        value={serviceType}
        onChange={(e) => setServiceType(e.target.value)}
      >
        <option value="">Select service</option>
        <option value="renovation">Renovation</option>
        <option value="construction">Construction</option>
      </select>

      {serviceType === "construction" && (
        <>
          <select
            className="w-full mb-3 p-2 border rounded"
            value={design}
            onChange={(e) => setDesign(e.target.value)}
          >
            <option value="">Select design</option>
            <option value="storey">Storey Building</option>
            <option value="normal">Normal Building</option>
          </select>

          <select
            className="w-full mb-3 p-2 border rounded"
            value={material}
            onChange={(e) => setMaterial(e.target.value)}
          >
            <option value="">Select material</option>
            <option value="high">High Quality</option>
            <option value="standard">Standard</option>
          </select>

          <select
            className="w-full mb-3 p-2 border rounded"
            value={rooms}
            onChange={(e) => setRooms(e.target.value)}
          >
            <option value="">Select number of rooms</option>
            {Array.from({ length: 15 }, (_, i) => (
              <option key={i + 1} value={i + 1}>
                {i + 1}
              </option>
            ))}
          </select>
        </>
      )}

      <input
        type="tel"
        className="w-full mb-3 p-2 border rounded"
        placeholder="Enter phone number"
        value={phone}
        onChange={(e) => setPhone(e.target.value)}
      />

      <button
        onClick={handleApply}
        disabled={submitting}
        className="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700"
      >
        {submitting ? "Processing..." : "Apply & Pay"}
      </button>
    </div>
  );
}

export default ApplicationForm;
