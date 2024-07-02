import React, { useEffect, useRef, useState } from 'react';
import { Bar } from 'react-chartjs-2';
import { useNavigate } from 'react-router-dom';
import { Layout, Tooltip, Typography, Row, Col, Space, Avatar } from 'antd';
import { QuestionCircleOutlined } from '@ant-design/icons';
import styled from 'styled-components';
import RequestCheckbox from '../ReportSystem/RequestCheckbox';
import { fetchWithTokenRefresh } from '../RefreshToken';

const { Content } = Layout;
const { Title, Text } = Typography;

const NumCountStudInLern = ({ teamId, onLessonSelect, numberOfItems }) => {
  const chartRef = useRef(null);
  const [AtendanceNumCountStudInLernData, setAtendanceNumCountStudInLernData] = useState(null);
  const [selectedLesson, setSelectedLesson] = useState(null);
  const [numberOfday, setNumberOfday] = useState(null);
  const [requests, setRequests] = useState([]);
  const [selectedIndex, setSelectedIndex] = useState(null); 


  // const handleBarClick = (_, elements) => {
  //   if (elements && elements.length > 0) {
  //     const clickedElement = elements[0];
  //     const dataIndex = clickedElement.index;
  //     const selectedLessonName = AtendanceNumCountStudInLernData[dataIndex].name;
  //     setSelectedLesson(selectedLessonName);
  //     onLessonSelect(selectedLessonName);
  //   }
  // };

  const handleBarClick = (_, elements) => {
    if (elements && elements.length > 0) {
      const clickedElement = elements[0];
      const dataIndex = clickedElement.index;
      const selectedLessonName = AtendanceNumCountStudInLernData[dataIndex].name;
      setSelectedLesson(selectedLessonName);
      setSelectedIndex(dataIndex); // Сохранение выбранного индекса
      onLessonSelect(selectedLessonName, dataIndex); // Передача индекса в onLessonSelect
    }
  };


  useEffect(() => {
    const fetchAtendanceNumCountStudInLernData = async () => {
      try {
        if (teamId !== null) {
          const response = await fetchWithTokenRefresh(`http://moais-dashboard.ru:8082/api/attendance_num_for_stud_for_team?id_team=${teamId}`);
          const result = await response.json();
          setAtendanceNumCountStudInLernData(result);
          setNumberOfday(result.length);
        }
      } catch (error) {
        console.error('Error fetching attendanceTotalPoints data:', error);
      }
    };
    fetchAtendanceNumCountStudInLernData();
  }, [teamId]);

  const requestUrl = `http://moais-dashboard.ru:8082/api/attendance_num_for_stud_for_team?id_team=${teamId}`;

  const handleUpdateRequests = (updatedRequests) => {
    setRequests(updatedRequests);
  };

  if (!AtendanceNumCountStudInLernData) {
    return <div>Loading...</div>;
  }

  const data = {
    labels: AtendanceNumCountStudInLernData.map((item, index) => {
      const nameWithoutLastTwoChars = item.name.slice(0, -2);
      return `${index + 1}. ${nameWithoutLastTwoChars}`;
    }),
    datasets: [
      {
        label: 'Количество студентов',
        data: AtendanceNumCountStudInLernData.map((item) => item.Посещаемость),
        backgroundColor: 'rgba(49, 141, 159, 0.8)',
        borderColor: 'rgba(49, 141, 159, 1)',
        borderWidth: 2,
        type: 'line',
        tension: 0.4,
        pointBackgroundColor: 'rgba(49, 141, 159, 1)',
        pointBorderColor: '#fff',
        pointBorderWidth: 2,
        pointRadius: 5,
        hoverBackgroundColor: 'rgba(49, 141, 159, 0.9)',
        hoverBorderColor: 'rgba(49, 141, 159, 1)',
      },
    ],
  };
  
  const options = {
    onClick: handleBarClick,
    scales: {
      x: {
        ticks: {
          callback: (value, index) => (index + 1).toString(),
          font: {
            size: 14,
            family: 'Trebuchet MS',
          },
          color: '#666',
        },
        type: 'category',
        position: 'bottom',
        title: {
          display: true,
          text: 'Учебная встреча',
          font: {
            size: 20,
            family: 'Trebuchet MS',
          },
          color: '#666',
        },
        grid: {
          display: false,
        },
      },
      y: {
        type: 'linear',
        position: 'left',
        title: {
          display: true,
          text: 'Количество студентов',
          font: {
            size: 20,
            family: 'Trebuchet MS',
          },
          color: '#666',
        },
        id: 'y-axis-0',
        ticks: {
          callback: (value) => value.toString(),
          font: {
            size: 14,
            family: 'Trebuchet MS',
          },
          color: '#666',
        },
        grid: {
          color: 'rgba(200, 200, 200, 0.3)',
        },
      },
    },
    plugins: {
      datalabels: {
        display: true,
        anchor: 'start',
        align: 'start',
        color: '#000',
        formatter: (value, context) => `${value}`,
        font: {
          size: 12,
          family: 'Trebuchet MS',
        },
      },
      title: {
        display: true,
        text: 'Количество студентов на учебной встрече',
        font: {
          size: 22,
          family: 'Trebuchet MS',
        },
        color: '#333',
      },
      legend: {
        display: true,
        position: 'bottom',
        labels: {
          font: {
            size: 14,
            family: 'Trebuchet MS',
          },
          color: '#333',
          padding: 20,
        },
      },
    },
    maintainAspectRatio: false,
    layout: {
      padding: {
      },
    },
    elements: {
      line: {
        borderWidth: 2,
        borderColor: 'rgba(49, 141, 159, 1)',
        backgroundColor: 'rgba(49, 141, 159, 0.8)',
        fill: false,
      },
      point: {
        radius: 5,
        backgroundColor: 'rgba(49, 141, 159, 1)',
        borderColor: '#fff',
        borderWidth: 2,
        hoverRadius: 7,
        hoverBorderWidth: 3,
      },
    },
    animation: {
      duration: 1500,
      easing: 'easeOutBounce',
    },
  };
  

  return (
    <Layout>
      <Content style={{ padding: '24px', background: '#fff', borderRadius: '20px',borderRadius: "20px", border: "1px solid lavender" 
 }}>

        <Row align="middle" gutter={16} justify="center">
          <Col>
            <Tooltip title="График отображающий количество студентов на каждой учебной встрече во время прохождения курса">
              <QuestionCircleOutlined />
            </Tooltip>
          </Col>
          
          <RequestCheckbox
            requestUrl={requestUrl}
            requestName="Количество студентов на встрече"
            onUpdateRequests={handleUpdateRequests}
          />
        </Row>

          <div style={{ width: '100%', height: '27vh' }}>
            <Bar  ref={chartRef} data={data} options={options} />
          </div>

      </Content>
    </Layout>
    
  );
};

export default NumCountStudInLern;
