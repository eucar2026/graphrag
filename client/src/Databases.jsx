import { useState, useEffect } from 'react';

function Databases() {

    const [databases, setDatabases] = useState(null)
    const [progress, setProgress] = useState(true)
    const [error, setError] = useState(null)


    const fetchData = async (method, data) => {
        setProgress(true);
        try {
            const options = {
                method,
                headers: {
                    'Content-Type': 'application/json'
                }
            };
            if (method === 'POST') options.body = JSON.stringify(data);
            const response = await fetch('/api/databases', options);
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

    const addDatabase = async e => {
        const dbName = prompt('Name your database: ');
        if (!dbName) return;
        const response = await fetchData('POST', { dbName });
        console.log(response);
        await getDatabases();
    };

    return <div>
        <h2>Databases</h2>
        <button onClick={addDatabase}>Add Database</button>
        {progress && <progress/>}
        {error && <div className="error">{error.message}</div>}
        <div className="center">
            {databases && <table className="list">
                <tbody>
                    {databases.map(database => <tr key={database}>
                        <td>{database}</td>
                        {/* to do: add links here with dbIDs, requires server change */}
                    </tr>)}
                </tbody>
            </table>}
        </div>
    </div>
}

export default Databases