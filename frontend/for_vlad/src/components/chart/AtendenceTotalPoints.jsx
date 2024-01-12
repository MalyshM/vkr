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
  

const AtendenceTotalPoints = ({ teamId}) => {
  const navigate = useNavigate ();
  const [attendanceTotalPointsData, setAttendanceTotalPointsData] = useState(null);
  const chartRef = useRef(null);
  const [sortBy, setSortBy] = useState('Посещаемость'); // По умолчанию сортировка по посещаемости
  const [threshold, setThreshold] = useState(61);  



// useEffect(() => {
//     if (chartRef.current) {
//       const chartInstance = chartRef.current.chartInstance;
//       chartInstance.update();
//     }
//   }, [teamId, sortBy]);


const toggleSort = () => {
    setSortBy((prevSortBy) => (prevSortBy === 'Посещаемость' ? 'Успеваемость' : 'Посещаемость'));
  };

  const handleThresholdChange = (value) => {
    const clampedValue = Math.min(Math.max(value, 0), 100);
    setThreshold(clampedValue);};

 

  

  const handleChartClick = (_, elements) => {
    if (elements && elements.length > 0) {
      const clickedElement = elements[0];
      const dataIndex = clickedElement.index;
      const studentId = attendanceTotalPointsData[dataIndex]?.id;
      navigate (`/student/${studentId}/${teamId}`);
    }
  };

  // console.log('selectedTeam changed:', selectedTeam);
  console.log('team ID in attendanceTotalPointsData:', teamId);


  useEffect(() => {
    const fetchAtendanceTotalPointsData = async () => {
      try {
        if (teamId !== null) {
          const response = await fetch(`http://localhost:8090/api/total_points_attendance_per_stud_for_team?id_team=${teamId}`);
          const result = await response.json();
          const dataArray = Object.values(result);
          const sortedDataArray = dataArray.sort((a, b) =>
              sortBy === 'Посещаемость' ? b.Посещаемость - a.Посещаемость : b.Успеваемость - a.Успеваемость
            );
  
  
          // Обновляем состояние с полученными данными
          setAttendanceTotalPointsData(sortedDataArray);
        }
      } catch (error) {
        console.error('Error fetching attendanceTotalPoints data:', error);
      }
    };
    fetchAtendanceTotalPointsData();
  },[teamId,sortBy]);


  


  if (!attendanceTotalPointsData) {
    return <div>Loading...</div>;
  }

  const data = {
    labels: attendanceTotalPointsData.map((item => item.id)),

    datasets: [
        {
            label: 'Линия уровня',
            data: Array(attendanceTotalPointsData.length).fill(threshold), // Постоянное значение y
            borderColor: 'rgba(0, 0, 0, 0.8)', // Цвет линии уровня
            borderWidth: 2,
            fill: false,
            borderDash: [5, 5], // Пунктирный стиль (по желанию)
            type: 'line',
            radius: 0,
            
    
          },
      {
        label: 'Успеваемость',
        data: attendanceTotalPointsData.map((item) => item.Успеваемость),
        backgroundColor: 'rgb(95,122,208)',
        borderColor: 'rgb(0,0,0)',
        borderWidth: 1,  

      },
      {
        label: 'Посещаемость',
        data: attendanceTotalPointsData.map((item) => item.Посещаемость),
        backgroundColor: 'rgb(251,157,47)',
        borderColor: 'rgb(0,0,0)',
        borderWidth: 1,
      },

     

    ],
  };
console.log('Data for chart:', data);

const options = {
onClick: handleChartClick,
  scales: {
    x: {
      type: 'category',
      position: 'bottom',
      title: {
        display: true,
        text: 'Идентификатор студента',
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
        text: 'Баллы',
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
      text: 'Посещаемость и успеваемость студентов по дисциплине выбранной группы',
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
   
        <>
        
        <Bar ref={chartRef} data={data} options={options} />
        
        <NumberInput    
        ml={4}
        mt={2}
        min={0}
        max={100}
        value={threshold}
        onChange={(valueAsString, valueAsNumber) => setThreshold(valueAsNumber)}>
        <NumberInputField />
        <NumberInputStepper>
            <NumberIncrementStepper />
            <NumberDecrementStepper />
        </NumberInputStepper>
    </NumberInput>
    <Center>
            <Text ml={2}>Выберите режим:</Text>
            <Switch onChange={toggleSort} isChecked={sortBy === 'Успеваемость'} size="md" colorScheme="twitter" />
            <Text ml={2}>{`Сортировка по: ${sortBy}`}</Text>
    </Center>
    

    
     </>
  
    
    
  );
};


export default AtendenceTotalPoints;

