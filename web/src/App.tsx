import React, { useState } from 'react';

import './App.css';

const App: React.FC = () => {
  const [url, setUrl] = useState('');
  const [uppercase, setUppercase] = useState(false);

  async function handleSubmit() {}

  return (
    <div id="container">
      <form onSubmit={handleSubmit}>
        <header>
          <h1>Reddit Word Count Bot!</h1>
        </header>
        <main>
          <input
            name="url"
            required
            onChange={({ target }) => setUrl(target.value)}
          />
          <button type="submit">Generate CSV</button>
          <div id="options">
            <label>
              Uppercase Only
              <input
                type="checkbox"
                name="uppercase"
                onChange={({ target }) => setUppercase(target.checked)}
              />
            </label>
            <br />
            <label>
              Upload a CSV containing words to not include
              <input type="file" name="filter" accept=".csv" />
            </label>
          </div>
        </main>
      </form>
    </div>
  );
};

export default App;
