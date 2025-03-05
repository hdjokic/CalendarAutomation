import React, { useState } from 'react';
import './styles.css';
import axios from 'axios';

const Spreadsheet = () => {
  const [sheetLink, setSheetLink] = useState('');
  const [events, setEvents] = useState([]);
  const [icsFile, setIcsFile] = useState(null);

  const handleSheetLinkChange = (e) => {
    setSheetLink(e.target.value);
  };

  const handleGenerateICS = async () => {
    try {
      const response = await axios.post('http://localhost:5000/generate-ics', {
        sheetLink,
      });
      const blob = new Blob([response.data], { type: 'text/calendar' });
      setIcsFile(blob);
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <div className="container">
      <input
        type="text"
        className="input-field"
        value={sheetLink}
        onChange={handleSheetLinkChange}
        placeholder="Enter Google Sheets link"
      />
      <button className="button" onClick={handleGenerateICS}>
        Generate ICS
      </button>
      {icsFile && (
        <a href={URL.createObjectURL(icsFile)} download="events.ics">
          Download ICS
        </a>
      )}
    </div>
  );
};

export default Spreadsheet;