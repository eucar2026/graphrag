import { useState, useEffect } from 'react';
import { useParams } from 'react-router';
import getFetchData from './fetchData';

function Files() {
    const { dbId } = useParams();

    const [files, setFiles] = useState(null);
    const [progress, setProgress] = useState(true);
    const [error, setError] = useState(null);

    const fetchData = getFetchData('/api/files', setError, setProgress);
    
    const getFiles = async () => {
      const dbs = await fetchData('GET', `dbId=${dbId}`);
      setFiles(dbs);
    };

    useEffect(() => { getFiles(); }, []); 

    const addFile = async () => {
        const dbName = prompt('Name your file: ');
        if (!dbName) return;
        await fetchData('POST', { dbName });
        await getFiles();
    };

    const deleteFile = async dbId => {
        if (!confirm('Are you sure you want to delete this file? ')) return;
        await fetchData('DELETE', `dbId=${dbId}`);
        await getFiles();
    };

    return <div>
        <h2>Files</h2>
        <button onClick={addFile}>Add File</button>
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

export default Files;