const getFetchData = (url, setError, setProgress) => async (method, data) => {
    setProgress(true);
    try {
        const options = {
            method,
            headers: {
                'Content-Type': 'application/json'
            }
        };
        if (method === 'POST') options.body = JSON.stringify(data);
        if (method === 'DELETE' || method === 'GET') url += `?${data}`;
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
export default getFetchData;