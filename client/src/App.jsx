import { Routes, Route } from 'react-router';
import { BrowserRouter } from 'react-router'
import Header from './Header.jsx';
import Footer from './Footer.jsx';
import Databases from './Databases.jsx';
import Database from './Database.jsx';
import './App.css';

function App() {

  return <div>
    <BrowserRouter>
      <Header/>
      <Routes>
        <Route path="/" element={<Databases />} />
        <Route path="/database/:dbId" element={<Database />} />
      </Routes>
      <Footer/>
    </BrowserRouter>
  </div>
}

export default App
