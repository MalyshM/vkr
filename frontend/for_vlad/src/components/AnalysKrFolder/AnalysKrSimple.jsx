import React, { useEffect, useRef, useState } from 'react';
import { Chart } from 'chart.js/auto';
import { Text } from '@chakra-ui/react';
import { BoxPlotChart } from '@sgratzl/chartjs-chart-boxplot';

const AnalysKrSimple = ({ tokenUsers, type, kr }) => {
  const [AnalysKrSimpleData, setAnalysKrSimpleData] = useState(null);
  const chartRef = useRef(null);

  useEffect(() => {
    const fetchAnalysKrSimpleData = async () => {
      try {
        if (type !== null && kr !== null) {
          const response = await fetch(`http://localhost:8090/api/kr_analyse_simple?type=${type}&kr=${kr}&token=${tokenUsers}`);
          const result = await response.json();
          setAnalysKrSimpleData(result);
        }
      } catch (error) {
        console.error('AnalysKrSimpleData - Error fetching attendance data:', error);
      }
    };
    fetchAnalysKrSimpleData();
  }, [type, kr, tokenUsers]);

  console.log("tokenUsers - ", tokenUsers)
  console.log("type - ", type)
  console.log("kr - ", kr)
  console.log("AnalysKrSimpleData - ", AnalysKrSimpleData)

  

  useEffect(() => {
    if (AnalysKrSimpleData) {
      const labels = Object.keys(AnalysKrSimpleData);
      const data = Object.values(AnalysKrSimpleData);


      const boxplotData = {
        labels: labels,
        datasets: [
          {
            label: 'Boxplot',
            data: data,
            backgroundColor: 'rgba(86, 173, 192, 0.8)',
            borderColor: 'rgba(223, 88, 87, 1)',
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
              text: 'Общий график результатов контрольных работ',
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
  }, [AnalysKrSimpleData]);

  if (!AnalysKrSimpleData) {
    return <div>Loading...</div>;
  }

  return (
    
      <canvas ref={chartRef} > </canvas>
    
  );
};

export default AnalysKrSimple;