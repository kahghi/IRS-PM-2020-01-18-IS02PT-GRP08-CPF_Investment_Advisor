import React from "react";
import { useForm } from "react-hook-form";
import { Component } from "react";
import { Form, Input, Button, Checkbox, Select } from "antd";
import { UserOutlined, DesktopOutlined } from "@ant-design/icons";
const { Option } = Select;
class step1 extends Component {
  state = {
    aboveAge: true,
    isBankrupt: false,
    sufficientOA: true,
    sufficientSA: true,
  };
  checkAge(e) {
    // console.log(e.target.value, "age");
    if (e.target.value < 18) {
      this.setState({ aboveAge: false });
      this.props.changeAge(false);
    } else {
      this.setState({ aboveAge: true });
      this.props.changeAge(true);
      this.props.handleChange(e.target.value, 1);
    }
  }

  checkOA(e) {
    // console.log(e.target.value, "oa");
    if (e.target.value < 20000) {
      this.setState({ sufficientOA: false });
      this.props.changeOA(false);
    } else {
      this.setState({ sufficientOA: true });
      this.props.changeOA(true);
      this.props.handleChange(e.target.value, 3);
    }
  }

  checkSA(e) {
    // console.log(e.target.value, "sa");
    if (e.target.value < 40000) {
      this.setState({ sufficientSA: false });
      this.props.changeSA(false);
    } else {
      this.setState({ sufficientSA: true });
      this.props.changeSA(true);
      this.props.handleChange(e.target.value, 4);
    }
  }

  checkBankrupt(e) {
    // console.log(e, "age");
    if (e === "yes") {
      this.setState({ isBankrupt: true });
      this.props.changeBankrupt(true);
    } else {
      this.setState({ isBankrupt: false });
      this.props.changeBankrupt(false);
      this.props.handleChange(e, 2);
    }
  }
  render() {
    if (this.props.currentStep !== 1) {
      // Prop: The current step
      return null;
    }
    // The markup for the Step 1 UI
    return (
      <div>
        <h2>Basic Information</h2>
        <h2>
          Welcome to CPF Investment Advisor (CIA) Here we hope to aid you in
          your stock investments :)
        </h2>
        <br />
        <label>Name</label>
        <Input
          size="large"
          placeholder="Name"
          onChange={(event) => this.props.handleChange(event.target.value, 0)}
        />
        <br />
        <label>Age</label>
        <Input
          size="large"
          placeholder="Age"
          onChange={(event) => this.checkAge(event)}
        />
        <div style={{ color: "red" }}>
          {!this.state.aboveAge
            ? "Below Age Limit"
            : ""}
        </div>

        <label>Are you an undischarged bankrupt?</label>
        <Select
          style={{ width: "100%" }}
          onChange={(event) => this.checkBankrupt(event)}
        >
          <Option key="yes" value="yes">
            Yes
          </Option>
          <Option key="no" value="no">
            No
          </Option>
          })}
        </Select>
        <div style={{ color: "red" }}>
          {this.state.isBankrupt ? "We are unable to proceed with your current status" : ""}
        </div>

        <br />
        <label>Amount in CPF OA:</label>
        <Input
          size="large"
          placeholder="CPF OA"
          onChange={(event) => this.checkOA(event)}
        />
        <div style={{ color: "red" }}>
          {!this.state.sufficientOA
            ? "I'm sorry, please ensure that you have the minimum amount of $20,000 in your OA account"
            : ""}
        </div>

        <br />
        <label>Amount in CPF SA:</label>
        <Input
          size="large"
          placeholder="CPF SA"
          onChange={(event) => this.checkSA(event)}
        />
        <div style={{ color: "red" }}>
          {!this.state.sufficientSA
            ? "I'm sorry, please ensure that you have the minimum amount of $40,000 in your SA account"
            : ""}
        </div>
      </div>

      // <div className="form-group">
      //   <label htmlFor="Name">Name</label>
      //   <input
      //     name="Name"
      //     placeholder="Enter Your Name"
      //     id="name"
      //     value={this.props.name}
      //     onChange={this.props.handleChange}
      //   />

      //   <label htmlFor="email">Email address</label>
      //   <input
      //     className="form-control"
      //     id="email"
      //     name="email"
      //     type="text"
      //     placeholder="Enter email"
      //     value={this.props.email} // Prop: The email input data
      //     onChange={this.props.handleChange} // Prop: Puts data into state
      //   />
      // </div>
    );
  }
}
export default step1;
