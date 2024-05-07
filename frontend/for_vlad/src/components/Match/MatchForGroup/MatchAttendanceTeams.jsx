import React, { useEffect, useRef ,useState} from 'react';
import { Bar } from 'react-chartjs-2';
import { Chart } from 'chart.js/auto';
import { fetchWithTokenRefresh } from '../../RefreshToken';

const MatchAttendanceTeams = ({ teamId1, teamId2}) => {
  const [attendanceData, setAttendanceData] = useState(null);
  const chartRef = useRef(null);

  useEffect(() => {
    if (chartRef.current) {
      // Уничтожаем чарт при размонтировании компонента
      return () => {
        if (chartRef.current) {
          const chartInstance = Chart.getChart(chartRef.current); // Получаем экземпляр чарта
          if (chartInstance) {
            chartInstance.destroy(); // Уничтожаем чарт
          }
        }
      };
    }
  }, []);

 
  console.log('team ID 1 in MatchAttendanceTeams:', teamId1, 'team ID 2 in MatchAttendanceTeams:', teamId2);
  
  useEffect(() => {
  const fetchMetchAttendanceData = async () => {
    try {
        if (teamId1 !== null && teamId2 !== null) {
        const response = await fetchWithTokenRefresh(`http://moais-dashboard.ru:8082/api/attendance_static_stud_for_teams?id_team1=${teamId1}&id_team2=${teamId2}`);
        const result = await response.json();
        setAttendanceData(result);
      }
    } catch (error) {
      console.error('MatchAttendanceTeams - Error fetching attendance data:', error);
    }
  };
  fetchMetchAttendanceData();
},[teamId1,teamId2]);


if (!attendanceData) {
    return <div>Loading...</div>;
  }
  
  const colors = {
    [teamId1]: 'rgba(217,68,58, 0.5)', // Цвет для teamId1
    [teamId2]: 'rgba(177,185,253, 0.7)', // Цвет для teamId2
  };
  
    const data = {
      labels: attendanceData.map(item => `${item.id} (${item.team_name})`),
      datasets: [
        {
          label: 'Процент посещения',
          data: attendanceData.map(item => item.arrival * 100,),
          backgroundColor: attendanceData.map(item => colors[item.team_id]),
          borderColor: 'rgb(0,174,239)',
          borderWidth: 0,
        },
      ],
    };
  console.log('fetchMetchAttendanceData:', attendanceData);
  
  const options = {
    
    scales: {
      x: {
        ticks: {
          display: false,
        },
        type: 'category',
        position: 'bottom',
        title: {
          display: true,
          text: `Студенты групп ${attendanceData[0]?.team_name || ''} и ${attendanceData[1]?.team_name || ''}`,
          font: {
            size: 20, // Размер шрифта названия оси X
            fontColor: 'black',
            family: 'Trebuchet MS'
          },
        },
      },
      y: {
        type: 'linear', // изменение типа шкалы на категорию
        position: 'left',
        title: {
          display: true,
          text: 'Процент посещаемости',
          font: {
            size: 20, // Размер шрифта названия оси X
            fontColor: 'black',
            family: 'Trebuchet MS'
          },
        },
      },
    },
    plugins: {
      datalabels: {
        display: true,
          anchor: 'end',
          align: 'end',
          color: 'black',
          // font: {
          //   size: 10, 
          // },
          formatter: (value, context) => {
            const roundedValue = (value).toFixed(0);
            return `${roundedValue}%`;
          },
        },

      title: {
        display: true,
        text: `Посещаемость студентов групп ${attendanceData[0]?.team_name || ''} и ${attendanceData[1]?.team_name || ''}`,
        font: {
          size: 22,
          fontColor: 'black',
          family: 'Trebuchet MS'
        },
      },
  
      legend: {
        display: false,
        position: 'top',
      },
    },
    maintainAspectRatio: false,
    layout: {
      padding: {
        left: 50,
        right: 50,
        top: 0,
        bottom: 0,
      },
    },
    elements: {
      
      bar: {
        barThickness: 400,
        borderRadius: 5, 
      },
    },
    animation: {
      duration: 2000,
    },
  };
  
  
    return <Bar ref={chartRef} data={data} options={options} />;
  };
  
export default MatchAttendanceTeams;