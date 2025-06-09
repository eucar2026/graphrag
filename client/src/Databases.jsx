import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router';
import getFetchData from './fetchData';

function Databases() {
    const navigate = useNavigate();

    const [databases, setDatabases] = useState(null);
    const [progress, setProgress] = useState(true);
    const [error, setError] = useState(null);

    const fetchData = getFetchData('/api/databases', setError, setProgress);
    
    const getDatabases = async () => {
      const dbs = await fetchData('GET');
      setDatabases(dbs);
    };

    useEffect(() => { getDatabases(); }, []); 

    const addDatabase = async () => {
        const dbName = prompt('Name your database: ');
        if (!dbName) return;
        await fetchData('POST', { dbName });
        await getDatabases();
    };

    const deleteDatabase = async dbId => {
        if (!confirm('Are you sure you want to delete this database? ')) return;
        await fetchData('DELETE', `dbId=${dbId}`);
        await getDatabases();
    };

    return <div>
        <h2>Databases</h2>
        <button onClick={addDatabase}>Add Database</button>
        {progress && <progress/>}
        {error && <div className="error">{error.message}</div>}
        <div className="center">
            {databases && <table className="list">
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Name</th>
                        <th>Options</th>
                    </tr>
                </thead>
                <tbody>
                    {databases.map(db => <tr key={db.db_id}>
                        <td>
                            <a onClick={() => navigate(`/files/${db.db_id}`)}>{db.db_id}</a>
                        </td>
                        <td>{db.db_name}</td>
                        <td>
                            <a onClick={() => deleteDatabase(db.db_id)}>Delete</a>
                        </td>
                    </tr>)}
                </tbody>
            </table>}
        </div>
    </div>
}

export default Databases;