import React, { useState, FormEvent } from 'react';
import { CSVReader } from 'react-papaparse';
import fileDownload from 'js-file-download';

import './App.css';
import { api } from './services/api';

interface DataArray {
  data: string[];
}

type Data = Array<DataArray>;

interface SubmitData {
  url: string;
  uppercase: boolean;
  filter: string[];
}

const App: React.FC = () => {
  const [url, setUrl] = useState('');
  const [uppercase, setUppercase] = useState(false);
  const [filter, setFilter] = useState<string[]>([]);

  // advide: nerver use setState inside loops
  function handleParseFilter(data: Data): void {
    const words = data.map((col) => col.data[0]).filter(Boolean);
    setFilter((prevFilter) => prevFilter.concat(words));
  }

  async function handleSubmit(e: FormEvent): Promise<void> {
    e.preventDefault();
    try {
      const submitData: SubmitData = {
        url,
        uppercase,
        filter,
      };

      await api.post('words', submitData);
      const res = await api.get('files');
      fileDownload(res.data, 'words_count.csv');
    } catch (err) {
      console.log(err);
    }
  }

  return (
    <div id="container">
      <form onSubmit={handleSubmit}>
        <header>
          <h1>Reddit Word Count Bot!</h1>
        </header>
        <main>
          <label>
            Reddit thread link
            <input
              name="url"
              required
              onChange={({ target }) => setUrl(target.value)}
            />
          </label>
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
            <CSVReader
              onDrop={handleParseFilter}
              addRemoveButton
              removeButtonColor="#659cef"
              onRemoveFile={() => setFilter([])}
              style={{ width: '30vw' }}
            >
              <span>Drop CSV file here or click to upload.</span>
            </CSVReader>
          </div>
        </main>
      </form>
    </div>
  );
};

export default App;
