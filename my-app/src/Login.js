function Login() {

  let jsonData = {
     "username": "fred", "password": "password" 
  }

  function handleClick() {
    
    // Send data to the backend via POST
    fetch('http://localhost:5103/login', {  // Enter your IP address here

      method: 'POST', 
      mode: 'cors', 
      headers:{'content-type': 'application/json'},
      body: JSON.stringify(jsonData) // body data type must match "Content-Type" header

    })  
    .then((response) => response.json())
    .then((data) => {
        console.log('Success:', data);
      })
    .catch((error) => {
        console.error('Error:', error);
      });



  }

  return (
      
    <button onClick={handleClick} >
      login    </button>
  );

}

export default Login;