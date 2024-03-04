import React, { useEffect, useRef ,useState} from 'react';
import { Bar } from 'react-chartjs-2';
import { Chart } from 'chart.js/auto';
import 'chartjs-plugin-datalabels'; // Импортируйте плагин

const VecStudyAllUsersTP = ({tokenUsers}) => {
  const [VecStudyAllUsersTPData, setVecStudyAllUsersTPData] = useState(null);
  const chartRef = useRef(null);
  const [count, setCount] = useState(null); // Новый стейт для данных о командах


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

 
  console.log('VecStudyAllUsersTP-token:', tokenUsers,);
  
  useEffect(() => {
  const fetchVecStudyAllUsersTPData = async () => {
    try {
        if (tokenUsers!== null) {
        const response = await fetch(`http://localhost:8090/api/total_points_studs_for_all_specialities?token=${tokenUsers}&lect=${false}`);
        const result = await response.json();
        setVecStudyAllUsersTPData(result);  
        setCount(result.length);
      }
    } catch (error) {
      console.error('VecStudyAllUsersAt - Error fetching attendance data:', error);
    }
  };
  fetchVecStudyAllUsersTPData();
},[tokenUsers]);


if (!VecStudyAllUsersTPData) {
    return <div>Loading...</div>;
  }


  const uniqueTeachersColors = {
    '01.03.01 Математика': 'rgb(255, 0, 0, 0.5)',        
    '01.03.03 Механика и математическое моделирование': 'rgb(0, 255, 0, 0.5)',
    '02.03.03 Математическое обеспечение и администрирование информационных систем': 'rgb(0, 0, 255, 0.5)',
    '03.03.02 Физика': 'rgb(255, 255, 0, 0.5)',
    '04.03.01 Химия': 'rgb(255, 0, 255, 0.5)',
    '05.03.02 География': 'rgb(0, 255, 255, 0.5)',
    '05.03.03 Картография и геоинформатика': 'rgb(255, 128, 0, 0.5)',
    '05.03.06 Экология и природопользование': 'rgb(128, 0, 128, 0.5)',
    '06.03.01 Биология': 'rgb(128, 128, 128, 0.5)',
    '06.05.01 Биоинженерия и биоинформатика': 'rgb(0, 128, 0, 0.5)',
    '09.03.02 Информационные системы и технологии': 'rgb(0, 0, 128, 0.5)',
    '09.03.03 Прикладная информатика': 'rgb(128, 0, 0, 0.5)',
    '10.03.01 Информационная безопасность': 'rgb(0, 128, 128, 0.5)',
    '10.05.01 Компьютерная безопасность': 'rgb(128, 128, 0, 0.5)',
    '10.05.03 Информационная безопасность автоматизированных систем': 'rgb(255, 0, 0, 0.5)',
    '15.03.06 Мехатроника и робототехника': 'rgb(0, 255, 0, 0.5)',
    '16.03.01 Техническая физика': 'rgb(0, 0, 255, 0.5)',
    '35.03.10 Ландшафтная архитектура': 'rgb(255, 255, 0, 0.5)',
    '38.03.01 Экономика': 'rgb(255, 0, 255, 0.5)',
    '38.03.02 Менеджмент': 'rgb(255, 128, 0, 0.5)',
    '38.05.01 Экономическая безопасность': 'rgb(128, 0, 128, 0.5)',
    '42.03.05 Медиакоммуникации': 'rgb(128, 128, 128, 0.5)',
    '43.03.02 Туризм': 'rgb(0, 128, 0, 0.5)',
    '44.03.05 Педагогическое образование (с двумя профилями подготовки)': 'rgb(0, 0, 128, 0.5)',
    '49.03.01 Физическая культура': 'rgb(255, 0, 0, 0.5)',
    'NaN': 'rgb(255, 128, 128, 0.5)',
  };

  const sortedData = VecStudyAllUsersTPData.sort((a, b) => b.avg_total_points - a.avg_total_points);

  const data = {
    labels: sortedData.map(item => `${item.Stud_speciality} - кол-во студентов: ${item.studs_in_speciality}`),
    datasets: [
      {
        label: 'Баллы',
        data: sortedData.map(item => item.avg_total_points),
        backgroundColor: sortedData.map(item => uniqueTeachersColors[item.Stud_speciality]),
        borderColor: 'rgb(0,174,239)',
        borderWidth: 0,
      },
    ],
  };
  
  const options = {
    
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
          text: 'Все направления, которые обучаеются ПиОА',
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
        font: {
          weight: "normal",
        },
        anchor: 'end',
        align: 'end',
        color: 'black', // Цвет текста
        formatter: (value, context) => {
          return `${sortedData[context.dataIndex].avg_total_points.toFixed(0)} Б\nкол-во:${sortedData[context.dataIndex].studs_in_speciality}`;
        },
      },


    title: {
        display: true,
                text: `Успеваемость ваших направлений, кол-во: ${count}`,
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
    // interaction: {
    //   mode: 'index',
    //   intersect: false,
    // },
  
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
  console.log('fetchVecStudyAllUsersTPData:', VecStudyAllUsersTPData);
  
    return(<>

      <Bar ref={chartRef} data={data} options={options} />;
  </>) 
    
  };
export default VecStudyAllUsersTP;