import React, { Component } from "react";
import { Radio, Input } from "antd";
import { Select } from "antd";
const { Option } = Select;

class step2 extends Component {
  state = {
    data: [
      {
        question:
          "1. I plan to begin withdrawing my money from my investments in:",
        default: "1",
        options: [
          {
            key: "1",
            value: "Less than 3 years",
          },
          {
            key: "2",
            value: "3 - 5 years",
          },
          {
            key: "3",
            value: "6 - 10 years",
          },
          {
            key: "4",
            value: "11 years",
          },
        ],
      },
      {
        question:
          "2. Once I begin withdrawing my funds, I plan to spend all of the funds in:",
        default: "1",
        options: [
          {
            key: "1",
            value: "Less than 3 years",
          },
          {
            key: "2",
            value: "3 - 5 years",
          },
          {
            key: "3",
            value: "6 - 10 years",
          },
          {
            key: "4",
            value: "11 years",
          },
        ],
      },
      {
        question: "3. I would describe my knowledge of investments as:",
        default: "1",
        options: [
          {
            key: "1",
            value: "None",
          },
          {
            key: "2",
            value: "Limited",
          },
          {
            key: "3",
            value: "Good",
          },
          {
            key: "4",
            value: "Extensive",
          },
        ],
      },
      {
        question: "4. When I invest my money, I am:",
        default: "1",
        options: [
          {
            key: "1",
            value: "Most concerned about my investment losing value",
          },
          {
            key: "2",
            value:
              "Equally concerned about my investment losing or gaining value",
          },
          {
            key: "3",
            value: "Most concerned about my investment gaining value",
          },
        ],
      },
    ],
  };

  render() {
    const { data } = this.state;
    if (this.props.currentStep !== 2) {
      // Prop: The current step
      return null;
    }

    return (
      <div>
        <h2>Time Horizon And Risk Tolerance Part I</h2>
        <label>{data[0].question}</label>
        <Select
          style={{ width: "100%" }}
          onChange={(event) => this.props.handleChange(event, 0)}
        >
          {data[0].options.map((item) => {
            return (
              <Option key={item.key} value={item.key}>
                {item.value}
              </Option>
            );
          })}
        </Select>
        <br />
        <br />
        <label>{data[1].question}</label>
        <Select
          style={{ width: "100%" }}
          onChange={(event) => this.props.handleChange(event, 1)}
        >
          {data[1].options.map((item) => {
            return (
              <Option key={item.key} value={item.key}>
                {item.value}
              </Option>
            );
          })}
        </Select>
        <br />
        <br />
        <label>{data[2].question}</label>
        <Select
          style={{ width: "100%" }}
          onChange={(event) => this.props.handleChange(event, 2)}
        >
          {data[2].options.map((item) => {
            return (
              <Option key={item.key} value={item.key}>
                {item.value}
              </Option>
            );
          })}
        </Select>
        <br />
        <br />
        <label>{data[3].question}</label>
        <Select
          style={{ width: "100%" }}
          onChange={(event) => this.props.handleChange(event, 3)}
        >
          {data[3].options.map((item) => {
            return (
              <Option key={item.key} value={item.key}>
                {item.value}
              </Option>
            );
          })}
        </Select>
      </div>
    );
  }
}
export default step2;
