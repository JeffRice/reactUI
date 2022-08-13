import React, { Component } from 'react';
 
 
class Listings extends Component {
 
    constructor(props) {
        super(props)   
        this.state = {
            records: []
        }
         
    }
 
    componentDidMount() {
        console.log('mounted')
        fetch('http://127.0.0.1:5103/calculations', {  // Enter your IP address here

        method: 'GET', 
        mode: 'cors', 
        headers:{'Content-Type': 'application/json'  }
        
    })  
            .then(response => response.json())
            .then(records => {
                this.setState({
                    records: records
                })
            })
            .catch(error => console.log(error))
    }
 
    render() {
        let records = this.state.records;
        return (
          <div>
              <ul>
                  {Object.keys(records).map((record, index) => <li key={index}>{records} : {records[record]}</li>)}
              </ul>
          </div>
      )
    }
}
 
export default Listings;