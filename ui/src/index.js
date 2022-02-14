import React from 'react';
import ReactDOM from 'react-dom';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, Brush, ResponsiveContainer } from 'recharts';
import './index.css';
import 'bootstrap/dist/css/bootstrap.css';

//var plot_data = [{"timestamp":"1641138775","current_speed":20.0,"set_speed":20},{"timestamp":"1641138785","current_speed":20.0,"set_speed":30}];
 
class App extends React.Component{
    constructor(props){
        super(props);
        this.state={
            set_speed: 0,
			plot_data: [],
			intervalId: 0
        };
    }
	
    updateInputValue(val){
        this.setState({
            set_speed: val
        });
    }
	
	modifyFormatter = (value, name, props) => {
		const nameJSX = <span><span style={{
		  display: "inline-block",
		  marginRight: "5px",
		  borderRadius: "10px",
		  width: "10px",
		  height: "10px",
		  backgroundColor: props.color
		}}></span>{name} : {value}</span>
		return [nameJSX];
	}
	
	sendData(speed){
		fetch(`http://127.0.0.1:5001/set?speed=${speed}`)
	}
	
	componentDidMount() {
		const newIntervalId = setInterval(() => {
			fetch('http://127.0.0.1:5001/get')
				.then(response => response.json())
				.then((responseData) => {
					if (responseData.length !== this.state.plot_data.length){
						this.setState({plot_data: responseData});
					}
				})				
		}, 2500);
		
	this.setState({intervalId: newIntervalId});
	}

	componentWillUnmount(){
		clearInterval(this.state.intervalId);
	}
	
    render(){
        return(
            <div className='app'>
                <div className='chart'>
					<ResponsiveContainer width={600} height={600}>
						<LineChart
						  width={500}
						  height={300}
						  data={this.state.plot_data}
						  margin={{
							top: 5, right: 30, left: 20, bottom: 5,
						  }}
						>
						  <CartesianGrid />
						  <Legend />
						  <CartesianGrid strokeDasharray="3 3" horizontal={false} vertical={false}/>
						  <XAxis dataKey="timestamp" unit="s"/>
						  <YAxis unit="km/h"/>
						  <Line dataKey="current_speed" stroke="blue"/>
						  <Line dataKey="set_speed" stroke="red"/>
						  <Tooltip formatter={this.modifyFormatter}/>
						<Brush dataKey="timestamp" startIndex={this.state.plot_data.length-16} endIndex={this.state.plot_data.length-1}>
						  <LineChart>
							<Line dataKey="current_speed" stroke="blue"/>
							<Line dataKey="set_speed" stroke="red"/>
						  </LineChart>
						</Brush>
						</LineChart>
					</ResponsiveContainer>
                </div>
                <div className='controller'>
                    <div className='slider'>
                        <input type='range' min='1' max='300' step='1' value={this.state.set_speed} onInput={e => this.setState({set_speed: parseInt(e.target.value)})}/>
                    </div>
                    <div className='manual-control'>
                        <input type='button' className='btn btn-primary' value='-' onClick={() => {if(this.state.set_speed > 0){this.setState({set_speed: parseInt(this.state.set_speed) - 1})}}}></input>
                        <input type='button' className='btn btn-primary' value='+' onClick={() => {if(this.state.set_speed < 300){this.setState({set_speed: parseInt(this.state.set_speed) + 1})}}}></input>
						<span> {this.state.set_speed} km/h</span>
                        <br/>
                        <input type='button' className='btn btn-success' value='Set' onClick={() => this.sendData(this.state.set_speed)}/>
                        <input type='button' className='btn btn-danger' value='Cancel' onClick={() => {this.setState({set_speed: 0});this.sendData(0)}}/>
                    </div>
                </div>
            </div>
        );
    }
}

ReactDOM.render(
    <App />,
    document.getElementById('root')
);