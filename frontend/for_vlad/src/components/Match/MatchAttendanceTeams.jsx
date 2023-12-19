import React, { useEffect, useRef ,useState} from 'react';
import { Bar } from 'react-chartjs-2';
import { Chart } from 'chart.js/auto';


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
        const response = await fetch(`http://localhost:8090/api/attendance_static_stud_for_teams?id_team1=${teamId1}&id_team2=${teamId2}`);
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
  
    const data = {
      labels: attendanceData.map(item => item.team_name),
      datasets: [
        {
          label: 'Среднее посещение',
          data: attendanceData.map(item => item.arrival_avg),
          backgroundColor: 'rgba(75, 192, 192, 0.2)',
          borderColor: 'rgb(0,174,239)',
          borderWidth: 3,
          
  
        },
      ],
    };
  console.log('fetchMetchAttendanceData:', attendanceData);
  
  const options = {
    
    scales: {
      x: {
        type: 'category',
        position: 'bottom',
        title: {
          display: false,
          text: 'Идентификатор студента',
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
          text: 'Посещаемость',
          font: {
            size: 20, // Размер шрифта названия оси X
            fontColor: 'black',
            family: 'Trebuchet MS'
          },
        },
      },
    },
    plugins: {
      title: {
        display: true,
        text: 'Средняя поcещаемость дисциплины ПиОА студентами выбранных подгрупп',
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
        borderRadius: 10, 
      },
    },
    animation: {
      duration: 2000,
    },
  };
  
  
    return <Bar ref={chartRef} data={data} options={options} />;
  };
  
export default MatchAttendanceTeams;