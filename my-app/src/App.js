import logo from './logo.svg';
import './App.css';
import Login from './Login';
import GetCalcs from './GetCalcs';
import GetOneCalc from './GetOneCalc';
import TableListing from './TableListing';
import NewCalcForm from './NewCalcForm';

function App() {
  return (
    <div className="App">
      <header className="App-header">   

       <Login />
       <GetCalcs />
       <GetOneCalc />
       <NewCalcForm />
       <TableListing />
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Edit <code>src/App.js</code> and save to reload.
        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
      </header>
    </div>
  );
}

export default App;
