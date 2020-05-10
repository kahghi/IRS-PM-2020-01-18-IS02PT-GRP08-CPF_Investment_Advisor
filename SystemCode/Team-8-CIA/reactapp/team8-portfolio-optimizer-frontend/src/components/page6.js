import React, { Component } from "react";
import { Radio, Input } from "antd";
import { Select } from "antd";
import { Checkbox, Row, Col } from "antd";
import _ from "lodash";
import { Modal, Button } from "antd";
import { Table, Tag } from "antd";
const { Option } = Select;
const columns = [
  {
    title: "Stock",
    dataIndex: "key",
    key: "key",
  },
  {
    title: "Yield",
    dataIndex: "value",
    key: "value",
  },
];
class step5 extends Component {
  state = {
    data: [],
    ans: [],
    isMax: false,
    checked: [],
    visible: false,
  };
  componentDidMount() {}

  // showModal = () => {
  //   this.setState({
  //     visible: true,
  //   });
  // };

  handleOk = (e) => {
    this.props.changeShowModal(false);
  };

  onChange = (checkedValues) => {
    this.setState(() => {
      return { checked: checkedValues };
    });
    this.props.handleChange(checkedValues, 8);
  };

  isDisabled = (id) => {
    console.log(id);
    return (
      this.state.checked.length > 1 && this.state.checked.indexOf(id) === -1
    );
  };

  render() {
    const { data } = this.props;
    const { checked } = this.state;
    if (this.props.currentStep !== 5) {
      return null;
    }

    return (
      <div>
        <h2>Companies to Invest in</h2>
        <label>
          Please select your preference of stocks to invest in: (Select up to 4
          stocks in total from the displayed choices)
        </label>
        <Checkbox.Group style={{ width: "100%" }} onChange={this.onChange}>
          {!_.isEmpty(data)
            ? Object.keys(data).map(function (key) {
                return (
                  <div>
                    <label>{key}</label>
                    <Row>
                      {data[key].map((item) => {
                        return (
                          <Col span={8}>
                            <Checkbox
                              value={item[1]}
                              disabled={
                                checked.length > 3 &&
                                checked.indexOf(item[1]) === -1
                              }
                            >
                              {item[0]}
                            </Checkbox>
                          </Col>
                        );
                      })}
                    </Row>
                  </div>
                );
              })
            : null}
        </Checkbox.Group>
        <Modal
          title="Predicted Yield"
          visible={this.props.showModal}
          onOk={this.handleOk}
          onCancel={this.props.hideModal}
          footer={[
            <Button
              key="submit"
              type="primary"
              loading={this.props.loading}
              onClick={this.handleOk}
            >
              Submit
            </Button>,
          ]}
        >
          <Table columns={columns} dataSource={this.props.modalData} />
          <p>Please ensure that you have at least one high yield in the selection below to make full use of our service, if not we will just suggest investing all in CPF Special Account by default</p>
        </Modal>
      </div>
    );
  }
}

export default step5;
