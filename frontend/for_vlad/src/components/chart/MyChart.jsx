import React, { useEffect, useRef ,useState} from 'react';
import { Bar } from 'react-chartjs-2';
import { Chart } from 'chart.js/auto';
import { useNavigate  } from 'react-router-dom';


const MyChart = ({ teamId}) => {
  const navigate = useNavigate ();
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

  const handleChartClick = (_, elements) => {
    if (elements && elements.length > 0) {
      const clickedElement = elements[0];
      const dataIndex = clickedElement.index;
      const studentId = sortedData[dataIndex]?.id;
      navigate (`/student/${studentId}/${teamId}`);
    }
  };

  // console.log('selectedTeam changed:', selectedTeam);
  console.log('team ID in MyChart (new realization):', teamId);
  
  useEffect(() => {
  const fetchAttendanceData = async () => {
    try {
      if (teamId !== null) {
        const response = await fetch(`http://localhost:8090/api/attendance_per_stud_for_team?id_team=${teamId}`);
        const result = await response.json();
        // Обновляем состояние с полученными данными
        setAttendanceData(result);
      }
    } catch (error) {
      console.error('Error fetching attendance data:', error);
    }
  };
  fetchAttendanceData();
},[teamId]);

if (!attendanceData) {
  return <div>Loading...</div>;
}


  const sortedData = [...attendanceData].sort((a, b) => b.Посещаемость - a.Посещаемость);

  const sortedData_map= sortedData.map(item => parseFloat(item.Посещаемость.toFixed(3)));

  const data = {
    labels: sortedData.map(item => item.id),
    datasets: [
      {
        label: 'Посещение',
        data: sortedData_map,
        backgroundColor: 'rgba(75, 192, 192, 0.2)',
        borderColor: 'rgb(0,174,239)',
        borderWidth: 3,
        

      },
    ],
  };
console.log('Data for chart:', data);

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
      text: 'Поcещаемость дисциплины ПиОА студентами выбранной подгруппы',
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

export default MyChart;

