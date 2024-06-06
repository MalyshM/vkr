import React, { useEffect, useRef, useState } from 'react';
import { Doughnut ,PolarArea,Pie} from 'react-chartjs-2';
import {  Tooltip, Typography, Row, Col, Layout } from 'antd';
import { QuestionCircleOutlined } from '@ant-design/icons';
import styled from 'styled-components';
import RequestCheckbox from '../ReportSystem/RequestCheckbox';

import { fetchWithTokenRefresh } from '../RefreshToken';

const { Content } = Layout;
const { Text, Title } = Typography;

const StataOfGroup = ({ teamId, teamName }) => {
  const [stataOfGroupData, setStataOfGroupData] = useState(null);
  const [requests, setRequests] = useState([]);

  useEffect(() => {
    const fetchSetStataOfGroupData = async () => {
      try {
        if (teamId !== null) {
          const response = await fetchWithTokenRefresh(`http://moais-dashboard.ru:8082/api/total_marks_for_team?id_team=${teamId}`);
          const result = await response.json();
          setStataOfGroupData(result);
        }
      } catch (error) {
        console.error('Error fetching fetch_stata_of_group_data data:', error);
      }
    };
    fetchSetStataOfGroupData();
  }, [teamId]);

  if (!stataOfGroupData) {
    return <div>Loading...</div>;
  }

  const requestUrl = `http://moais-dashboard.ru:8082/api/total_marks_for_team?id_team=${teamId}`;

  const handleUpdateRequests = (updatedRequests) => {
    setRequests(updatedRequests);
  };

  const getColorByMark = (mark) => {
    switch (mark) {
      case "неудовл.":
        return 'rgb(220,18,55)'
      case "удовл.":
        return '#FF8C00'; // Темно-оранжевый для оценки 3
      case "хор.":
        return '#FFD700'; // Золотой для оценки 4
      case "отл.":
        return '#32CD32'; // Зеленый для оценки 5
      default:
        return '#808080'; // Серый для неизвестных оценок
    }
  };

const markOrder = ['неудовл.', 'удовл.', 'хор.', 'отл.'];
stataOfGroupData.sort((a, b) => markOrder.indexOf(a.mark) - markOrder.indexOf(b.mark));


  const chartData = {
    labels: stataOfGroupData.map(item => item.mark),
    datasets: [
      {
        data: stataOfGroupData.map(item => item.percent),
        backgroundColor: stataOfGroupData.map(item => getColorByMark(item.mark)),

        borderWidth: 2,
        borderColor: '#ffffff', // Белые границы для контраста
        hoverBorderColor: '#000', // Черные границы при наведении
        hoverBorderWidth: 3,
      },
    ],
  };
console.log('stataOfGroupData',stataOfGroupData)
  const options = {
    responsive: true,
    plugins: {
      title: {
        display: true,
        text: `Оценки группы ${teamName}`,
        font: {
          size: 22,
          color: 'black',
          family: 'Trebuchet MS',
        },
      },
      datalabels: {
        display: true,
        anchor: 'center',
        align: 'center',
        color: 'black',
        font: {
          size: 20,
          weight: 'normal',
          family: 'Trebuchet MS',
        },
        formatter: (value, context) => {
          const roundedValue = (value * 100).toFixed(2);
          return `${roundedValue}%`;
        },
      },
      tooltip: {
        callbacks: {
          label: (context) => {
            const dataIndex = context.dataIndex;
            const avgTotalPoints = stataOfGroupData[dataIndex].avg_total_points.toFixed(2);
            return `Средний балл: ${avgTotalPoints}`;
          },
        },
      },
      legend: {
        display: true,
        position: 'bottom',
      },
    },
    maintainAspectRatio: false,
    layout: {
      padding: {},
    },
  };

  return (
    <Layout>
      <Content style={{ padding: '24px', background: '#fff', borderRadius: '20px',borderRadius: "20px", border: "1px solid lavender" 
 }}>
       
      <Row align="middle" gutter={16} justify={'center'}>

          <Col>
            <Tooltip title="Круговая диаграмма отображающая процентное количество студентов с определенной оценкой">
              <QuestionCircleOutlined />
            </Tooltip>
          </Col>
          
              <RequestCheckbox
                requestUrl={requestUrl}
                requestName="Оценки группы"
                onUpdateRequests={handleUpdateRequests}
              />
         

          </Row>

          <div style={{ width: '100%', height: '41vh' }}>
              <Doughnut data={chartData} options={options} />
              
          </div>

          

      </Content>
    </Layout>
  );
};

export default StataOfGroup;
