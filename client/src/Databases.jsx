import { useState, useEffect } from 'react';

function Databases() {

    const [databases, setDatabases] = useState(null)
    const [progress, setProgress] = useState(true)
    const [error, setError] = useState(null)

    useEffect(() => {
        const fetchData = async () => {
          try {
            const response = await fetch('/api/databases');
            if (!response.ok)
              throw new Error(`HTTP error! status: ${response.status}`);
            const dbs = await response.json();
            setDatabases(dbs);
          } 
          catch (error) {
            setError(error);
          } 
          finally {
            setProgress(false);
          }
        };
        fetchData();
      }, []); 

    return <div>
        <h2>Databases</h2>
        {progress && <progress/>}
        {error && <div className="error">{error.message}</div>}
        {databases && <table className="list">
            {databases.map(database => <tr>
                <td>{database}</td>
                {/* to do: add links here with dbIDs, requires server change */}
            </tr>)}
        </table>}
    </div>
}

export default Databases