import React, { useEffect, useRef ,useState} from 'react';
import { Bar } from 'react-chartjs-2';
import { Chart } from 'chart.js/auto';


const AllUsersTotalPoint = ({tokenUsers}) => {
  const [AllUsersTotalPointData, setAllUsersTotalPointData] = useState(null);
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

 
  console.log('AllUsersTotalPoint-token:', tokenUsers,);
  
  useEffect(() => {
  const fetchAllUsersTotalPointData = async () => {
    try {
        if (tokenUsers!== null) {
        const response = await fetch(`http://localhost:8090/api/total_points_studs_for_all_teams?token=${tokenUsers}`);
        const result = await response.json();
        setAllUsersTotalPointData(result);
      }
    } catch (error) {
      console.error('AllUsersTotalPoint - Error fetching attendance data:', error);
    }
  };
  fetchAllUsersTotalPointData();
},[tokenUsers]);


if (!AllUsersTotalPointData) {
    return <div>Loading...</div>;
  }
  
    const data = {
      labels: AllUsersTotalPointData.map(item => item.team_name),
      datasets: [
        {
          label: 'Среднее посещение',
          data: AllUsersTotalPointData.map(item => item.avg_total_points),
          backgroundColor: 'rgb(177,185,253, 0.9)',
          borderColor: 'rgb(0,174,239)',
          borderWidth: 0,
          
  
        },
      ],
    };
  console.log('fetchAllUsersTotalPointData:', AllUsersTotalPointData);
  
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
          text: 'Баллы',
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
        text: 'Успеваемость ваших групп',
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
        borderRadius: 10, 
      },
    },
    animation: {
      duration: 2000,
    },
  };
  
  
    return <Bar ref={chartRef} data={data} options={options} />;
  };
  
export default AllUsersTotalPoint;