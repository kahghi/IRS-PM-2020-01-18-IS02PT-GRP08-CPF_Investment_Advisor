import React, {Component} from 'react';
import ReactDOM from 'react-dom';
// import 'antd/dist/antd.css';
import { Radio, Input } from 'antd';


class Form extends Component {
        state = {
          value: 1,
        };
      
        onChange = e => {
          console.log('radio checked', e.target.value);
          this.setState({
            value: e.target.value,
          });
        };
      
        render() {
          return (
            
            <Radio.Group onChange={this.onChange} value={this.state.value}>
              <Radio value={1}>A</Radio>
              <Radio value={2}>B</Radio>
              <Radio value={3}>C</Radio>
              <Radio value={4}>D</Radio>
            </Radio.Group>
          );
        }
      }

export default Form 

