import { Routes, Route } from 'react-router';
import Header from './Header.jsx';
import Footer from './Footer.jsx';
import Databases from './Databases.jsx';
import Files from './Files.jsx';
import './App.css';

function App() {

  return <div>
    <Header/>
      <Routes>
        <Route path="/" element={<Databases />} />
        <Route path="/files/:dbId" element={<Files />} />
      </Routes>
    <Footer/>
  </div>
}

export default App
