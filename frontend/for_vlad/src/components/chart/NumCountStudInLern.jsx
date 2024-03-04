
import React, { useEffect, useRef ,useState} from 'react';
import { Bar } from 'react-chartjs-2';
import TableOfGroup from './TableOfGroup';
// import { TableOfGroup } from './TableOfGroup';
import { useNavigate  } from 'react-router-dom';
import { Box } from "@chakra-ui/react";
import { useNumberItems } from './NumberItemsContext';


const NumCountStudInLern = ({ teamId,onLessonSelect, numberOfItems}) => {
  const numberOfItemsRef = useNumberItems();

  const [AtendanceNumCountStudInLernData, setAtendanceNumCountStudInLernData] = useState(null);
  const [selectedLesson, setSelectedLesson] = useState(null);
  const chartRef = useRef(null);
  const [numberOfday ,setNumberOfday] = useState(null)


  const handleBarClick = (_, elements) => {
    if (elements && elements.length > 0) {
      const clickedElement = elements[0];
      const dataIndex = clickedElement.index;
      const selectedLessonName = AtendanceNumCountStudInLernData[dataIndex].name;
      setSelectedLesson(selectedLessonName);
      
      onLessonSelect(selectedLessonName);
    }
  };

  useEffect(() => {
    const fetchAtendanceNumCountStudInLernData = async () => {
      try {
        if (teamId !== null) {
          const response = await fetch(`http://localhost:8090/api/attendance_num_for_stud_for_team?id_team=${teamId}`);
          const result = await response.json();
          const dataArray = Object.values(result);
   
          // Обновляем состояние с полученными данными
          setAtendanceNumCountStudInLernData(dataArray);

          setNumberOfday(dataArray.length)

        }
      } catch (error) {
        console.error('Error fetching attendanceTotalPoints data:', error);
      }
    };
    fetchAtendanceNumCountStudInLernData();
  },[teamId]);


  
  

  if (!AtendanceNumCountStudInLernData) {
    return <div>Loading...</div>;
  }

//   const labelsWithIndex = AtendanceNumCountStudInLernData.map((item, index) => ({ name: item.name, index: index + 1 }));

  const data = {
    labels: AtendanceNumCountStudInLernData.map((item, index) => `${index + 1}. ${item.name}`),

    datasets: [
        {
            label: `Кол-во студентов`,
            data: AtendanceNumCountStudInLernData.map((item) => item.arrival),
            backgroundColor: 'rgb(49,141,159, 0.8)',
            borderColor: 'rgb(0,0,0)',
            borderWidth: 0,  
          },
    ],
  };

const options = {

  onClick: handleBarClick,
  scales: {
    x: {
        ticks: {
          callback: (value, index) => (index + 1).toString(), 
        },
      type: 'category',
      position: 'bottom',
      title: {
        display: true,
        text: 'Практика',
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
        text: 'Количество студентов',
        font: {
          size: 20,
          fontColor: 'black',
          family: 'Trebuchet MS',
        },
      },
      id: 'y-axis-0',
      ticks: {
        callback: (value) => value.toString(), // Установка значения для оси Y
      },
      
    },
  },
  plugins: {
    datalabels: {
      display: true,
        anchor: 'end',
        align: 'end',
        color: 'black',
        formatter: (value, context) => {
          return `${value}`; // Замените на тот формат, который вам нужен
        },
      },
    title: {
      display: true,
      text: `Количество студентов на практике`,
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
    },
  },
  animation: {
    duration: 2000,
  },

};



return (<>
  
  <Box  h={[330]} mt={14} bg={'white'} borderRadius={20}>
  <Bar ref={chartRef} data={data} options={options} />
</Box>
  {/* {selectedLesson && <TableOfGroup teamId={teamId} selectedLesson={selectedLesson} />} */}

</>);
};


export default NumCountStudInLern;

