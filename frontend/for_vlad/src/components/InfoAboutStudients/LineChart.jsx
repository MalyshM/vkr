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
