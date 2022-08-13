import React, { Component } from 'react';
 
 
class Listing extends Component {
 
    constructor(props) {
        super(props)   
        this.state = {
            records: []
        }
         
    }
 
    componentDidMount() {

        console.log('mounted')



        this.timerID = setInterval(
            () => this.tick(),
            1000
          );

        fetch('http://127.0.0.1:5103/calculations', {  // Enter your IP address here

        method: 'GET', 
        mode: 'cors', 
        headers:{'Content-Type': 'application/json'  }
        
    })  
            .then(response => response.json())
            .then(data => {
                this.setState({
                    records: data
                })
            })
            .catch(error => console.log(error))
    }

    componentWillUnmount() {
        clearInterval(this.timerID);
    }
    
    tick() {
        fetch('http://127.0.0.1:5103/calculations', {  // Enter your IP address here

        method: 'GET', 
        mode: 'cors', 
        headers:{'Content-Type': 'application/json'  }
        
    })  
            .then(response => response.json())
            .then(data => {
                this.setState({
                    records: data
                })
            })
            .catch(error => console.log(error))
    }


 
    renderListing() {
        let recordList = []

        recordList.sort((a, b) => (a.started_at > b.started_at) ? 1 : -1)

        this.state.records.map((record, index)   => {
            return recordList.push(

            
            <li class='calcListItem' key={record.id}>
                
            index is {index} |
            started at is {record.started_at} | 
            id is {record.id} |
            babar is {record.bar} | 
            baz is {record.baz} | 
            calc_type is {record.calc_type} | 
            </li>)
        })
 
        return recordList;
    }
 
    render() {
        return (
            <ul class='calcList'>
                {this.renderListing()}
            </ul>
        );
    }
}
 
export default Listing;