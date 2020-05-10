import React, { Component } from "react";
import { Radio, Input } from "antd";
import { Select } from "antd";
import { Checkbox, Row, Col } from "antd";
import _ from "lodash";

const { Option } = Select;

class step3 extends Component {
  state = {
    data: [],
    ans: [],
    isMax: false,
    notBlocked: [],
    checked: [],
    visible: false,
  };

  onChange = (checkedValues) => {
    this.setState(() => {
      return { checked: checkedValues };
    });
    this.props.handleChange(checkedValues, 7);
  };

  isDisabled = (id) => {
    console.log(id);
    return (
      this.state.checked.length > 1 && this.state.checked.indexOf(id) === -1
    );
  };

  checkMax(event) {
    this.props.handleChange(event, 7);
  }

  render() {
    const { data } = this.props;
    const { checked } = this.state;
    if (this.props.currentStep !== 4) {
      return null;
    }
    return (
      <div>
        <h2>Sectors to Invest in</h2>
        <label>
          Please select your sector of interest to invest in: Select up to 5
          sectors
        </label>
        <Checkbox.Group style={{ width: "100%" }} onChange={this.onChange}>
          <Row>
            {!_.isEmpty(data)
              ? data.map((item) => {
                  return (
                    <Col span={8}>
                      <Checkbox
                        value={item}
                        disabled={
                          checked.length > 3 && checked.indexOf(item) === -1
                        }
                      >
                        {item}
                      </Checkbox>
                    </Col>
                  );
                })
              : null}
          </Row>
        </Checkbox.Group>
      </div>
    );
  }
}

export default step3;
