import React from 'react';
 
 
class NewCalcForm extends React.Component {
    constructor(props) {
      super(props);
  //    this.state = {calc_type: 'Purple', Foo: 0,Bar: 1, Baz: 2};
      this.state = {
        calc_type: 'Purple', Foo: '0',Bar: '0', Baz: '0', errors: {}, submitDisabled: false };

  
      this.handleInputChange = this.handleInputChange.bind(this);
      this.handleSubmit = this.handleSubmit.bind(this);
      this.handleValidation = this.handleValidation.bind(this);

    }

    handleValidation() {
      let errors = {};

      const fooValue = parseFloat(this.state.Foo)
      const barValue = parseFloat(this.state.Bar)
      const bazValue = parseFloat(this.state.Baz)


      //Foo, Bar, Baz Validations
      if (!Number.isInteger(fooValue)){
        errors["Foo"] = "Please enter an integer between -10 and 10";
      }
      else if  (fooValue > 10 || fooValue < -10){
        errors["Foo"] = "Please enter an integer between -10 and 10";
      }

      else if (isNaN(barValue)){
        errors["Bar"] = "Please enter a number ";

      }
      else if (isNaN(bazValue)){
        errors["Baz"] = "Please enter a number ";

      }
      else if (bazValue > 10 || bazValue < 0){
        errors["Baz"] = "Please enter a number between 0 and 10";
      }
      //no errors
      else {
        errors = {};  
        this.setState({ errors: 'none', submitDisabled: false });
      }
      //if there is an error, update the error object and disable form
       if (Object.keys(errors).length !== 0){
          this.setState({ errors: errors, submitDisabled: true }); 
        }

      }
    
  
    handleInputChange(event) {
        const target = event.target;
        const value = target.type === 'checkbox' ? target.checked : target.value;
        const name = target.name;

        this.setState({
          [name]: value
        });


         setTimeout(() => {this.handleValidation()}, 50);
      }  

    handleSubmit(event) {

      event.preventDefault();

      //make sure form is valid
      this.handleValidation()


      let jsonData = {calc_type: this.state.calc_type, foo: this.state.Foo ,bar: this.state.Bar, baz: this.state.Baz}
      // Send data to the backend via POST
      fetch('http://localhost:5103/calculations', {  
        method: 'POST', 
        mode: 'cors', 
        headers:{'content-type': 'application/json'},
        body: JSON.stringify(jsonData) 
      })  
      .then((response) => response.json())
      .then((data) => {
          console.log('Success:', data);
        })
      .catch(err => { console.log(JSON.stringify(err) ) 
      });

    }
  
    render() {
      return (
        <form onSubmit={this.handleSubmit}>
          <label>
            Calc Type:
            <select name="calc_type" value={this.state.calc_type} onChange={this.handleInputChange}>
              <option value="Blue">Blue</option>
              <option value="Green">Green</option>
              <option value="Purple">Purple</option>
              <option value="Yellow">Yellow</option>
            </select>
          </label>
          <label>
            Foo:        
             <input
            name="Foo"
            type="number"
            value={this.state.Foo}
            onChange={this.handleInputChange}  /> 
          </label>
          <span style={{ color: "red" }}>{this.state.errors["Foo"]}</span>
          <label>
            Bar:        
             <input
            name="Bar"
            type="number"
            value={this.state.Bar}
            onChange={this.handleInputChange} /> 
          </label>
          <span style={{ color: "red" }}>{this.state.errors["Bar"]}</span>
          <label>
            Baz:        
             <input
            name="Baz"
            type="number"
            value={this.state.Baz}
            onChange={this.handleInputChange} /> 
          <input type="submit" value="Submit" disabled={this.state.submitDisabled} />
          </label>
          <span style={{ color: "red" }}>{this.state.errors["Baz"]}</span>
        </form>

      );
    }
  }
 
export default NewCalcForm;