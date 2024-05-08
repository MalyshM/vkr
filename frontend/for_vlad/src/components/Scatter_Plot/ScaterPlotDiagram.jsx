import React, { useEffect, useRef, useState } from 'react';
import { Chart } from 'chart.js/auto';
import { Text } from '@chakra-ui/react';
import { BoxPlotChart } from '@sgratzl/chartjs-chart-boxplot';
import { Scatter } from 'react-chartjs-2';
import { fetchWithTokenRefresh } from '../RefreshToken';

const ScaterPlotDiagram = ({ tokenUsers, type_group_by , teacher_list, speciality_list,team_list }) => {

    const [ScaterPlotData, setScaterPlotData] = useState(null);

    console.log('type_group_by',type_group_by)
   
    console.log('chek teacher_list',teacher_list) 
    console.log('chek speciality_list',speciality_list)
    console.log('chek team_list',team_list)

    useEffect(() => {
        const fetchScaterPlot = async () => {
          try {
              if (tokenUsers!== null) {
                if (type_group_by === 3 ) {
                  type_group_by = 0
                }
              const response = await fetchWithTokenRefresh (`http://moais-dashboard.ru:8082/api/stud_scatter_plot?token=${tokenUsers}&type_group_by=${type_group_by}${teacher_list ? `&teacher_list=${Array.isArray(teacher_list) ? teacher_list.join(',') : teacher_list}` : ''}${speciality_list ? `&speciality_list=${Array.isArray(speciality_list) ? speciality_list.join(',') : speciality_list}` : ''}
              ${team_list ? `&team_list=${Array.isArray(team_list) ? team_list.join(',') : team_list}` : ''}`);
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

    const data = {
      datasets: [
          {
              label: 'Dataset 1',
              borderColor: 'rgba(75, 192, 192, 1)',
              backgroundColor: 'rgba(75, 192, 192, 1)',
              data: []
          }
      ],
  };
  
  // Обходим каждый объект в массиве ScaterPlotData
  ScaterPlotData.forEach(item => {
      
      item.result1.forEach(student => {// Обходим каждый объект result1 в текущем объекте
         
          data.datasets[0].data.push({ // Извлекаем значения Пос и Усп и добавляем их в данные диаграммы
              x: student['Посещаемость'],
              y: student['Успеваемость'],
              name: student['stud_id'] // Используем stud_id в качестве имени точки
          });
      });
  });
  
  const options = {
    responsive: true,
    plugins: {
        legend: {
            display: true,
        },
        title: {
            display: false,
            text: 'Scatter Chart'
        },
        tooltip: {
            callbacks: {
                label: function(context) {
                    let label = '';
                    const dataItem = ScaterPlotData[context.dataIndex];

                   
                    
                    if (dataItem && dataItem.name) {
                        label += `${label ? '\n' : ''}name: ${dataItem.name}`;
                    }

                    if (dataItem && dataItem.speciality) {
                        label += `${label ? '\n' : ''}speciality: ${dataItem.speciality}`;
                    }

                    if (dataItem && dataItem.team_id) {
                        label += `${label ? '\n' : ''}team_id: ${dataItem.team_id}`;
                    }

                    return label;
                }
            }
        }
    },
};


  
 

    return(<>
    <Scatter height={'100vh'} data={data} options={options} />
    </>);

};

export default ScaterPlotDiagram;
