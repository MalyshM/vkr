import React, { useEffect, useRef, useState } from 'react';
import { Chart } from 'chart.js/auto';
import { Text } from '@chakra-ui/react';
import { BoxPlotChart } from '@sgratzl/chartjs-chart-boxplot';

import { fetchWithTokenRefresh } from '../RefreshToken';

const AnalysKrFiltres = ({ tokenUsers, type, kr, teacher,speciality,team }) => {
  const [AnalysKrFiltresData, setAnalysKrFiltresData] = useState(null);
  const chartRef = useRef(null);

  console.log('tokenUsers,',tokenUsers)
  console.log('type',type)
  console.log('kr',kr)

  console.log('teacher,',teacher)
  console.log('speciality',speciality)
  console.log('team',team)


  useEffect(() => {
    const fetchAnalysKrFiltresData = async () => {
      try {
        if (tokenUsers !== null ) {
          // const response = await fetchWithTokenRefresh(`http://moais-dashboard.ru:8082/api/kr_analyse_with_filters?type_select=${type}&kr=${kr}&token=${tokenUsers}`);


          // прошлая реалзиация// const response = await fetchWithTokenRefresh(`http://moais-dashboard.ru:8082/api/kr_analyse_with_filters?type_select=${type}&kr=${kr}&token=${tokenUsers}${teacher?`&teacher=${teacher}`:''}${speciality?`&speciality=${speciality}`:''}${team?`&team=${team}`:''}`);

          // предложила ии const response = await fetchWithTokenRefresh(`http://moais-dashboard.ru:8082/api/kr_analyse_with_filters?type_select=${type}&kr=${kr}&token=${tokenUsers}${teacher ? `&teacher=${Array.isArray(teacher) ? teacher.join(',') : teacher}` : ''}${speciality ? `&speciality=${Array.isArray(speciality) ? speciality.join(',') : speciality}` : ''}${team ? `&team=${Array.isArray(team) ? team.join(',') : team}` : ''}`);

          const response = await fetchWithTokenRefresh(`http://moais-dashboard.ru:8082/api/kr_analyse_with_filters?token=${tokenUsers}&type_select=${type}&kr=${kr}${teacher ? `&teacher=${Array.isArray(teacher) ? teacher.join(',') : teacher}` : ''}${speciality ? `&speciality=${Array.isArray(speciality) ? speciality.join(',') : speciality}` : ''}${team ? `&team=${Array.isArray(team) ? team.join(',') : team}` : ''}`);

          // const response = await fetchWithTokenRefresh(`http://moais-dashboard.ru:8082/api/kr_analyse_with_filters?&token=${tokenUsers}&kr=${kr}&type_select=${type}${teacher?`&teacher=${teacher}`:''}${speciality?`&speciality=${speciality}`:''}${team?`&team=${team}`:''}`);

          const result = await response.json();
          setAnalysKrFiltresData(result);
        }
      } catch (error) {
        console.error('AnalysKrFiltresData - Error fetching AnalysKrFiltresData data:', error);
      }
    };
    fetchAnalysKrFiltresData();
  }, [type, kr, tokenUsers,teacher,speciality,team]);

  useEffect(() => {
    if (Array.isArray(AnalysKrFiltresData)) {
 
      const labels = AnalysKrFiltresData.map(item => item.team_name || item.speciality || item.teacher_name );
      const data = AnalysKrFiltresData.map(item => item.test_mark_list);

      const boxplotData = {
        labels: labels,
        datasets: [
          {
            label: 'Boxplot',
            data: data,
            borderColor: 'rgba(86, 173, 192, 1)',
            backgroundColor: 'rgba(223, 88, 87, 0.9)',
            borderWidth: 2,
          },
        ],
      };

      const config = {
        type: 'boxplot',
        data: boxplotData,

        options: {
          scales: {
            x: {
              stacked: true, 
              ticks: {
                display: true,
            },
              type: 'category',
              position: 'bottom',
              title: {
                display: false,
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
              display: false,
              anchor: 'end',
              align: 'end',
              color: 'black', // Цвет текста
              formatter: (value, context) => {
                const teacherName = data.labels[context.dataIndex].split(' ')[1].slice(1, -1); // Получаем teacher_name
                return teacherName;
      
              },
            },

            title: {
              display: true,
              text: 'Точный График результатов контрольных работ',
              font: {
                size: 22,
                fontColor: 'black',
                family: 'Trebuchet MS'
              },
            },
        
            legend: {
              display: false,
            },
          },
          maintainAspectRatio: false,
          responsive: true, 
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
        },
      };

      const ctx = chartRef.current.getContext('2d');

      if (chartRef.current.chart) {
        chartRef.current.chart.destroy();
      }

      chartRef.current.chart = new BoxPlotChart(ctx, config);

    }
  }, [AnalysKrFiltresData]);

  if (!AnalysKrFiltresData) {
    return <div>Loading...</div>;
  }

  return (
    
      <canvas ref={chartRef} > </canvas>
    
  );
};

export default AnalysKrFiltres;