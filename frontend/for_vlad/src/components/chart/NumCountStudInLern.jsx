

  //   useEffect(() => {
//     if (chartRef.current) {
//       // Уничтожаем чарт при размонтировании компонента
//       return () => {
//         if (chartRef.current) {
//           const chartInstance = Chart.getChart(chartRef.current); // Получаем экземпляр чарта
//           if (chartInstance) {
//             chartInstance.destroy(); // Уничтожаем чарт
//           }
//         }
//       };
//     }
//   }, []);

import React, { useEffect, useRef ,useState} from 'react';
import { Bar } from 'react-chartjs-2';
// import { Chart } from 'chart.js/auto';
import { useNavigate  } from 'react-router-dom';
import { Box,Switch,Text, NumberInput, NumberInputField, NumberInputStepper, NumberIncrementStepper, NumberDecrementStepper, Center  } from '@chakra-ui/react';
// import 'chartjs-plugin-trendline';

import Chart from 'chart.js/auto';
import 'chartjs-plugin-trendline';

const chartjsPluginTrendline = require('chartjs-plugin-trendline');

Chart.register(chartjsPluginTrendline);
  

const NumCountStudInLern = ({ teamId}) => {
  const navigate = useNavigate ();
  const [AtendanceNumCountStudInLernData, setAtendanceNumCountStudInLernData] = useState(null);
  const chartRef = useRef(null);
  const [sortBy, setSortBy] = useState('Посещаемость'); // По умолчанию сортировка по посещаемости
  const [threshold, setThreshold] = useState(61);  

// useEffect(() => {
//     if (chartRef.current) {
//       const chartInstance = chartRef.current.chartInstance;
//       chartInstance.update();
//     }
//   }, [teamId, sortBy]);


// const toggleSort = () => {
//     setSortBy((prevSortBy) => (prevSortBy === 'Посещаемость' ? 'Успеваемость' : 'Посещаемость'));
//   };

//   const handleThresholdChange = (value) => {
//     const clampedValue = Math.min(Math.max(value, 0), 100);
//     setThreshold(clampedValue);};

 
//   const handleChartClick = (_, elements) => {
//     if (elements && elements.length > 0) {
//       const clickedElement = elements[0];
//       const dataIndex = clickedElement.index;
//       const studentId = attendanceTotalPointsData[dataIndex]?.id;
//       navigate (`/student/${studentId}/${teamId}`);
//     }
//   };

  // console.log('selectedTeam changed:', selectedTeam);
  console.log('team ID in NumCountStudInLern:', teamId);


  useEffect(() => {
    const fetchAtendanceNumCountStudInLernData = async () => {
      try {
        if (teamId !== null) {
          const response = await fetch(`http://localhost:8090/api/attendance_num_for_stud_for_team?id_team=${teamId}`);
          const result = await response.json();
          const dataArray = Object.values(result);
   
          // Обновляем состояние с полученными данными
          setAtendanceNumCountStudInLernData(dataArray);
        }
      } catch (error) {
        console.error('Error fetching attendanceTotalPoints data:', error);
      }
    };
    fetchAtendanceNumCountStudInLernData();
  },[teamId,sortBy]);


  


  if (!AtendanceNumCountStudInLernData) {
    return <div>Loading...</div>;
  }

//   const labelsWithIndex = AtendanceNumCountStudInLernData.map((item, index) => ({ name: item.name, index: index + 1 }));

  const data = {
    labels: AtendanceNumCountStudInLernData.map((item => item.name)),

    datasets: [
        {
            label: 'Кол-во студентов',
            data: AtendanceNumCountStudInLernData.map((item) => item.arrival),
            backgroundColor: 'rgb(51,201,139)',
            borderColor: 'rgb(0,0,0)',
            borderWidth: 2,  
    
            
    
          },

    ],
  };
console.log('Data for NumCountStudInLern:', data);

const options = {
  scales: {
    x: {
        ticks: {
            display: false,
        },
      type: 'category',
      position: 'bottom',
      title: {
        display: true,
        text: 'Встреча/пара',
        font: {
          size: 20,
          fontColor: 'black',
          family: 'Trebuchet MS',
        },
      },
    },
    y: {
      type: 'linear',
      position: 'left',
      title: {
        display: true,
        text: 'Количество студентов на паре',
        font: {
          size: 20,
          fontColor: 'black',
          family: 'Trebuchet MS',
        },
      },
      id: 'y-axis-0',
    },
  },
  plugins: {
    title: {
      display: true,
      text: 'Количество студентов на паре',
      font: {
        size: 22,
        fontColor: 'black',
        family: 'Trebuchet MS',
      },
    },
    legend: {
      display: false,
      position: 'top',
    },
    // trendline: {
    //   trendlineLinear: {
    //     style: 'rgba(43, 66, 255, 0.3)',
    //     lineStyle: 'solid',
    //     width: 2,
    //   },
    // },
  },
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



return (
   
     
        <Bar ref={chartRef} data={data} options={options} />
  
      
    
  );
};


export default NumCountStudInLern;

