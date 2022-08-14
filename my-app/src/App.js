import './App.css';
import {
  BrowserRouter as Router,
  Routes,
  Route,
  Link
} from "react-router-dom";
import TableListing from './TableListing';
import SecondPlot from './SecondPlot';

function App() {
  return (
    <div className="App">
      <header className="App-header">   
      </header>
        <Router>
          <ul className="links">
            <li>
              <Link to="/">To Table Listing</Link>
            </li>
            <li>
              <Link to="/secondplot">To secondplot</Link>
            </li>
          </ul>
          <Routes>
            <Route path="/" element={<TableListing />} />
            <Route path="/secondplot" element={<SecondPlot />} />
        	  <Route path="/secondplot/:id" element={<SecondPlot />} render={(props) => (
              <SecondPlot id={props.match.params.id}/>
                )} />
          </Routes>
        </Router>


    </div>
  );
}

export default App;
