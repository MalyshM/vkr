// LineChart.jsx

import React from 'react';
import { Line } from 'react-chartjs-2';

const LineChart = ({ data, options }) => {
  return (
    <Line
      data={data}
      options={{
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          x: {
            type: 'linear',
            position: 'bottom',
          },
          y: {
            min: 0,
            max: 100, // Установите максимальное значение оси y, если необходимо
          },
        },
        plugins: {
          datalabels: {
            display: false,
            anchor: 'end',
            align: 'end',
            color: 'black', // Цвет текста
            formatter: (value, context) => {
              return `${data[context.dataIndex].avg_total_points.toFixed(0)} Б`;
    
            },
          },
          legend: {
            display: false, // Установите true, если хотите отобразить легенду
          },
          title: {
            display: true,
            text: 'График', // Заголовок графика
          },
        },
        ...options, // Переданные пользователем опции
      }}
    />
  );
};

export default LineChart;
