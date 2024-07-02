import React, { useEffect, useRef ,useState} from 'react';
import { Bar } from 'react-chartjs-2';
import { Chart } from 'chart.js/auto';
import 'chartjs-plugin-datalabels'; // Импортируйте плагин
import { useNavigate  } from 'react-router-dom';
import { Text } from '@chakra-ui/react'
// import { Legend } from 'react-chartjs-2';
// import RequestCheckbox from '../ReportSystem/RequestCheckbox';
// import {RequestCheckbox} from '' 
import RequestCheckbox from '../../ReportSystem/RequestCheckbox'

import { fetchWithTokenRefresh } from '../../RefreshToken';

const AllUsersAtendenceTotalPointsWitchGroup = ({tokenUsers, choiseGroupTeacher, selectedTeachers, allTeacherForLegend}) => {
  const [AllUsersAtendenceTotalPointsWitchGroupData, setAllUsersAtendenceTotalPointsWitchGroupData] = useState(null);
  const chartRef = useRef(null);
  const [NumberOfGr, setNumberOfGr] = useState(null);
  const navigate = useNavigate ();
  const [requests, setRequests] = useState([]);


  console.log("choiseGroupTeacher до запроса: ", choiseGroupTeacher)

  useEffect(() => {
  const fetchAllUsersAtendenceTotalPointsWitchGroupData = async () => {
    try {
        if (tokenUsers!== null) {
        const response = await fetchWithTokenRefresh(`http://moais-dashboard.ru:8082/api/team_kr_total_points_attendance_dynamic?token=${tokenUsers}&group_by_teacher=${choiseGroupTeacher}${selectedTeachers ? `&teacher_list=${selectedTeachers.join(',')}` : ''}`);

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

// console.log('allTeacherForLegend: ', allTeacherForLegend)

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

    13: '#ecc94b', // 
};

if (!AllUsersAtendenceTotalPointsWitchGroupData) {
    return <div>Loading...</div>;
  }


  const data = {
    labels: AllUsersAtendenceTotalPointsWitchGroupData.map(item => {
      if (item.team_name) {
        //   return `${item.teacher_name} - ${item.team_name}`;
        return `${item.team_name}`;

      } else {
          return item.teacher_name;
      }
  }),

    datasets: [
        {
            label: ` Медианная посещаемость (после 1й КР)`,
            data: AllUsersAtendenceTotalPointsWitchGroupData.map((item) => item.Посещаемость_средняя),
            backgroundColor: AllUsersAtendenceTotalPointsWitchGroupData.map((item) => colorsByTeacherId[item.teacher_id]),
            borderWidth: 1,
    
        },
        {
            label: `Медианная успеваемость (после 1й КР)`,
            data: AllUsersAtendenceTotalPointsWitchGroupData.map((item) => item.Успеваемость_средняя),
            backgroundColor: AllUsersAtendenceTotalPointsWitchGroupData.map((item) => colorsByTeacherId[item.teacher_id]),
            borderWidth: 1,        
        },
        {
          label: `Медианная посещаемость (после 2й КР)`,
          data: AllUsersAtendenceTotalPointsWitchGroupData.map((item) => item.Посещаемость_средняя0),
          backgroundColor: AllUsersAtendenceTotalPointsWitchGroupData.map((item) => colorsByTeacherId[item.teacher_id]),
          borderWidth: 1,
  
      },
      {
          label: `Медианная успеваемость (после 2й КР)`,
          data: AllUsersAtendenceTotalPointsWitchGroupData.map((item) => item.Успеваемость_средняя0),
          backgroundColor: AllUsersAtendenceTotalPointsWitchGroupData.map((item) => colorsByTeacherId[item.teacher_id]),
          borderWidth: 1,        
      },
      {
        label: `Медианная посещаемость (после 3й КР)`,
        data: AllUsersAtendenceTotalPointsWitchGroupData.map((item) => item.Посещаемость_средняя1),
        backgroundColor: AllUsersAtendenceTotalPointsWitchGroupData.map((item) => colorsByTeacherId[item.teacher_id]),
        borderWidth: 1,

    },
    {
        label: `Медианная успеваемость (после 3й КР)`,
        data: AllUsersAtendenceTotalPointsWitchGroupData.map((item) => item.Успеваемость_средняя1),
        backgroundColor: AllUsersAtendenceTotalPointsWitchGroupData.map((item) => colorsByTeacherId[item.teacher_id]),
        borderWidth: 1,        
    },
    {
      label: `Медианная посещаемость (после аттестации)`,
      data: AllUsersAtendenceTotalPointsWitchGroupData.map((item) => item.Посещаемость_средняя2),
      backgroundColor: AllUsersAtendenceTotalPointsWitchGroupData.map((item) => colorsByTeacherId[item.teacher_id]),
      borderWidth: 1,

  },
  {
      label: `Медианная успеваемость (после аттестации)`,
      data: AllUsersAtendenceTotalPointsWitchGroupData.map((item) => item.Успеваемость_средняя2),
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
            min: 0, // минимальное значение оси y
            max: 110, // максимальное значение оси y

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
            text: `Учебные показатели после контрольных точек, кол-во групп: ${NumberOfGr}`,
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
                  const uniqueTeacherNames = new Set();
                  const labels = [];
                  AllUsersAtendenceTotalPointsWitchGroupData.forEach((item) => {
                      if (!uniqueTeacherNames.has(item.teacher_name)) {
                          uniqueTeacherNames.add(item.teacher_name);
                          labels.push({
                              text: item.teacher_name,
                              fillStyle: colorsByTeacherId[item.teacher_id]
                          });
                      }
                  });
                  return labels; 
      },
    },
    events: [], 

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

    const requestUrl = `http://moais-dashboard.ru:8082/api/team_kr_total_points_attendance_dynamic?token=${tokenUsers}&group_by_teacher=${choiseGroupTeacher}${selectedTeachers ? `&teacher_list=${selectedTeachers.join(',')}` : ''}`;
  
    const handleUpdateRequests = (updatedRequests) => {
        setRequests(updatedRequests);
      };

    return(<>
    <RequestCheckbox
        requestUrl={requestUrl}
        requestName="Ваши команды"
        onUpdateRequests={handleUpdateRequests}
      />
      <Bar ref={chartRef} data={data} options={options} />;
      
  </>) 
    
  };
export default AllUsersAtendenceTotalPointsWitchGroup;

