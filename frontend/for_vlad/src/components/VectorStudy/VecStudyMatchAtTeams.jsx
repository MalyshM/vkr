import React, { useEffect, useRef ,useState} from 'react';
import { Bar } from 'react-chartjs-2';
import { Chart } from 'chart.js/auto';


const VecStudyMatchAtTeams = ({ speciality1, speciality2, token}) => {
  const [VecStudyMatchAtTeamsData, setVecStudyMatchAtTeamsData] = useState(null);
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

 
  console.log('team ID 1 in VecStudyMatchAtTeamsData:', speciality1, 'team ID 2 in VecStudyMatchAtTeamsData:', speciality1, 'token:', token);
  
  useEffect(() => {
  const fetchVecStudyMatchAtTeamsData = async () => {
    try {
        if (speciality1 !== null && speciality2 !== null) {
        const response = await fetch(`http://localhost:8090/api/attendance_static_for_specialities?speciality1=${speciality1}&speciality2=${speciality2}&token=${token}&lect=${false}`);
        const result = await response.json();
        setVecStudyMatchAtTeamsData(result);
      }
    } catch (error) {
      console.error('VecStudyMatchAtTeamsData - Error fetching attendance data:', error);
    }
  };
  fetchVecStudyMatchAtTeamsData();
},[speciality1,speciality2,token]);


if (!VecStudyMatchAtTeamsData) {
    return <div>Loading...</div>;
  }
  
  const colors = {
    [speciality1]: 'rgba(217,68,58, 0.5)', // Цвет для teamId1
    [speciality2]: 'rgba(177,185,253, 0.7)', // Цвет для teamId2
  };
  
    const data = {
      labels: VecStudyMatchAtTeamsData.map(item => `${item.speciality} - Студент: ${item.id}`),
      datasets: [
        {
          label: 'Процент посещения',
          data: VecStudyMatchAtTeamsData.map(item => item.arrival,),
          backgroundColor: VecStudyMatchAtTeamsData.map(item => colors[item.speciality]),
          borderColor: 'rgb(0,174,239)',
          borderWidth: 0,
        },
      ],
    };
  console.log('fetchVecStudyMatchAtTeamsData:', VecStudyMatchAtTeamsData);
  
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
          text: `Студенты направлений ${VecStudyMatchAtTeamsData[0]?.speciality || ''} и ${VecStudyMatchAtTeamsData[1]?.speciality || ''}`,
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
        text: `Посещаемость студентов направлений ${VecStudyMatchAtTeamsData[0]?.speciality || ''} и ${VecStudyMatchAtTeamsData[1]?.speciality || ''}`,
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
  
export default VecStudyMatchAtTeams;