import React, { useEffect, useRef ,useState} from 'react';
import { Bar } from 'react-chartjs-2';
import { Chart } from 'chart.js/auto';


const AllUsersTotalPoint = ({tokenUsers}) => {
  const [AllUsersTotalPointData, setAllUsersTotalPointData] = useState(null);
  const [NumberOfGr, setNumberOfGr] = useState(null);

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

        setNumberOfGr(result.length);
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

  const uniqueTeachersColors = {
    'Самойлов Михаил Юрьевич': 'rgb(255, 0, 0, 0.5)',        // Красный
    'Павлова Елена Александровна': 'rgb(0, 255, 0, 0.5)',        // Зеленый
    'Плотоненко Юрий Анатольевич': 'rgb(0, 0, 255, 0.5)',        // Синий
    'Плотоненко Юрий Анатольевич, Подзолков Павел Николаевич': 'rgb(255, 255, 0, 0.5)',      // Желтый
    'Семихин Дмитрий Витальевич': 'rgb(255, 0, 255, 0.5)',      // Фиолетовый
    'Семихина Иветта Григорьевна, Черняев Александр Андреевич': 'rgb(0, 255, 255, 0.5)',      // Бирюзовый
    'Аврискин Михаил Владимирович': 'rgb(255, 128, 0, 0.5)',     // Оранжевый
    'Сальников Никита Владиславович': 'rgb(128, 0, 128, 0.5)',     // Пурпурный
    'Мельникова Антонина Владимировна': 'rgb(128, 128, 128, 0.5)',   // Серый
    'Трефилин Иван Андреевич': 'rgb(0, 128, 0, 0.5)',      // Темно-зеленый
    'Березовский Артем Константинович': 'rgb(0, 0, 128, 0.5)',      // Темно-синий
    'Дубровин Михаил Григорьевич': 'rgb(128, 0, 0, 0.5)',      // Темно-красный
    'Аврискин Михаил Владимирович, Подзолков Павел Николаевич': 'rgb(0, 128, 128, 0.5)',    // Темно-бирюзовый
  };

  const sortedData = AllUsersTotalPointData.sort((a, b) => b.avg_total_points - a.avg_total_points);

  
    const data = {
      labels: sortedData.map(item => `${item.team_name} (${item.teacher_name})`),
      datasets: [
        {
          label: 'Средняя усепваемость',
          data: sortedData.map(item => item.avg_total_points),
          backgroundColor: sortedData.map(item => uniqueTeachersColors[item.teacher_name]),
          borderColor: 'rgb(0,174,239)',
          borderWidth: 0,
          },
      ],
    };

  console.log('fetchAllUsersTotalPointData:', AllUsersTotalPointData);
  
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
          text: 'Все группы',
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
      datalabels: {
        display: true,
        anchor: 'end',
        align: 'end',
        color: 'black', // Цвет текста
        formatter: (value, context) => {
          return `${sortedData[context.dataIndex].avg_total_points.toFixed(0)} Б`;

        },
      },
      title: {
        display: true,
        text: `Успеваемость ваших групп, кол-во: ${NumberOfGr}`,
        font: {
          size: 22,
          fontColor: 'black',
          family: 'Trebuchet MS'
        },
      },
  
      legend: {
        display: false,
        position: 'right',
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