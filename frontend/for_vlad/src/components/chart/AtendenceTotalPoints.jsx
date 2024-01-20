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
import { useNavigate  } from 'react-router-dom';
import { Flex, Text, NumberInput, NumberInputField, NumberInputStepper, NumberIncrementStepper, NumberDecrementStepper, Center, Spacer, theme  } from '@chakra-ui/react';
import { ChakraProvider, Button, CSSReset } from '@chakra-ui/react';

import 'chartjs-plugin-trendline';
  



const AtendenceTotalPoints = ({teamId,teamName}) => {
  const navigate = useNavigate ();
  const [attendanceTotalPointsData, setAttendanceTotalPointsData] = useState(null);
  const chartRef = useRef(null);
  const [sortBy, setSortBy] = useState('Успеваемость'); // По умолчанию сортировка по посещаемости
  const [threshold, setThreshold] = useState(61);  
  
  const [totalPointsAvg, setTotalPointsAvg] = useState(null);
  const [arrivalAvg, setArrivalAvg] = useState(null);

  const [successColor, setSuccessColor] = useState('rgb(177,185,253, 0.9)');
  const [attendanceColor, setAttendanceColor] = useState('rgb(255,227,94, 0.9)');


const handleButtonClick = (sortType) => {
  setSortBy(sortType);

  // Обновляем цвет графика в зависимости от выбранной кнопки
  if (sortType === 'Успеваемость') {
    setSuccessColor('rgb(177,185,253, 0.9)');
    setAttendanceColor('rgb(255,227,94, 0.9)');
  } else {
    setSuccessColor('rgb(255,227,94, 0.9)');
    setAttendanceColor('rgb(177,185,253, 0.9)')
};
};

const toggleSort = () => {
    setSortBy((prevSortBy) => (prevSortBy === 'Посещаемость' ? 'Успеваемость' : 'Посещаемость'));
  };

  
  const handleChartClick = (_, elements) => {
    if (elements && elements.length > 0) {
      const clickedElement = elements[0];
      const dataIndex = clickedElement.index;
      const studentId = attendanceTotalPointsData[dataIndex]?.Stud_id;
      navigate (`/student/${studentId}/${teamId}/${teamName}`);
    }
  };

  // console.log('selectedTeam changed:', selectedTeam);
  // console.log('team ID in attendanceTotalPointsData:', teamId);


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
  console.log('setTotalPointsAvg:', setTotalPointsAvg);
  console.log('setArrivalAvg:', setArrivalAvg);
  const data = {
    labels: attendanceTotalPointsData.map((item => item.Stud_id)),
    

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
      borderColor: 'rgb(255,0,0)',
      borderWidth: 2,
      fill: false,
      type: 'line',
      radius: 0,
    },
    {
      label: 'Arrival Avg',
      data: Array(attendanceTotalPointsData.length).fill(arrivalAvg),
      borderColor: 'rgb(0,255,0)',
      borderWidth: 2,
      fill: false,
      type: 'line',
      radius: 0,
      
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
      text: `Посещаемость и успеваемость студентов группы ${teamName}`,
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
      left: 0,
      right: 40,
      top: 0,
      bottom: 0,
    },
  },
  elements: {
    bar: {
      barThickness: 400,
      borderRadius: 6,
    },
  },
  animation: {
    duration: 2000,
  },

};

const buttonStyle = {
  fontFamily: 'Trebuchet MS',
  padding: '10px',
  margin: '0 5px',
  cursor: 'pointer',
  borderRadius: '16px',
  border: '1px solid #ccc',
  color: 'white',
  fontSize: '20px'
};

const successButtonStyle = {
  ...buttonStyle,
  background: sortBy === 'Успеваемость' ? '#B1B9FD' : '#ffeb8e',
};

const attendanceButtonStyle = {
  ...buttonStyle,
  background: sortBy === 'Посещаемость' ? '#B1B9FD' : '#ffeb8e',
};



return (
<>

<Flex align="center" justifyContent='space-around'>
  <Flex align="center">
  <Text borderColor={'rgb(0,255,0)'} mr={2} p={2} borderWidth={2} borderRadius={6}>Среднее посещение: {arrivalAvg.toFixed(2)}</Text>

  <Text borderColor={'rgb(255,0,0)'} mr={2} p={2} borderWidth={2} borderRadius={6}>Средний балл: {totalPointsAvg.toFixed(2)}</Text>
    <Text ml={10}>Выберите уровень:</Text>
          <NumberInput
            // ml={4}
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

  <ChakraProvider theme={theme}>
      <CSSReset />
  <Flex align="center">
        <Text mr={2}>Выберите режим:</Text>
        <div>
          <button
            style={successButtonStyle}
            onClick={() => handleButtonClick('Успеваемость')}
          >
            Успеваемость
          </button>
          <button
            style={attendanceButtonStyle}
            onClick={() => handleButtonClick('Посещаемость')}
          >
            Посещаемость
          </button>
        </div>
        {/* <Button
          colorScheme={sortBy === 'Успеваемость' ? 'purple' : 'gray'}
          onClick={() => handleButtonClick('Успеваемость')}
          size="md"
        >
          Успеваемость
        </Button>
        <Button ml={5}
          colorScheme={sortBy === 'Посещаемость' ? 'purple' : 'gray'}
          onClick={() => handleButtonClick('Посещаемость')}
          size="md"
        >
          Посещаемость
        </Button> */}
      </Flex>
      </ChakraProvider>
  </Flex>
    
    <Bar ref={chartRef} data={data} options={options} />

</> 
   
  );
};

export default AtendenceTotalPoints;

