
import React, { useEffect, useRef ,useState,createContext } from 'react';
import { Bar } from 'react-chartjs-2';
import { useNavigate  } from 'react-router-dom';
import { Flex, Text, NumberInput, NumberInputField, NumberInputStepper, NumberIncrementStepper, NumberDecrementStepper, Center, Spacer, theme  } from '@chakra-ui/react';
import { ChakraProvider, Button, Box } from '@chakra-ui/react';

import { useNumberItems } from './NumberItemsContext';
import RequestCheckbox from '../ReportSystem/RequestCheckbox';

import {Tooltip } from '@chakra-ui/react';
import { QuestionOutlineIcon } from '@chakra-ui/icons'

import { fetchWithTokenRefresh } from '../RefreshToken';

import 'chartjs-plugin-trendline';

const AtendenceTotalPoints = ({teamId,teamName}) => {
  const [requests, setRequests] = useState([]);

  const navigate = useNavigate ();
  const [attendanceTotalPointsData, setAttendanceTotalPointsData] = useState(null);
  const chartRef = useRef(null);
  const [sortBy, setSortBy] = useState('Успеваемость'); // По умолчанию сортировка по посещаемости
  
  const [totalPointsAvg, setTotalPointsAvg] = useState(null);
  const [arrivalAvg, setArrivalAvg] = useState(null);

  const [successColor, setSuccessColor] = useState('rgba(0,174,239, 1)');
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
    setSuccessColor('rgba(0,174,239, 1)'); 

    setAttendanceColor('rgba(223, 88, 87, 1)');
  } else {
    setSuccessColor('rgba(223, 88, 87, 1)');
    setAttendanceColor('rgba(0,174,239, 1)')
};
};

  
  const handleChartClick = (_, elements) => {
    if (elements && elements.length > 0) {
      const clickedElement = elements[0];
      const dataIndex = clickedElement.index;
      const studentId = attendanceTotalPointsData[dataIndex]?.stud_id;
      navigate (`/student/${studentId}`);
    }
  };

  useEffect(() => {
    const fetchAtendanceTotalPointsData = async () => {
      try {
        if (teamId !== null) { 
          const response = await fetchWithTokenRefresh(`http://moais-dashboard.ru:8082/api/total_points_attendance_per_stud_for_team?id_team=${teamId}`);
          const result = await response.json();

          console.log('Total_points_attendance_per_stud_for_team:', result);

          const sortedDataArray = result.sort((a, b) =>
              sortBy === 'Посещаемость' ? b.Посещаемость - a.Посещаемость : b.Успеваемость - a.Успеваемость
            );
          // Обновляем состояние с полученными данными
          setAttendanceTotalPointsData(sortedDataArray);
          setNumberOfItems(sortedDataArray.length);


          
          
          const firstStudentAtendence = sortedDataArray[0];
          const averageAttendance = firstStudentAtendence.Посещаемость_средняя;
          // Устанавливаем значение в состояние arrivalAvg
          setArrivalAvg(averageAttendance);

          const firstStudentTotalPoints = sortedDataArray[0];
          const averageTotalPoints = firstStudentTotalPoints.Успеваемость_средняя;
          // Устанавливаем значение в состояние arrivalAvg
          setTotalPointsAvg(averageTotalPoints);

          
        }
      } catch (error) {
        console.error('Error fetching attendanceTotalPoints data:', error);
      }
    };
    fetchAtendanceTotalPointsData();
  },[teamId,sortBy]);
  console.log("NOW: attendanceTotalPointsData", attendanceTotalPointsData);


  if (!attendanceTotalPointsData) {
    return <div>Loading...</div>;
  }



  const data = {
    labels: attendanceTotalPointsData.map((item => item.stud_id)),
    
    datasets: [
      
        
      {
        label: 'Успеваемость',
        data: attendanceTotalPointsData.map((item) => item.Успеваемость),
        backgroundColor: successColor,
        radius: 0,

      },
      {
        label: 'Посещаемость %',
        data: attendanceTotalPointsData.map(item => Math.round(item.Посещаемость)),
        backgroundColor: attendanceColor,
        borderWidth: 0,

      },
      {
      label: 'Total Points Avg',
      data: Array(attendanceTotalPointsData.length).fill(totalPointsAvg.toFixed(2)),
      borderColor: 'rgba(0, 28, 172, 1)',
      borderWidth: 3,
      fill: false,
      type: 'line',
      radius: 0,
    },
    {
      label: 'Arrival Avg',
      data: Array(attendanceTotalPointsData.length).fill(Math.round(arrivalAvg)),
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

const requestUrl=`http://moais-dashboard.ru:8082/api/total_points_attendance_per_stud_for_team?id_team=${teamId}`;

const handleUpdateRequests = (updatedRequests) => {
  setRequests(updatedRequests);
};

return (
<>

<Flex align="center" justifyContent='space-between' mb={3}>

  <Flex align="center" justifyContent='space-between' >

    <Text mr={4} fontFamily={'Trebuchet MS'}>Выберите режим:</Text> 

    <Flex >
    <Button 
      fontFamily={'Trebuchet MS'}
      as='samp'
      colorScheme={sortBy === 'Успеваемость' ? 'blue' : 'transparent'}
      onClick={() => handleButtonClick('Успеваемость')}
      size="md"
      color={sortBy === 'Успеваемость' ? 'white' : 'black'} 
    >
      Успеваемость
    </Button>
    <Button 
      fontFamily={'Trebuchet MS'} 
      as='samp'
      colorScheme={sortBy === 'Посещаемость' ? 'blue' : 'transparent'}
      onClick={() => handleButtonClick('Посещаемость')}
      size="md"
      color={sortBy === 'Посещаемость' ? 'white' : 'black'} 
    >
      Посещаемость
    </Button>
    </Flex>
    
  </Flex>

  <Flex align="center"> 
    <Text bg={'white'} fontFamily={'Trebuchet MS'} borderColor={'rgba(0, 28, 172, 1)'} mr={3} p={2} borderWidth={2} borderRadius={6}>Медиана поещаемости:{totalPointsAvg.toFixed(2)}
    </Text>
    
    <Text bg={'white'} fontFamily={'Trebuchet MS'} borderColor={'rgb(255,100,50)'} mr={3} p={2} borderWidth={2} borderRadius={6}>Медиана Успеваемости:{Math.round(arrivalAvg)}%</Text>
  </Flex>
  <Flex>

  </Flex>

</Flex>

    <Box h={'40vh'} bg={'white'} borderRadius={20} >
    

        <Tooltip label="Диаграмма отображающая баллы и процент посещаемости каждого студента в выбранной группе" aria-label="A tooltip">
            <QuestionOutlineIcon ml={2} boxSize={4} cursor="pointer" />
        </Tooltip>
        <RequestCheckbox
      requestUrl={requestUrl}
      requestName="Посещаемсть и успеваемость"
      onUpdateRequests={handleUpdateRequests} />

    
      <Bar ref={chartRef} data={data} options={options} />
    </Box>
    

</> 
   
  );
};

export default AtendenceTotalPoints;

