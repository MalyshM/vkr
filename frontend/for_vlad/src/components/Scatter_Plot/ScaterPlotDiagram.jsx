import React, { useEffect, useRef, useState } from 'react';
import { Chart } from 'chart.js/auto';
import { Text } from '@chakra-ui/react';
import { BoxPlotChart } from '@sgratzl/chartjs-chart-boxplot';
import { Scatter } from 'react-chartjs-2';
import { fetchWithTokenRefresh } from '../RefreshToken';

const ScaterPlotDiagram = ({ tokenUsers, type_group_by , teacher_list, speciality_list,team_list }) => {

    const [ScaterPlotData, setScaterPlotData] = useState(null);

    console.log('type_group_by',type_group_by)
    

    useEffect(() => {
        const fetchScaterPlot = async () => {
          try {
              if (tokenUsers!== null) {
              console.log(`http://moais-dashboard.ru:8082/api/stud_scatter_plot?token=${tokenUsers}&type_group_by=${type_group_by}${teacher_list ? `&teacher_list=${teacher_list.join(',')}` : ''}${speciality_list ? `&speciality_list=${speciality_list.join(',')}` : ''}${team_list ? `&team_list=${team_list.join(',')}` : ''}`)
                if (type_group_by === 3 ) {
                  type_group_by = 0
                }
              const response = await fetchWithTokenRefresh (`http://moais-dashboard.ru:8082/api/stud_scatter_plot?token=${tokenUsers}&type_group_by=${type_group_by}${teacher_list ? `&teacher_list=${teacher_list.join(',')}` : ''}${speciality_list ? `&speciality_list=${speciality_list.join(',')}` : ''}${team_list ? `&team_list=${team_list.join(',')}` : ''}`);
              const result = await response.json();
              setScaterPlotData(result);              
            }
          } catch (error) {
            console.error('ScaterPlotData - Error fetching ScaterPlotData:', error);
          }
        };
        fetchScaterPlot();
      },[tokenUsers, type_group_by , teacher_list, speciality_list,team_list]);
  
    console.log('ScaterPlotData:', ScaterPlotData )
    console.log('tokenUsers after request: ',tokenUsers)

    if (!ScaterPlotData) {
      return <div>Loading...</div>;
    }

    const prepareScatterPlotData = (data) => {
      return data.map(item => ({
          x: item.result1.reduce((acc, student) => acc + student['Посещаемость'], 0) / item.result1.length, // Пример расчета средней посещаемости для оси X
          y: item.result1.reduce((acc, student) => acc + student['Успеваемость'], 0) / item.result1.length, // Пример расчета средней успеваемости для оси Y
          label: item.name // Название для точки
      }));
  };

    const data = {
      datasets: [
          {
              label: 'Scatter Plot',
              borderColor: 'rgba(75, 192, 192, 1)',
              backgroundColor: 'rgba(75, 192, 192, 1)',
              data: prepareScatterPlotData(ScaterPlotData),
          }
      ]
  };

  const options = {
      responsive: true,
      plugins: {
          legend: {
              position: 'top',
          },
          title: {
              display: true,
              text: 'Scatter Chart'
          }
      }
  };


  //   const data = {
  //       datasets: [
  //           {
  //               label: 'Dataset 1',
  //               borderColor: 'rgba(75, 192, 192, 1)',
  //               backgroundColor: 'rgba(75, 192, 192, 1)',
  //               data: [
                    
  //               ],
  //           },
  //           {
  //               label: 'Dataset 2',
  //               borderColor: 'rgba(255, 99, 132, 1)',
  //               backgroundColor: 'rgba(255, 99, 132, 1)',
  //               data: [
                   
  //               ],
  //           },
  //       ],
  //   };

  //   const options = {
  //     responsive: true,
  //     plugins: {
  //         legend: {
  //             position: 'top',
  //         },
  //         title: {
  //             display: true,
  //             text: 'Scatter Chart'
  //         }
  //     },
  //     elements: {
  //       point: {
  //           display: false, // Скрываем метки точек
  //           pointStyle: '', 
  //       },
  //   },
  //   pointLabels: {
  //       display: false, // Скрываем метки точек
  //   },


  // };
  

    return(<>
    <Scatter height={'100vh'} data={data} options={options} />
    </>);

};

export default ScaterPlotDiagram;
