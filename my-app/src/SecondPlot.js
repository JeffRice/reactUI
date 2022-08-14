import React from 'react';
import Plot from 'react-plotly.js';
import { useParams } from "react-router-dom";

function withParams(Component) {
  return props => <Component {...props} params={useParams()} />;
}


class SecondPlot extends React.Component {



    constructor(props) {
      super(props);
      this.state = {data: [
          {
            x: [1, 2, 3],
            y: [2, 6, 3],
            type: 'scatter',
            mode: 'lines+markers',
            marker: {color: 'red'},
          }
        ],

       layout: {width: 640, height: 480, title: 'A Dynamic Plot'}, frames: [], config: {}}
    }

  


      componentDidMount() {
        let { id } = this.props.params;
        console.log(id);

        this.timerID = setInterval(
            () => this.tick(),
            1000
          );

        this.setState({
          'testid': id
        });
    }

    componentWillUnmount() {
        clearInterval(this.timerID);
    }

    
    tick() {

        let plotData = [{}]

        plotData[0].x = [1, 2, 3 ];
        plotData[0].y = [3, 2, 6, 4];
        plotData[0].type ='scatter';
        plotData[0].mode = 'lines+markers';
        plotData[0].marker = {color: 'red'};

        let { id } = this.props.params;
        let fetchCalcURL = 'http://127.0.0.1:5103/calculations/' + id;

               console.log(fetchCalcURL);

        fetch(fetchCalcURL, {  // Enter your IP address here

        method: 'GET', 
        mode: 'cors', 
        headers:{'Content-Type': 'application/json'  }
        
               })  
            .then(response => response.json())
            .then(data => {



               let xArray = [];
               let xArrayLen = data.values.length;

                 for( let i=1; i< xArrayLen; i++){
                    xArray.push(i);
                  }



               console.log(data.values.length)
               console.log(xArray.length, xArray)



               plotData[0].x = xArray; 
               plotData[0].y = data.values;




                this.setState({
                   data: plotData
                })
            })
            .catch(error => console.log(error))
    }

  render() {
    
    return (
        <div>
            <h2>Calculation: {this.state.testid}</h2>
      <Plot
        data={this.state.data}
        layout={this.state.layout}
        frames={this.state.frames}
        config={this.state.config}
        onInitialized={(figure) => this.setState(figure)}
        onUpdate={(figure) => this.setState(figure)}
      /></div>
    );
  }
}
export default withParams(SecondPlot);