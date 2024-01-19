import React, { useEffect, useRef ,useState} from 'react';
import { Bar } from 'react-chartjs-2';
import { Chart } from 'chart.js/auto';
import 'chartjs-plugin-datalabels'; // Импортируйте плагин
import { useNavigate  } from 'react-router-dom';

const AllUsersAtenadance = ({tokenUsers,teamId,teamName}) => {
  const [AllUsersAtenadanceData, setAllUsersAtenadanceData] = useState(null);
  const chartRef = useRef(null);
  const [NumberOfGr, setNumberOfGr] = useState(null);
  const navigate = useNavigate ();

  

  useEffect(() => {
    if (chartRef.current) {
      // Сохраняем значение в переменную
      const currentChartRef = chartRef.current;
  
      // Уничтожаем чарт при размонтировании компонента
      return () => {
        if (currentChartRef) {
          const chartInstance = Chart.getChart(currentChartRef); // Получаем экземпляр чарта
          if (chartInstance) {
            chartInstance.destroy(); // Уничтожаем чарт
          }
        }
      };
    }
  }, []);

  // const handleTeleportGroup = (_, elements) => {
  //   if (elements && elements.length > 0) {
  //     const clickedElement = elements[0];
  //     const dataIndex = clickedElement.index;
  //     const teamName  = sortedData[dataIndex]?.team_name;
  //     navigate (`/main/${teamName}`);
  //   }
  // };
 
  console.log('AllUsersAtenadance-token:', tokenUsers,);
  
  useEffect(() => {
  const fetchAllUsersAtenadanceData = async () => {
    try {
        if (tokenUsers!== null) {
        const response = await fetch(`http://localhost:8090/api/attendance_static_stud_for_all_teams?token=${tokenUsers}`);
        const result = await response.json();
        setAllUsersAtenadanceData(result);  
        
        setNumberOfGr(result.length)
      }
    } catch (error) {
      console.error('AllUsersAtenadance - Error fetching attendance data:', error);
    }
  };
  fetchAllUsersAtenadanceData();
},[tokenUsers]);


if (!AllUsersAtenadanceData) {
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

  const sortedData = AllUsersAtenadanceData.sort((a, b) => b.arrival - a.arrival);


  const data = {
    labels: sortedData.map(item => `${item.team_name} (${item.teacher_name})`),
    datasets: [
      {
        label: 'Среднее посещение',
        data: sortedData.map(item => item.arrival),
        backgroundColor: sortedData.map(item => uniqueTeachersColors[item.teacher_name]),
        borderColor: 'rgb(0,174,239)',
        borderWidth: 0,
      },
    ],
  };
  
  const options = {
    // onClick: handleTeleportGroup,
    scales: {
      x: {
        stacked: true, 
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
        color: 'black', // Цвет текста
        formatter: (value, context) => {
          return `${sortedData[context.dataIndex].arrival.toFixed(0)}%`;


        },
      },


    title: {
        display: true,
        text: `Посещаемость ваших групп, кол-во: ${NumberOfGr}`,
        font: {
          size: 22,
          fontColor: 'black',
          family: 'Trebuchet MS'
        },
      },
  
      legend: {
        display: false,
        position: 'right'
        
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
  console.log('fetchAllUsersAtenadanceData:', AllUsersAtenadanceData);
  
    return(<>

      <Bar ref={chartRef} data={data} options={options} />;
  </>) 
    
  };
export default AllUsersAtenadance;