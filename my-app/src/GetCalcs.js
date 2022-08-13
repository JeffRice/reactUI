function Login() {



  function handleClick() {
    
    
    fetch('http://127.0.0.1:5103/calculations', {  // Enter your IP address here

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
      Get calculations
    </button>
  );

}

export default Login;