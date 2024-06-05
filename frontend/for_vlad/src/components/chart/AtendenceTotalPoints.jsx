import React, { useEffect, useRef, useState } from 'react';
import { Bar } from 'react-chartjs-2';
import { useNavigate } from 'react-router-dom';
import { Button, Typography, Tooltip, Row, Col, Layout, Space } from 'antd';
import { QuestionCircleOutlined } from '@ant-design/icons';

import { useNumberItems } from './NumberItemsContext';
import RequestCheckbox from '../ReportSystem/RequestCheckbox';

import { fetchWithTokenRefresh } from '../RefreshToken';

import 'chartjs-plugin-trendline';

const { Content } = Layout;
const { Title, Text } = Typography;

const AtendenceTotalPoints = ({ teamId, teamName }) => {
  const [requests, setRequests] = useState([]);

  const navigate = useNavigate();
  const [attendanceTotalPointsData, setAttendanceTotalPointsData] = useState(null);
  const chartRef = useRef(null);
  const [sortBy, setSortBy] = useState('Успеваемость');

  const [totalPointsAvg, setTotalPointsAvg] = useState(null);
  const [arrivalAvg, setArrivalAvg] = useState(null);

  const [successColor, setSuccessColor] = useState('rgba(22,119,255, 1)');
  const [attendanceColor, setAttendanceColor] = useState('rgb(206,206,206, 0.8)');

  const [numberOfItems, setNumberOfItems] = useState(null);
  const [yAxisTitle, setYAxisTitle] = useState('Баллы');

  const handleButtonClick = (sortType) => {
    setSortBy(sortType);

    if (sortType === 'Успеваемость') {
      setYAxisTitle('Баллы');
    } else if (sortType === 'Посещаемость') {
      setYAxisTitle('Процент посещения');
    }

    if (sortType === 'Успеваемость') {
      setSuccessColor('rgba(22,119,255, 1)');

      setAttendanceColor('rgb(206,206,206, 0.8)');
    } else {
      setSuccessColor('rgb(206,206,206, 0.8)');
      setAttendanceColor('rgba(22,119,255, 1)');
    }
  };

  const handleChartClick = (_, elements) => {
    if (elements && elements.length > 0) {
      const clickedElement = elements[0];
      const dataIndex = clickedElement.index;
      const studentId = attendanceTotalPointsData[dataIndex]?.stud_id;
      navigate(`/student/${studentId}`);
    }
  };

  useEffect(() => {
    const fetchAtendanceTotalPointsData = async () => {
      try {
        if (teamId !== null) {
          const response = await fetchWithTokenRefresh(`http://moais-dashboard.ru:8082/api/total_points_attendance_per_stud_for_team?id_team=${teamId}`);
          const result = await response.json();

          console.log('Total_points_attendance_per_stud_for_team:', result);

          const sortedDataArray = result.sort((a, b) =>
            sortBy === 'Посещаемость' ? b.Посещаемость - a.Посещаемость : b.Успеваемость - a.Успеваемость
          );

          setAttendanceTotalPointsData(sortedDataArray);
          setNumberOfItems(sortedDataArray.length);

          const firstStudentAtendence = sortedDataArray[0];
          const averageAttendance = firstStudentAtendence.Посещаемость_средняя;
          setArrivalAvg(averageAttendance);

          const firstStudentTotalPoints = sortedDataArray[0];
          const averageTotalPoints = firstStudentTotalPoints.Успеваемость_средняя;
          setTotalPointsAvg(averageTotalPoints);
        }
      } catch (error) {
        console.error('Error fetching attendanceTotalPoints data:', error);
      }
    };
    fetchAtendanceTotalPointsData();
  }, [teamId, sortBy]);

  if (!attendanceTotalPointsData) {
    return <div>Loading...</div>;
  }

  const data = {
    labels: attendanceTotalPointsData.map(item => item.stud_id),
    datasets: [
      {
        label: 'Успеваемость',
        data: attendanceTotalPointsData.map(item => item.Успеваемость),
        backgroundColor: successColor,
        borderWidth: 1,
        borderColor: '#fff',
        hoverBorderColor: '#000',
        hoverBorderWidth: 2,
      },
      {
        label: 'Посещаемость %',
        data: attendanceTotalPointsData.map(item => Math.round(item.Посещаемость)),
        backgroundColor: attendanceColor,
        borderWidth: 1,
        borderColor: '#fff',
        hoverBorderColor: '#000',
        hoverBorderWidth: 2,
      },
      {
        label: 'Медиана поещаемости',
        data: Array(attendanceTotalPointsData.length).fill(totalPointsAvg.toFixed(2)),
        borderColor: 'rgba(0, 28, 172, 1)',
        borderWidth: 3,
        fill: false,
        type: 'line',
        pointRadius: 0,
      },
      {
        label: 'Медиана Успеваемости',
        data: Array(attendanceTotalPointsData.length).fill(Math.round(arrivalAvg)),
        borderColor: 'rgb(255,100,50)',
        borderWidth: 3,
        fill: false,
        type: 'line',
        pointRadius: 0,
      },
    ],
  };
  
  const options = {
    onClick: handleChartClick,
    scales: {
      x: {
        type: 'category',
        position: 'bottom',
        title: {
          display: true,
          text: 'Идентификатор студента',
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
          text: yAxisTitle,
          font: {
            size: 20,
            family: 'Trebuchet MS',
          },
          color: '#666',
        },
        grid: {
          color: 'rgba(200, 200, 200, 0.3)',
        },
        id: 'y-axis-0',
      },
    },
    plugins: {
      datalabels: {
        display: false,
        anchor: 'end',
        align: 'end',
        color: '#000',
        formatter: (value, context) => `${value}%`,
      },
      title: {
        display: true,
        text: `Посещаемость и успеваемость студентов группы ${teamName}, кол-во студентов: ${numberOfItems}`,
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
          // padding: 20,
        },
      },
    },
    maintainAspectRatio: false,
    layout: {
      padding: {
        // left: 20,
        // right: 20,
        // top: 20,
        // bottom: 20,
      },
    },
    elements: {
      bar: {
        borderWidth: 2,
        borderRadius: 10,
      },
    },
    animation: {
      duration: 1500,
      easing: 'easeOutBounce',
    },
  };
  

  const requestUrl = `http://moais-dashboard.ru:8082/api/total_points_attendance_per_stud_for_team?id_team=${teamId}`;

  const handleUpdateRequests = (updatedRequests) => {
    setRequests(updatedRequests);
  };

  return (
    <Layout>
      <Content style={{ padding: '24px', background: '#fff', borderRadius: '20px',borderRadius: "20px", border: "1px solid lavender" 
 }}>
        <Row align="middle" gutter={16} justify={'center'}>

        <Col>
            <Tooltip title="Диаграмма отображающая баллы и процент посещаемости каждого студента в выбранной группе">
              <QuestionCircleOutlined />
            </Tooltip>
          </Col>

          <Col>
            <Text>Режим сортировки:</Text>
          </Col>

          <Col>
            <Button
              type={sortBy === 'Успеваемость' ? 'primary' : 'default'}
              onClick={() => handleButtonClick('Успеваемость')}
            >
              Успеваемость
            </Button>
          </Col>

          <Col>
            <Button
              type={sortBy === 'Посещаемость' ? 'primary' : 'default'}
              onClick={() => handleButtonClick('Посещаемость')}
            >
              Посещаемость
            </Button>
          </Col>


          <RequestCheckbox
            requestUrl={requestUrl}
            requestName="Посещаемсть и успеваемость"
            onUpdateRequests={handleUpdateRequests}
          />

        </Row>
          
          <div style={{ width: '100%', height:'40vh'}}>
            <Bar ref={chartRef} data={data} options={options} />
          </div>

      </Content>
    </Layout>
  );
};


export default AtendenceTotalPoints;
