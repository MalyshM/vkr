import React, { useEffect, useRef ,useState} from 'react';
import { Bar } from 'react-chartjs-2';
import { Chart } from 'chart.js/auto';

const AllUsersAtenadance = ({tokenUsers}) => {
  const [AllUsersAtenadanceData, setAllUsersAtenadanceData] = useState(null);
  const chartRef = useRef(null);
  const [teachersUnic, setTeachers] = useState([]);


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

 
  console.log('AllUsersAtenadance-token:', tokenUsers,);
  
  useEffect(() => {
  const fetchAllUsersAtenadanceData = async () => {
    try {
        if (tokenUsers!== null) {
        const response = await fetch(`http://localhost:8090/api/attendance_static_stud_for_all_teams?token=${tokenUsers}`);
        const result = await response.json();
        setAllUsersAtenadanceData(result);

        const uniqueTeachers = [...new Set(result.map(item => item.teacher_name))];
        setTeachers(uniqueTeachers);

       
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
    'Самойлов Михаил Юрьевич': 'rgb(255, 0, 0, 0.9)',        // Красный
    'Павлова Елена Александровна': 'rgb(0, 255, 0, 0.9)',        // Зеленый
    'Плотоненко Юрий Анатольевич': 'rgb(0, 0, 255, 0.9)',        // Синий
    'Плотоненко Юрий Анатольевич, Подзолков Павел Николаевич': 'rgb(255, 255, 0, 0.9)',      // Желтый
    'Семихин Дмитрий Витальевич': 'rgb(255, 0, 255, 0.9)',      // Фиолетовый
    'Семихина Иветта Григорьевна, Черняев Александр Андреевич': 'rgb(0, 255, 255, 0.9)',      // Бирюзовый
    'Аврискин Михаил Владимирович': 'rgb(255, 128, 0, 0.9)',     // Оранжевый
    'Сальников Никита Владиславович': 'rgb(128, 0, 128, 0.9)',     // Пурпурный
    'Мельникова Антонина Владимировна': 'rgb(128, 128, 128, 0.9)',   // Серый
    'Трефилин Иван Андреевич': 'rgb(0, 128, 0, 0.9)',      // Темно-зеленый
    'Березовский Артем Константинович': 'rgb(0, 0, 128, 0.9)',      // Темно-синий
    'Дубровин Михаил Григорьевич': 'rgb(128, 0, 0, 0.9)',      // Темно-красный
    'Аврискин Михаил Владимирович, Подзолков Павел Николаевич': 'rgb(0, 128, 128, 0.9)',    // Темно-бирюзовый
  };

  const data = {
    labels: AllUsersAtenadanceData.map(item => item.teacher_name),
    datasets: [
      {
        label: 'Среднее посещение',
        data: AllUsersAtenadanceData.map(item => item.arrival),
        backgroundColor: AllUsersAtenadanceData.map(item => uniqueTeachersColors[item.teacher_name]),
        borderColor: 'rgb(0,174,239)',
        borderWidth: 0,
      },
    ],
  };
  

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
        text: 'Посещаемость ваших групп',
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
  console.log('fetchAllUsersAtenadanceData:', AllUsersAtenadanceData);
  
    return(<>

      <Bar ref={chartRef} data={data} options={options} />;


  </>) 
    
  };
export default AllUsersAtenadance;