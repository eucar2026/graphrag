import { useState, useEffect } from 'react';

function Databases() {

    const [databases, setDatabases] = useState(null)
    const [progress, setProgress] = useState(true)
    const [error, setError] = useState(null)


    const fetchData = async (method, data) => {
        setProgress(true);
        try {
            let url = '/api/databases';
            const options = {
                method,
                headers: {
                    'Content-Type': 'application/json'
                }
            };
            if (method === 'POST') options.body = JSON.stringify(data);
            if (method === 'DELETE') url += `?${data}`;
            const response = await fetch(url, options);
            if (!response.ok)
                throw new Error(`HTTP error! status: ${response.status}`);
            return response.json();
        } 
        catch (error) {
            setError(error);
        } 
        finally {
            setProgress(false);
        }
    };
    
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
                        <td>{db.db_id}</td>
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

export default Databases