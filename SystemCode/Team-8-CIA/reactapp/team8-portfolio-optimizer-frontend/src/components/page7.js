import React, { Component } from "react";
import { Radio, Input, Popconfirm, Button, message, Space } from "antd";
import { Select } from "antd";
import { Checkbox, Row, Col } from "antd";
import _ from "lodash";



import { Table, Tag, Typography } from "antd";

const { Text } = Typography;



function confirm() {
  message.info('Feature coming soon!');
}

const { Option } = Select;
const columns = [
  {
    title: "No.",
    dataIndex: "index",
    key: "index",
  },
  {
    title: "Name",
    dataIndex: "name",
    key: "name",
  },
  {
    title: "Price",
    dataIndex: "price",
    key: "price",
  },
  {
    title: 'Purchase',
    key: 'purchase',
    render: () => (
      <>
      <Popconfirm 
      placement="rightTop"
      title="investment"
      onConfirm={confirm}
      okText="Yes"
      cancelText="No"
      >
      <Button>Invest</Button>
      </Popconfirm>
      </>
    ),
  },
];

class step5 extends Component {
  state = {
    tableData: [],
    ans: [],
    isMax: false,
    checked: [],
  };
  componentDidMount() {}

  render() {
    const { data } = this.props;
    const { tableData } = this.state;
    if (this.props.currentStep !== 6) {
      return null;
    }
    let newData = [];
    // console.log(data, "page 7 data");
    if (!_.isEmpty(data) && _.isEmpty(tableData)) {
      let count = 1;
      data.stock_allocation.map((item) => {
        newData.push({
          index: count++,
          name: item[0],
          price: item[1],
        });
      });
      this.setState({ tableData: newData });
    }

    return (
      <div>
        <label>
          Based on your inputs, your risk profile is: <Text type="warning">{data.risk_profile}</Text>. 
          You will have to keep a minimum of $20,000 in your CPF OA account, taking that into account, maximum investible account is <Text type="warning">${data.CPFOA}</Text>
        </label>
        {/* <label>You have selected your preferred stocks of:</label> */}
        <label>
          We recommend you to invest a total of as an investment portfolio
          outlined below:
        </label>
        <Table columns={columns} dataSource={tableData}/>
        <label>
          The expected return of this portfolio is <Text type="warning">{data.best_return}</Text>, with a risk of <Text type="warning">{data.optimal_risk}</Text>, which is well within your risk appetite of <Text type="warning">{data.rules_risk}</Text> that is calculated according to your risk profile."
        </label>
      </div>
    );
  }
}

export default step5;
