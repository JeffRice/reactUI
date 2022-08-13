function GetOneCalc() {

  function handleClick() {
    
    // Send data to the backend via POST
    fetch('http://127.0.0.1:5103/calculations/d0e964b6-72b3-40bb-af0a-b0b12849ffe7', {  // Enter your IP address here

    method: 'GET', 
    mode: 'cors', 
    headers:{'Content-Type': 'application/json'  }
    
})  
    .then((response) => response.json())
    .then((data) => {
        console.log('Success:', data);
      })




  }

  return (
      
    <button onClick={handleClick} >
      Get one calc
    </button>
  );

}

export default GetOneCalc;