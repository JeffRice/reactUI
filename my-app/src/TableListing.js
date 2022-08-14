import React, { Component } from 'react';
import NewCalcForm from './NewCalcForm';
 
class TableListing extends Component {
 
    constructor(props) {
        super(props)   
        this.state = {
            records: []
        }
         
    }
 
    componentDidMount() {



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
        let recordList = [];

        recordList.sort((a, b) => (a.started_at > b.started_at) ? 1 : -1);
        this.state.records.map((record, index)   => {
            const classes = `calcList ${record.mine}`
            const recordLink = `secondplot/${record.id}`
            return recordList.push(
                    <tr key={index} className={classes}>
                        <td>List index {index} <a href={recordLink}>{record.id} Details Page</a></td>
                        <td>started at is {record.started_at}</td>
                        <td>foo is {record.foo} </td>
                        <td>babar is {record.bar} </td>
                        <td>baz is {record.baz}</td>
                        <td>calc_type is {record.calc_type}</td>
                        <td>fraction complete {record.fraction_complete}</td>
                    </tr>
                    )
        })
 
        return recordList.reverse();
    }
 
    render() {
        return (
            <div>
            <NewCalcForm />                
            <table>
             <thead>
                <tr>
                    <th colSpan='7'>Calculations Table</th>
                </tr>
             </thead>
                 <tbody>

                {this.renderListing()}
           
                </tbody>
            </table>
            </div>
        );
    }
}
 
export default TableListing;