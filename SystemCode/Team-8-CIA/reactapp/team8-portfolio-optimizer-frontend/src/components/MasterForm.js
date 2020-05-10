import React from "react";
import { useForm } from "react-hook-form";
import { Component } from "react";
import Radiochecklist from "./RadioChecklist"; // importing child component
import Step1 from "./BasicInfo";
import Step2 from "./RiskTolerance1";
import Step3 from "./RiskTolerance2";
import Step4 from "./page5";
import Step5 from "./page6";
import Step6 from "./page7";
class MasterForm extends Component {
  constructor(props) {
    super(props);
    // Set the initial input values
    this.state = {
      currentStep: 1, // Default is Step 1
      basicInfoAns: [],
      answer: [],
      page5_data: [],
      page6_data: {},
      modal_data: [],
      page7_data: {},
      page6_formatted: [],
      changeAge: false,
      changeOA: false,
      changeSA: false,
      changeBankrupt: true,
      showModal: false,
      loading: false,
      errorPopup: false,
      errMsg: "",
    };
    this.handleChange = this.handleChange.bind(this);
    this._next = this._next.bind(this);
    this._prev = this._prev.bind(this);
  }

  // handleChange = event => {
  //   // const { name, value } = event.target;
  //   // this.setState({
  //   //   [name]: value
  //   // });
  // };

  handlebasicInfoPage(event, question) {
    // console.log(event, "event");
    // console.log(`Question ${question}: answer is -> ${JSON.stringify(event)}`);
    let answer = this.state.basicInfoAns;
    answer[question] = event;
    this.state.basicInfoAns = answer;
  }

  handleChange(event, question) {
    // console.log(`Question ${question}: answer is -> ${JSON.stringify(event)}`);
    let answer = this.state.answer;
    if (question == 8) {
      let newResult = [];
      this.state.page6_formatted.map((item) => {
        if (event.includes(item.Code)) newResult.push(item);
      });
      answer[question] = newResult;
      this.state.answer = answer;
    } else if (question < 7) {
      answer[question] = event;
      answer[question] = Number((question + 1).toString() + event.toString());
      this.state.answer = answer;
    } else {
      answer[question] = event;
      this.state.answer = answer;
    }
  }

  handleSubmit = (event) => {
    event.preventDefault();
    const { email, username, password } = this.state;
    alert(`Your registration detail: \n 
           Email: ${email} \n 
           Username: ${username} \n
           Password: ${password}`);
  };

  _next = () => {
    // console.log("next", this.state.currentStep);
    // console.log(this.state.basicInfoAns, "basicInfo");
    // console.log(this.state.answer, "answer");
    let currentStep = this.state.currentStep;
    // If the current step is 1 or 2, then add one on "next" button click
    if (currentStep === 3) {
      let param = {
        Data: {
          Rules: this.state.answer.slice(0, 7),
        },
      };
      let headers = new Headers();
      headers.append("Content-Type", "application/json");
      headers.append("Accept", "application/json");
      headers.append("Access-Control-Allow-Origin", "*");
      headers.append("GET", "POST", "OPTIONS");

      console.log(JSON.stringify(param));

      // fetch("http://www.mocky.io/v2/5eb509e40e00001d42081eeb", {
        fetch("http://localhost:5000/rules", {
        method: "POST",
        // mode: "cors",
        // headers: headers,
        body: JSON.stringify(param),
      })
        .then((res) => res.json())
        .then(
          (result) => {
            // console.log(result);
            if (!result.Data.Error) {
              // fetch("http://www.mocky.io/v2/5eaa841f2d000095002686ba")
                fetch("http://localhost:5000/categories")
                .then((res) => res.json())
                .then(
                  (result) => {
                    // console.log(result);
                    this.setState({ page5_data: result.Data });
                    currentStep = currentStep + 1;
                    this.setState({
                      currentStep: currentStep,
                    });
                  },
                  (error) => {}
                );
            } else {
              this.setState({ errorPopup: true });
              this.setState({ errMsg: result.Data.Error });
            }
          },
          (error) => {}
        );
    } else {
      currentStep = currentStep + 1;
      this.setState({
        currentStep: currentStep,
      });
    }
  };

  _prev = () => {
    let currentStep = this.state.currentStep;
    // If the current step is 2 or 3, then subtract one on "previous" button click
    currentStep = currentStep <= 1 ? 1 : currentStep - 1;
    this.setState({
      currentStep: currentStep,
    });
  };

  _submit = () => {
    let currentStep = this.state.currentStep;
    console.log(this.state.answer, "answer");
    console.log(this.state.basicInfoAns, "basic info ans");
    //params
    let param = {
      Data: this.state.answer[7],
    };

    let headers = new Headers();
    headers.append("Content-Type", "application/json");
    headers.append("Accept", "application/json");
    headers.append("Access-Control-Allow-Origin", "*");
    headers.append("GET", "POST", "OPTIONS");

    console.log(param, "API para for page 5 ");
    console.log(JSON.stringify(param));
    //call api
    // fetch("http://www.mocky.io/v2/5eae64e22f00006600198943", {
      fetch("http://localhost:5000/categories/curated", {
      method: "POST",
      // mode: "cors",
      // headers: headers,
      body: JSON.stringify(param),
    })
      .then((res) => res.json())
      .then(
        (result) => {
          console.log(result, "asdhjadsjasd");
          this.setState({ page6_data: result.Data });
          let formatted = [];
          Object.keys(result.Data).map(function (key) {
            result.Data[key].map((item) => {
              formatted.push({
                Name: item[0],
                Code: item[1],
              });
            });
          });
          this.setState({ page6_formatted: formatted });
        },
        (error) => {}
      );

    // next step
    currentStep = currentStep = currentStep + 1;
    this.setState({
      currentStep: currentStep,
    });
  };

  _submit2 = () => {
    let currentStep = this.state.currentStep;
    console.log(this.state.answer, "answer");
    console.log(this.state.basicInfoAns, "basic info ans");
    //params
    let param = {
      Data: {
        Rules: this.state.answer.slice(0, 7),
        Selected_Stocks: this.state.answer[8],
        CPFOA: this.state.basicInfoAns[3],
        CPFSA: this.state.basicInfoAns[4],
      },
    };

    console.log(param, "API param for last page");
    //call api
    // fetch("http://www.mocky.io/v2/5eaf91ab3300004b009f446c", {
      fetch("http://localhost:5000/decisiontree", {
      method: "POST",
      body: JSON.stringify(param),
    })
      .then((res) => res.json())
      .then(
        (result) => {
          console.log(result, "this is an object");
          let formatted = [];
          Object.keys(result.Data).map(function (key) {
            formatted.push({
              key: key,
              value: result.Data[key],
            });
          });
          this.setState({ modal_data: formatted });
          this.setState({ showModal: true });
        },
        (error) => {}
      );
  };

  _submit3 = () => {
    this.setState({ loading: true });
    let currentStep = this.state.currentStep;
    console.log(this.state.answer, "answer");
    console.log(this.state.basicInfoAns, "basic info ans");
    //params
    let param = {
      Data: {
        Rules: this.state.answer.slice(0, 7),
        Selected_Stocks: this.state.answer[8],
        CPFOA: this.state.basicInfoAns[3],
        CPFSA: this.state.basicInfoAns[4],
      },
    };

    console.log(param, "API param for last page");
    //call api
    // fetch("http://www.mocky.io/v2/5eae74a62f00006800198964", {
      fetch("http://localhost:5000/ga", {
      method: "POST",
      body: JSON.stringify(param),
    })
      .then((res) => res.json())
      .then(
        (result) => {
          // console.log(result);
          setTimeout(() => {
            this.setState({ page7_data: result.Data });
            this.setState({ showModal: true });
            this.setState({ loading: false });
            currentStep = currentStep = currentStep + 1;
            this.setState({
              currentStep: currentStep,
            });
          }, 3000);
        },
        (error) => {}
      );
  };

  //button functions

  previousButton() {
    let currentStep = this.state.currentStep;
    if (currentStep !== 1) {
      return (
        <button
          className="btn btn-secondary"
          type="button"
          onClick={this._prev}
        >
          Previous
        </button>
      );
    }
    return null;
  }
  nextButton() {
    let currentStep = this.state.currentStep;

    if (currentStep < 4) {
      return (
        <button
          className="btn btn-primary float-right"
          type="button"
          onClick={() => this._next()}
          disabled={
            !this.state.changeAge ||
            this.state.changeBankrupt ||
            !this.state.changeOA ||
            !this.state.changeSA
          }
        >
          {!this.state.changeAge ||
          this.state.changeBankrupt ||
          !this.state.changeOA ||
          !this.state.changeSA
            ? "Please fill up the fields to proceed"
            : "Next"}
        </button>
      );
    }
    return null;
  }

  submitButton() {
    let currentStep = this.state.currentStep;
    if (currentStep === 4 || currentStep === 5) {
      return (
        <button
          className="btn btn-success float-right"
          type="button"
          onClick={currentStep === 4 ? this._submit : this._submit2}
        >
          Submit
        </button>
      );
    }
    return null;
  }

  restart() {
    this.setState({ currentStep: 1 });
    this.setState({ basicInfoAns: [] });
    this.setState({ answer: [] });
    this.setState({ page5_data: [] });
    this.setState({ page6_data: {} });
    this.setState({ modal_data: [] });
    this.setState({ page7_data: {} });
    this.setState({ page6_formatted: [] });
    this.setState({ changeAge: false });
    this.setState({ changeOA: false });
    this.setState({ changeSA: false });
    this.setState({ changeBankrupt: true });
    this.setState({ showModal: false });
    this.setState({ loading: false });
    this.setState({ errorPopup: false });
    this.setState({ errMsg: "" });
  }
  render() {
    var style = {
      display: "flex",
      justifyContent: "space-between",
      width: "100%",
      padding: "50px 0",
    };

    let textStyle = {
      textAlign: "center",
      paddingTop: "30px",
    };
    return (
      <React.Fragment>
        <h1>CPF Investment Advisor</h1>

        <h2>
          Investing is an effective way to put your money to work and build
          wealth. Kickstart your investment planning with us! Just fill up a
          short questionaire below
        </h2>

        <h3 style={textStyle}>Step {this.state.currentStep} </h3>
        

        <form onSubmit={this.handleSubmit}>
          <Step1
            currentStep={this.state.currentStep}
            handleChange={(event, qn) => this.handlebasicInfoPage(event, qn)}
            changeAge={(changeAge) => this.setState({ changeAge })}
            changeOA={(changeOA) => this.setState({ changeOA })}
            changeSA={(changeSA) => this.setState({ changeSA })}
            changeBankrupt={(changeBankrupt) =>
              this.setState({ changeBankrupt })
            }
          />
          <Step2
            currentStep={this.state.currentStep}
            handleChange={(event, qn) => this.handleChange(event, qn)}
            checkboxvalue={this.state.checkboxvalue}
            username={this.state.username}
          />
          <Step3
            currentStep={this.state.currentStep}
            handleChange={this.handleChange}
            password={this.state.password}
            isError={this.state.errorPopup}
            errorMsg={this.state.errMsg}
            restart={() => this.restart()}
          />
          <Step4
            currentStep={this.state.currentStep}
            handleChange={this.handleChange}
            data={this.state.page5_data}
          />
          <Step5
            currentStep={this.state.currentStep}
            handleChange={this.handleChange}
            data={this.state.page6_data}
            showModal={this.state.showModal}
            hideModal={() => this.setState({ showModal: false })}
            changeShowModal={(showModal) => this._submit3(showModal)}
            modalData={this.state.modal_data}
            loading={this.state.loading}
          />
          <Step6
            currentStep={this.state.currentStep}
            handleChange={this.handleChange}
            data={this.state.page7_data}
          />
          <div style={style}>
            {this.previousButton()}
            {this.nextButton()}
            {this.submitButton()}
          </div>
        </form>
      </React.Fragment>
    );
  }
}

export default MasterForm;
