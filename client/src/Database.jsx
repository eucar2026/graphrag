import { useState, useEffect } from 'react';
import { useParams } from 'react-router';
import getFetchData from './fetchData';
import './Database.css';

function Database() {
    const { dbId } = useParams();

    const [files, setFiles] = useState(null);
    const [progress, setProgress] = useState(true);
    const [error, setError] = useState(null);
    const [result, setResult] = useState(null);

    const fetchFiles = getFetchData('/api/files', setError, setProgress);
    const fetchQuery = getFetchData('/api/query', setError, setProgress);
    
    const getFiles = async () => {
      const dbs = await fetchFiles('GET', `dbId=${dbId}`);
      setFiles(dbs);
    };

    useEffect(() => { getFiles(); }, []); 

    const addFiles = async event => {
        setProgress(true);
        try {
            const formData = new FormData();
            formData.append('file', event.target.files[0]);
            console.log(event.target.files);
            const response = await fetch(`/api/files?dbId=${dbId}`, { method: 'POST', body: formData });
            if (!response.ok)
                throw new Error(`HTTP error! status: ${response.status}`);
            await getFiles();
        } 
        catch (error) {
            setError(error);
        } 
        finally {
            setProgress(false);
        }
    };

    const deleteFile = async dbId => {
        if (!confirm('Are you sure you want to delete this file? ')) return;
        await fetchFiles('DELETE', `dbId=${dbId}`);
        await getFiles();
    };

    const queryDatabase = async () => {
        const response = await fetchQuery('GET', `dbId=${dbId}&prompt=${document.getElementById('query').value}`);
        console.log(response);
        setResult(response);
    };

    return <div>
        <h2>Database ID: {dbId}</h2>
        <div className="upload">
            <label>Upload files</label>
            <input type="file" multiple={false} onChange={addFiles}></input>
        </div>
        <div className="qarea">
            <label>Query</label>
            <textarea id="query"></textarea>
            <button onClick={queryDatabase}>Submit</button>
        </div>
        {result && <div className="results">
            <label>Result: </label>
            <span>{result}</span>
        </div>}
        {progress && <progress/>}
        {error && <div className="error">{error.message}</div>}
        <div className="center">
            {files && <table className="list">
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Name</th>
                        <th>Options</th>
                    </tr>
                </thead>
                <tbody>
                    {files.map(file => <tr key={file.file_id}>
                        <td>{file.file_id}</td>
                        <td>{file.file_name}</td>
                        <td>
                            <a onClick={() => deleteFile(file.file_id)}>Delete</a>
                        </td>
                    </tr>)}
                </tbody>
            </table>}
        </div>
    </div>
}

export default Database;