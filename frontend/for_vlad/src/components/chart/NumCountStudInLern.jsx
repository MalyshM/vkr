
import React, { useEffect, useRef ,useState} from 'react';
import { Bar } from 'react-chartjs-2';
import TableOfGroup from './TableOfGroup';
// import { TableOfGroup } from './TableOfGroup';
import { useNavigate  } from 'react-router-dom';
import { Flex } from "@chakra-ui/react";


const NumCountStudInLern = ({ teamId,onLessonSelect }) => {
  const [AtendanceNumCountStudInLernData, setAtendanceNumCountStudInLernData] = useState(null);
  const [selectedLesson, setSelectedLesson] = useState(null);
  const chartRef = useRef(null);

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
    labels: AtendanceNumCountStudInLernData.map((item => item.name)),

    datasets: [
        {
            label: 'Кол-во студентов',
            data: AtendanceNumCountStudInLernData.map((item) => item.arrival),
            backgroundColor: 'rgb(255,77,65, 0.5)',
            borderColor: 'rgb(0,0,0)',
            borderWidth: 0,  
          },
    ],
  };
// console.log('Data for NumCountStudInLern:', data);

const options = {

  onClick: handleBarClick,
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
        text: 'Количество студентов',
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

  },
  maintainAspectRatio: false, 
  layout: {
    padding: {
      left: 0,
      right: 0,
      top: 50,
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



return (<>

  <Bar ref={chartRef} data={data} options={options} />
  
  {/* {selectedLesson && <TableOfGroup teamId={teamId} selectedLesson={selectedLesson} />} */}

</>);
};


export default NumCountStudInLern;

