import React, { Component } from "react";
import { Radio, Input } from "antd";
import { Select } from "antd";
import { Modal, Button } from "antd";
const { Option } = Select;
class step3 extends Component {
  state = {
    data: [
      {
        question: "5. Select the investments you currently own",
        default: "1",
        options: [
          {
            key: "1",
            value: "Bonds and/or bond funds",
          },
          {
            key: "2",
            value: "Stocks and/or stock funds",
          },
          {
            key: "3",
            value: "International securities and/ or international funds",
          },
        ],
      },
      {
        question:
          "6. Consider this scenario: Imagine that in the past three months, the overall stock market lost 25% of its value. An individual stockinvestment you own also lost 25% of its value. What would you do?",
        default: "1",
        options: [
          {
            key: "1",
            value: "Sell all of my shares",
          },
          {
            key: "2",
            value: "Sell some of my shares",
          },
          {
            key: "3",
            value: "Do nothing",
          },
          {
            key: "4",
            value: "Buy more shares",
          },
        ],
      },
      {
        question:
          "7. We’ve outlined the most likely best-case and worst-case annual returns of five hypothetical investment plans. Which range of possible outcomes is most acceptable to you? The figures are hypothetical and do not represent the performance of any particular investment.",
        default: "1",
        options: [
          {
            key: "1",
            value: "Average Annual Returns: 7.2% , Best-Case: 16.3%, Worst-Case: -5.6%",
          },
          {
            key: "2",
            value: "Average Annual Returns: 9.0%, Best-Case: 25.0%, Worst-Case: -12.1%",
          },
          {
            key: "3",
            value: "Average Annual Returns: 10.4%, Best-Case: 33.6%, Worst-Case: -18.2%",
          },
          {
            key: "4",
            value: "Average Annual Returns: 11.7%, Best-Case: 42.8%, Worst-Case: -24.0%",
          },
          {
            key: "5",
            value: "Average Annual Returns: 12.5%, Best-Case: 50.0%, Worst-Case: -28.2%",
          },
        ],
      },
    ],
  };

  render() {
    const { data } = this.state;
    if (this.props.currentStep !== 3) {
      return null;
    }
    return (
      <div>
        <h2>Time Horizon And Risk Tolerance Part II</h2>
        <label>{data[0].question}</label>
        <Select
          style={{ width: "100%" }}
          onChange={(event) => this.props.handleChange(event, 4)}
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
          onChange={(event) => this.props.handleChange(event, 5)}
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
          onChange={(event) => this.props.handleChange(event, 6)}
        >
          {data[2].options.map((item) => {
            return (
              <Option key={item.key} value={item.key}>
                {item.value}
              </Option>
            );
          })}
        </Select>
        <Modal
          title="Patience is bitter, but its fruit is sweet"
          visible={this.props.isError}
          footer={[
            <Button
              key="submit"
              type="primary"
              onClick={() => this.props.restart()}
            >
              Home
            </Button>,
          ]}
        >
          <label>{this.props.errorMsg}</label>
        </Modal>
      </div>
    );
  }
}

export default step3;
