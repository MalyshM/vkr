import React, { useEffect, useRef ,useState} from 'react';
import { Bar } from 'react-chartjs-2';
import { Chart } from 'chart.js/auto';
import 'chartjs-plugin-datalabels'; // Импортируйте плагин
import { useNavigate  } from 'react-router-dom';
import { Text } from '@chakra-ui/react'
import { Legend } from 'react-chartjs-2';

import { fetchWithTokenRefresh } from '../../RefreshToken';


const VecStudyAllusersAtTp = ({tokenUsers, choiseGroupSpeciality, selectedTeachers, selectedSpeciality}) => {
  const [VecStudyAllusersAtTpData, setVecStudyAllusersAtTpData] = useState(null);
  const chartRef = useRef(null);
  const [NumberOfGr, setNumberOfGr] = useState(null);

//   useEffect(() => {
//     if (chartRef.current) {
//       // Сохраняем значение в переменную
//       const currentChartRef = chartRef.current;
  
//       // Уничтожаем чарт при размонтировании компонента
//       return () => {
//         if (currentChartRef) {
//           const chartInstance = Chart.getChart(currentChartRef); // Получаем экземпляр чарта
//           if (chartInstance) {
//             chartInstance.destroy(); // Уничтожаем чарт
//           }
//         }
//       };
//     }
//   }, []);

//   console.log("choiseGroupTeacher до запроса: ": '#', choiseGroupTeacher)

  useEffect(() => {
  const fetchVecStudyAllusersAtTpData = async () => {
    try {
        if (tokenUsers!== null) {
        const response = await fetchWithTokenRefresh(`http://moais-dashboard.ru:8082/api/speciality_kr_total_points_attendance_dynamic?token=${tokenUsers}&group_by_speciality=${choiseGroupSpeciality}${selectedTeachers ? `&teacher_list=${selectedTeachers.join(',')}` : ''}${selectedSpeciality ? `&speciality_list=${selectedSpeciality.join(',')}` : ''}`);

        const result = await response.json();
        setVecStudyAllusersAtTpData(result);  
        
        setNumberOfGr(result.length)
      }
    } catch (error) {
      console.error('VecStudyAllusersAtTp - Error fetching attendance data:', error);
    }
  };
  fetchVecStudyAllusersAtTpData();
},[tokenUsers,choiseGroupSpeciality,selectedTeachers,selectedSpeciality]);

console.log('NEW VecStudyAllusersAtTpData - ', VecStudyAllusersAtTpData)


if (!VecStudyAllusersAtTpData) {
    return <div>Loading...</div>;
  }

  const colorsByTeacher_id = {
    1: '#ef2424',
    2: '#f8e136',
    3: '#36f85d',
    4: '#113ded',

    5: '#f15cf4',
    6: '#f57305',
    7: '#05f5eb',
    8: '#705ef8',

    9: '#c0c0c0',
    10: '#ebf9a7', 
    11: '#a7f9f2', 
    12: '#a7c1f9', 

    13: '#333333', 
};


const colorsBySpeciality_id = {
  
    "43.03.02 Туризм": '#ef2424',
    "01.03.03 Механика и математическое моделирование": '#FFA500',
    "35.03.10 Ландшафтная архитектура": '#FFFF00',
    "44.03.05 Педагогическое образование (с двумя профилями подготовки)": '#00FF00',
    "10.05.03 Информационная безопасность автоматизированных систем": '#00FFFF ',
    "42.03.05 Медиакоммуникации": '#0000FF ',
    "05.03.06 Экология и природопользование": '#8A2BE2 ',
    "09.03.02 Информационные системы и технологии": '#FF1493 ',
    "05.03.02 География": '#A52A2A ',
    "NaN": '#2E8B57 ',
    "38.05.01 Экономическая безопасность": '#228B22 ',
    "06.03.01 Биология": '#00FF7F ',
    "16.03.01 Техническая физика": '#4682B4 ',
    "10.03.01 Информационная безопасность": '#B0E0E6 ',
    "03.03.02 Физика": '#800080 ',
    "05.03.03 Картография и геоинформатика": '#696969 ',
    "06.05.01 Биоинженерия и биоинформатика": '#D3D3D3 ',
    "01.03.01 Математика": '#708090 ',
    "38.03.02 Менеджмент": '#F0FFF0 ',
    "15.03.06 Мехатроника и робототехника": '#FF69B4 ',
    "10.05.01 Компьютерная безопасность": '#FF4500 ',
    "04.03.01 Химия": '#FFD700 ',
    "49.03.01 Физическая культура": '#9ACD32 ',
    "02.03.03 Математическое обеспечение и администрирование информационных систем": '#48D1CC ',
    "09.03.03 Прикладная информатика": '#',
    "38.03.01 Экономика": '#9370DB ',
}
function getColorByTeacherAndSpeciality(teacherId, speciality) {
  return colorsByTeacher_id[teacherId] || colorsBySpeciality_id[speciality];
  // || getRandomColor();
}

// function getRandomColor() {
//   return '#' + Math.floor(Math.random() * 16777215).toString(16); // Генерация случайного HEX цвета
// }


    const data = {
      labels: VecStudyAllusersAtTpData.map(item => {
        if (item.teacher_name) {
            return `${item.stud_speciality} - ${item.teacher_name}`;
        } else {
            return item.stud_speciality;
        }
    }),

        datasets: [
          {
              label: ` Средняя посещаемость (после 1й КР)`,
              data: VecStudyAllusersAtTpData.map((item) => item.Посещаемость_средняя),
              backgroundColor: VecStudyAllusersAtTpData.map((item) => getColorByTeacherAndSpeciality(item.teacher_id, item.stud_speciality)),
              borderWidth: 1,
            },
      
          {
              label: `Средняя успеваемость (после 1й КР)`,
              data: VecStudyAllusersAtTpData.map((item) => item.Успеваемость_средняя),
              backgroundColor: VecStudyAllusersAtTpData.map((item) => getColorByTeacherAndSpeciality(item.teacher_id, item.stud_speciality)),
              borderWidth: 1,        
          },
          {
            label: `Средняя посещаемость (после 2й КР)`,
            data: VecStudyAllusersAtTpData.map((item) => item.Посещаемость_средняя0),
            backgroundColor: VecStudyAllusersAtTpData.map((item) => getColorByTeacherAndSpeciality(item.teacher_id, item.stud_speciality)),
            borderWidth: 1,
    
        },
        {
            label: `Средняя успеваемость (после 2й КР)`,
            data: VecStudyAllusersAtTpData.map((item) => item.Успеваемость_средняя0),
            backgroundColor: VecStudyAllusersAtTpData.map((item) => getColorByTeacherAndSpeciality(item.teacher_id, item.stud_speciality)),
            borderWidth: 1,        
        },
        {
          label: `Средняя посещаемость (после 3й КР)`,
          data: VecStudyAllusersAtTpData.map((item) => item.Посещаемость_средняя1),
          backgroundColor: VecStudyAllusersAtTpData.map((item) => getColorByTeacherAndSpeciality(item.teacher_id, item.stud_speciality)),
          borderWidth: 1,
  
      },
      {
          label: `Средняя успеваемость (после 3й КР)`,
          data: VecStudyAllusersAtTpData.map((item) => item.Успеваемость_средняя1),
          backgroundColor: VecStudyAllusersAtTpData.map((item) => getColorByTeacherAndSpeciality(item.teacher_id, item.stud_speciality)),
          borderWidth: 1,        
      },
      {
        label: `Средняя посещаемость (после аттестации)`,
        data: VecStudyAllusersAtTpData.map((item) => item.Посещаемость_средняя2),
        backgroundColor: VecStudyAllusersAtTpData.map((item) => getColorByTeacherAndSpeciality(item.teacher_id, item.stud_speciality)),
        borderWidth: 1,
  
    },
    {
        label: `Средняя успеваемость (после аттестации)`,
        data: VecStudyAllusersAtTpData.map((item) => item.Успеваемость_средняя2),
        backgroundColor: VecStudyAllusersAtTpData.map((item) => getColorByTeacherAndSpeciality(item.teacher_id, item.stud_speciality)),
        borderWidth: 1,        
    },
          
      ],

    };
    
    const options = {
        // onClick: handleTeleportGroup,
        scales: {
        x: {
            grouped: true, 
        //     ticks: {
        //         display: true,
        // },
        ticks: {
          display: true,         
          padding: 0,
          labelOffset: 0,
          minRotation: 0,
          // maxRotation: 99,
          // maxTicksLimit: 10,
          
      },
      
            type: 'category',
            position: 'bottom',
            title: {
                display: true,
                text: 'Все группы',
                font: {
                    size: 20, 
                    fontColor: 'black',
                    family: 'Trebuchet MS'
                },
            },
        },
        y: {
            type: 'linear', 
            position: 'left',
            title: {
            display: true,
            text: 'Баллы/успеваемость',
            font: {
                size: 20, 
                fontColor: 'black',
                family: 'Trebuchet MS'
            },
            },
        },
        },
        plugins: {
        datalabels: {
            display: true,
            rotation: 0,

            anchor: 'end',
            align: 'end',
            color: 'black',  // Цвет текста
            formatter: (value, context) => {
              return ;

            },
        },


        title: {
            display: true,
            text: `Учебные показатели после КР, кол-во: ${NumberOfGr}`,
            font: {
            size: 22,
            fontColor: 'black',
            family: 'Trebuchet MS'
            },
        },
    
        legend: {
          display: true,
          position: 'bottom',
          labels: {
              usePointStyle: true,
              generateLabels: function(chart) {
                  const uniqueLabels = new Set();
                  const labels = [];
                  VecStudyAllusersAtTpData.forEach((item) => {
                      let label;
                      let fillStyle;
                      if (item.teacher_name) {
                          label = item.teacher_name;
                          fillStyle = colorsByTeacher_id[item.teacher_id];
                      } else if (item.stud_speciality && colorsBySpeciality_id[item.stud_speciality]) {
                          label = item.stud_speciality;
                          fillStyle = colorsBySpeciality_id[item.stud_speciality];
                      } else {
                          return; // Пропускаем элемент, если ни учителя, ни специальности нет
                      }
                      if (!uniqueLabels.has(label)) {
                          uniqueLabels.add(label);
                          labels.push({
                              text: label,
                              fillStyle: fillStyle 
                          });
                      }
                  });
                  return labels;
              },
          },
          events: [],
      }
      
        },

        maintainAspectRatio: false,
        layout: {
        padding: {
            left: 30,
            right: 30,
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

    // }
    // }, [VecStudyAllusersAtTpData]);
  
    return(<>
      <Bar ref={chartRef} data={data} options={options} />;
      
  </>) 
    
  };
export default VecStudyAllusersAtTp;