import React, { useEffect, useRef ,useState} from 'react';
import { Bar } from 'react-chartjs-2';
import { Chart } from 'chart.js/auto';
import 'chartjs-plugin-datalabels'; // Импортируйте плагин
import { useNavigate  } from 'react-router-dom';
import { Text } from '@chakra-ui/react'
import { Legend } from 'react-chartjs-2';

const AllUsersAtendenceTotalPointsWitchGroup = ({tokenUsers, choiseGroupTeacher, selectedTeachers, allTeacherForLegend}) => {
  const [AllUsersAtendenceTotalPointsWitchGroupData, setAllUsersAtendenceTotalPointsWitchGroupData] = useState(null);
  const chartRef = useRef(null);
  const [NumberOfGr, setNumberOfGr] = useState(null);
  const navigate = useNavigate ();

  

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

  console.log("choiseGroupTeacher до запроса: ", choiseGroupTeacher)

  useEffect(() => {
  const fetchAllUsersAtendenceTotalPointsWitchGroupData = async () => {
    try {
        if (tokenUsers!== null) {
        const response = await fetch (`http://moais-dashboard.ru:8082/api/team_kr_total_points_attendance_dynamic?token=${tokenUsers}&group_by_teacher=${choiseGroupTeacher}${selectedTeachers ? `&teacher_list=${selectedTeachers.join(',')}` : ''}`);

        const result = await response.json();
        setAllUsersAtendenceTotalPointsWitchGroupData(result);  
        
        setNumberOfGr(result.length)
      }
    } catch (error) {
      console.error('AllUsersAtenadance - Error fetching attendance data:', error);
    }
  };
  fetchAllUsersAtendenceTotalPointsWitchGroupData();
},[tokenUsers,choiseGroupTeacher,selectedTeachers]);

console.log('NEW AllUsersAtendenceTotalPointsWitchGroupData - ', AllUsersAtendenceTotalPointsWitchGroupData)

console.log('allTeacherForLegend: ', allTeacherForLegend)

if (!AllUsersAtendenceTotalPointsWitchGroupData) {
    return <div>Loading...</div>;
  }

  const colorsByTeacherId = {
    1: '#ef2424', //
    2: '#f8e136', //
    3: '#36f85d', //
    4: '#113ded', //

    5: '#f15cf4', //
    6: '#f57305', //
    7: '#05f5eb', //
    8: '#705ef8', //

    9: '#c0c0c0', //
    10: '#ebf9a7', // 
    11: '#a7f9f2', // 
    12: '#a7c1f9', // 

    13: '#333333', // 
};


    const data = {
        labels: AllUsersAtendenceTotalPointsWitchGroupData.map(item => item.team_name),
        datasets: [
            {
                label: 'Средняя посещаемость',
                data: AllUsersAtendenceTotalPointsWitchGroupData.map(item => Math.round(item.Посещаемость_средняя*100)),
                backgroundColor: AllUsersAtendenceTotalPointsWitchGroupData.map((item) => colorsByTeacherId[item.teacher_id]),
                borderWidth: 1,
        
            },
            {
                label: 'Средняя успеваемость',
                data: AllUsersAtendenceTotalPointsWitchGroupData.map((item) => item.Успеваемость_средняя),
                backgroundColor: AllUsersAtendenceTotalPointsWitchGroupData.map((item) => colorsByTeacherId[item.teacher_id]),
                borderWidth: 1,        
            },
            
        ],
    };
    
    const options = {
        // onClick: handleTeleportGroup,
        scales: {
        x: {
            grouped: true, 
            ticks: {
                display: true,
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
            text: 'Баллы/успеваемость',
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
                    const labels = [];
                    selectedTeachers.forEach((teacherId) => {
                      labels.push({
                        text: teacherId, // Здесь можете использовать teacherId или имя преподавателя из других источников
                        fillStyle: colorsByTeacherId[teacherId] 
                      });
                    });
                    return labels;
               
      },
    },

            
        },
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
    // }, [AllUsersAtendenceTotalPointsWitchGroupData]);
  
    return(<>
    <div>
        {choiseGroupTeacher}
    </div>
      <Bar ref={chartRef} data={data} options={options} />;
      
  </>) 
    
  };
export default AllUsersAtendenceTotalPointsWitchGroup;