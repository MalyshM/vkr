
import React, { useEffect, useRef ,useState,createContext } from 'react';
import { Bar } from 'react-chartjs-2';
import { useNavigate  } from 'react-router-dom';
import { Flex, Text, NumberInput, NumberInputField, NumberInputStepper, NumberIncrementStepper, NumberDecrementStepper, Center, Spacer, theme  } from '@chakra-ui/react';
import { ChakraProvider, Button, Box } from '@chakra-ui/react';
import { useNumberItems } from './NumberItemsContext';

import 'chartjs-plugin-trendline';

const AtendenceTotalPoints = ({teamId,teamName}) => {

  const navigate = useNavigate ();
  const [attendanceTotalPointsData, setAttendanceTotalPointsData] = useState(null);
  const chartRef = useRef(null);
  const [sortBy, setSortBy] = useState('Успеваемость'); // По умолчанию сортировка по посещаемости
  const [threshold, setThreshold] = useState(61);  
  
  const [totalPointsAvg, setTotalPointsAvg] = useState(null);
  const [arrivalAvg, setArrivalAvg] = useState(null);

  const [successColor, setSuccessColor] = useState('rgba(86, 173, 192, 1)');
  const [attendanceColor, setAttendanceColor] = useState('rgba(223, 88, 87, 1) ');

  const [numberOfItems ,setNumberOfItems] = useState(null)
  
  const [yAxisTitle, setYAxisTitle] = useState('Баллы'); // Изначально установлено значение для 'Баллы'

const handleButtonClick = (sortType) => {
  setSortBy(sortType);
  
  if (sortType === 'Успеваемость') {
    setYAxisTitle('Баллы');
  } else if (sortType === 'Посещаемость') {
    setYAxisTitle('Процент посещения');
  }

  // Обновляем цвет графика в зависимости от выбранной кнопки
  if (sortType === 'Успеваемость') {
    setSuccessColor('rgba(86, 173, 192, 1)'); 
    setAttendanceColor('rgba(223, 88, 87, 1)');
  } else {
    setSuccessColor('rgba(223, 88, 87, 1)');
    setAttendanceColor('rgba(86, 173, 192, 1)')
};
};

  
  const handleChartClick = (_, elements) => {
    if (elements && elements.length > 0) {
      const clickedElement = elements[0];
      const dataIndex = clickedElement.index;
      const studentId = attendanceTotalPointsData[dataIndex]?.Stud_id;
      navigate (`/student/${studentId}/${teamId}/${teamName}`);
    }
  };

  useEffect(() => {
    const fetchAtendanceTotalPointsData = async () => {
      try {
        if (teamId !== null) { 
          const response = await fetch(`http://localhost:8090/api/total_points_attendance_per_stud_for_team?id_team=${teamId}`);
          const result = await response.json();

          const lastItem = result[result.length - 1];

          console.log('Last item from API:', lastItem);

          if ('total_points_avg' in lastItem && 'arrival_avg' in lastItem) {
            // Обновляем состояния для новых данных
            setTotalPointsAvg(lastItem.total_points_avg);
            setArrivalAvg(lastItem.arrival_avg);
          }
          const dataArray = Object.values(result);
          const sortedDataArray = dataArray.sort((a, b) =>
              sortBy === 'Посещаемость' ? b.Посещаемость - a.Посещаемость : b.Успеваемость - a.Успеваемость
            );
          // Обновляем состояние с полученными данными
          setAttendanceTotalPointsData(sortedDataArray);
          setNumberOfItems(sortedDataArray.length - 1);
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
    labels: attendanceTotalPointsData.map((item => item.Stud_id)),
    

    datasets: [
      {
        label: 'Линия уровня',
        data: Array(attendanceTotalPointsData.length).fill(threshold), // Постоянное значение y
        borderColor: 'rgba(0, 0, 0, 0.8)', // Цвет линии уровня
        borderWidth: 2,
        fill: false,
        // borderDash: [5, 5], // Пунктирный стиль (по желанию)
        type: 'line',
        radius: 0,
      },
        
      {
        label: 'Успеваемость',
        data: attendanceTotalPointsData.map((item) => item.Успеваемость),
        backgroundColor: successColor,
        radius: 0,

      },
      {
        label: 'Посещаемость',
        data: attendanceTotalPointsData.map((item) => item.Посещаемость),
        backgroundColor: attendanceColor,
        borderWidth: 0,
      },
      {
      label: 'Total Points Avg',
      data: Array(attendanceTotalPointsData.length).fill(totalPointsAvg),
      borderColor: 'rgba(0, 28, 172, 1)',
      borderWidth: 3,
      fill: false,
      type: 'line',
      radius: 0,
    },
    {
      label: 'Arrival Avg',
      data: Array(attendanceTotalPointsData.length).fill(arrivalAvg),
      borderColor: 'rgb(255,100,50)',
      borderWidth: 3,
      fill: false,
      type: 'line',
      radius: 0,
      
    },

    
    ],
  };

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
        text: yAxisTitle,
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
    background: {
      color: 'red' // Set the background color for the entire canvas
    },
    datalabels: {
      display: false,
        anchor: 'end',
        align: 'end',
        color: 'black',
        formatter: (value, context) => {
          return `${value}%`; // Замените на тот формат, который вам нужен
        },
      },
    title: {
      display: true,
      text: `Посещаемость и успеваемость студентов группы ${teamName}, кол-во студентов:${numberOfItems}`,
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
  },
  maintainAspectRatio: false, 
  layout: {
    padding: {
      left: 40,
      right: 10,
      top: 10,
      bottom: 10,
    },
  },
  elements: {
    bar: {
      barThickness: 400,
      borderRadius: 6,
      backgroundColor: 'rgba(60, 60, 60, 0.9)',

    },
  },
  animation: {
    duration: 2000,
  },

};


return (
<>

<Flex align="center" justifyContent='space-around' mb={3}>

<Flex align="center">
        <Text fontFamily={'Trebuchet MS'} mr={2}>Выберите режим:</Text> 
        <Button fontFamily={'Trebuchet MS'}
          as='samp'
          colorScheme={sortBy === 'Успеваемость' ? 'teal' : 'transparent'}
          onClick={() => handleButtonClick('Успеваемость')}
          size="md"
          color={sortBy  === 'Успеваемость' ? 'white' : 'black'} 
          // backgroundColor={sortBy === 'Успеваемость' ? 'transparent' : undefined}
          // _hover={{ backgroundColor: sortBy === 'Успеваемость' ? 'transparent' : undefined }}      
        >
          Успеваемость
        </Button>

        <Button fontFamily={'Trebuchet MS'} ml={0}
        as='samp'
          colorScheme={sortBy === 'Посещаемость' ? 'teal' : 'transparent'}
          onClick={() => handleButtonClick('Посещаемость')}
          size="md"
          color={sortBy  === 'Посещаемость' ? 'white' : 'black'} 
          // backgroundColor={sortBy === 'Посещаемость' ? 'transparent' : undefined}
          // _hover={{ backgroundColor: sortBy === 'Посещаемость' ? 'transparent' : undefined }}
        >
          Посещаемость
        </Button>
      </Flex>

  <Flex align="center">
  <Text bg={'white'} fontFamily={'Trebuchet MS'} borderColor={'rgba(0, 28, 172, 1)'} mr={2} p={2} borderWidth={2} borderRadius={6}>Среднее посещение: {arrivalAvg.toFixed(2)}%</Text>

  <Text bg={'white'} fontFamily={'Trebuchet MS'} borderColor={'rgb(255,100,50)'} mr={2} p={2} borderWidth={2} borderRadius={6}>Средний балл: {totalPointsAvg.toFixed(2)}</Text>
    
    <Text fontFamily={'Trebuchet MS'} ml={10}>Установите порог:</Text>
          <NumberInput
          bg={'white'}
          borderColor={'teal'}
          fontFamily={'Trebuchet MS'}
            // ml={4}
            borderWidth={0}
            ml={2}
            min={0}
            max={100}
            maxW={24} 
            value={threshold}
            onChange={(valueAsString, valueAsNumber) => setThreshold(valueAsNumber)}
          >
            <NumberInputField />
            <NumberInputStepper>
              <NumberIncrementStepper />
              <NumberDecrementStepper />
            </NumberInputStepper>
          </NumberInput>
  </Flex>

  
  </Flex>
  <Box h={'368'} bg={'white'} borderRadius={20}>
      <Bar ref={chartRef} data={data} options={options} />
    </Box>
    

</> 
   
  );
};

export default AtendenceTotalPoints;

