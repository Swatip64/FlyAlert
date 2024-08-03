import React, { useState, useEffect } from 'react';
import '../styles/App.css';

const FlightStatusDashboard = () => {
  const [flights, setFlights] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [sortBy, setSortBy] = useState('flightNumber');
  const [ascending, setAscending] = useState(true);

  useEffect(() => {
    // Fetch flight data from API
    const fetchFlights = async () => {
      try {
        const response = await fetch('http://localhost:5000/api/flight-status');
        const data = await response.json();
        setFlights(data);
      } catch (error) {
        console.error('Error fetching flight data:', error);
      }
    };

    fetchFlights();
  }, []);

  // Filter flights based on search term
  const filteredFlights = flights
    .filter((flight) => 
      flight.flightNumber.toLowerCase().includes(searchTerm.toLowerCase()) ||
      flight.status.toLowerCase().includes(searchTerm.toLowerCase()) ||
      flight.gate.toLowerCase().includes(searchTerm.toLowerCase()) ||
      flight.arrivalTime.toLowerCase().includes(searchTerm.toLowerCase()) ||
      flight.boardingTime.toLowerCase().includes(searchTerm.toLowerCase()) ||
      flight.airline.toLowerCase().includes(searchTerm.toLowerCase()) ||
      flight.aircraftType.toLowerCase().includes(searchTerm.toLowerCase())
    )
    .sort((a, b) => {
      if (a[sortBy] < b[sortBy]) return ascending ? -1 : 1;
      if (a[sortBy] > b[sortBy]) return ascending ? 1 : -1;
      return 0;
    });

  // Handle sorting
  const handleSort = (column) => {
    setSortBy(column);
    setAscending(sortBy === column ? !ascending : true);
  };

  return (
    <div className="flight-status-dashboard">
      <header>
        <h1>FlyAlert</h1>
      </header>
      <input
        type="text"
        placeholder="Search by flight number, status, gate, arrival time, boarding time, airline, aircraft type..."
        value={searchTerm}
        onChange={(e) => setSearchTerm(e.target.value)}
      />
      {filteredFlights.length > 0 ? (
        <table className="table">
          <thead>
            <tr>
              <th onClick={() => handleSort('flightNumber')}>
                Flight Number
                <span className={`sort-indicator ${sortBy === 'flightNumber' ? (ascending ? 'asc' : 'desc') : ''}`}></span>
              </th>
              <th onClick={() => handleSort('status')}>
                Status
                <span className={`sort-indicator ${sortBy === 'status' ? (ascending ? 'asc' : 'desc') : ''}`}></span>
              </th>
              <th onClick={() => handleSort('gate')}>
                Gate
                <span className={`sort-indicator ${sortBy === 'gate' ? (ascending ? 'asc' : 'desc') : ''}`}></span>
              </th>
              <th onClick={() => handleSort('arrivalTime')}>
                Arrival Time
                <span className={`sort-indicator ${sortBy === 'arrivalTime' ? (ascending ? 'asc' : 'desc') : ''}`}></span>
              </th>
              <th onClick={() => handleSort('boardingTime')}>
                Boarding Time
                <span className={`sort-indicator ${sortBy === 'boardingTime' ? (ascending ? 'asc' : 'desc') : ''}`}></span>
              </th>
              <th onClick={() => handleSort('airline')}>
                Airline
                <span className={`sort-indicator ${sortBy === 'airline' ? (ascending ? 'asc' : 'desc') : ''}`}></span>
              </th>
              <th onClick={() => handleSort('aircraftType')}>
                Aircraft Type
                <span className={`sort-indicator ${sortBy === 'aircraftType' ? (ascending ? 'asc' : 'desc') : ''}`}></span>
              </th>
            </tr>
          </thead>
          <tbody>
            {filteredFlights.map((flight) => (
              <tr key={flight.id}>
                <td>{flight.flightNumber}</td>
                <td>{flight.status}</td>
                <td>{flight.gate}</td>
                <td>{flight.arrivalTime}</td>
                <td>{flight.boardingTime}</td>
                <td>{flight.airline}</td>
                <td>{flight.aircraftType}</td>
              </tr>
            ))}
          </tbody>
        </table>
      ) : (
        <p>No flights found</p>
      )}
    </div>
  );
};

export default FlightStatusDashboard;
