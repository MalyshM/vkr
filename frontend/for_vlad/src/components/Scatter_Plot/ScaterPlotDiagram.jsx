import React, { useEffect, useState } from 'react';
import Plot from 'react-plotly.js';
import { fetchWithTokenRefresh } from '../RefreshToken';
import {Heading,Select,Box,Flex} from '@chakra-ui/react';
import RequestCheckbox from '../ReportSystem/RequestCheckbox';

const ScatterPlotDiagram = ({ tokenUsers, type_group_by, teacher_list, speciality_list, team_list,CheckboxOne,CheckboxMany }) => {
  const [scatterPlotData, setScatterPlotData] = useState(null);
  const [selectedName, setSelectedName] = useState(null);
  const [requests, setRequests] = useState([]);

  const handleNameSelect = value => { // click on select for choose name of learn meeting
    setSelectedName(value);
  };

  useEffect(() => {
    const fetchScatterPlot = async () => {
      try {
        if (tokenUsers !== null) {
          if (type_group_by === 3) {
            type_group_by = 0;
          }

          const params = new URLSearchParams({
            token: tokenUsers,
            type_group_by,
            ...(teacher_list && { teacher_list: Array.isArray(teacher_list) ? teacher_list.join(',') : teacher_list }),
            ...(speciality_list && { speciality_list: Array.isArray(speciality_list) ? speciality_list.join(',') : speciality_list }),
            ...(team_list && { team_list: Array.isArray(team_list) ? team_list.join(',') : team_list })
          });

          const requestUrl = `http://moais-dashboard.ru:8082/api/stud_scatter_plot?${params.toString()}`;

          const response = await fetchWithTokenRefresh(requestUrl);
          const result = await response.json();
          setScatterPlotData(result);
        }
      } catch (error) {
        console.error('ScatterPlotData - Error fetching ScatterPlotData:', error);
      }
    };
    fetchScatterPlot();
  }, [tokenUsers, type_group_by, teacher_list, speciality_list, team_list]);


  // console.log('scatterPlotData after request - ', scatterPlotData)

  if (!scatterPlotData) {
    return <div>Loading...</div>;
  }

const uniqueNames = [...new Set(scatterPlotData.map(item => item.name))]; // Получение уникальных имен (названий) встреч
const filteredData = scatterPlotData.filter(item => item.name === selectedName); // Фильтрация данных по выбранному имени (названию) встречи

console.log('filteredData-',filteredData)

const data = [];
const dataArray = []; // Массив для хранения каждого result
const teamColors = {}; // Объект для хранения цветов команд
var trace2;

// Проходимся по отфильтрованным данным
filteredData.forEach((item, index) => {
  const teamId = item.team_id;
  const speciality = item.speciality;
  const teacher_id = item.teacher_id;
  let label = "";
  

  // Определение метки в зависимости от данных
  if (teamId) {
    label = `${teamId}`;
  } else if (speciality) {
    label = `${speciality}`;
  } else if (teacher_id) {
    label = `${teacher_id}`;
  }

  const key = `${label}`;

  // Генерация случайного цвета для команды, если он еще не был сгенерирован
  if (!(key in teamColors)) {
    teamColors[key] = `rgba(${Math.floor(Math.random() * 256)}, ${Math.floor(Math.random() * 256)}, ${Math.floor(Math.random() * 256)}, 1)`;
  }

  // Создание объекта трассировки
  const trace = {
    x: [],
    y: [],
    mode: 'markers',
    type: 'scatter',
    marker: {
      color: teamColors[key], // Цвет точек для каждой команды
      size: 10, 
    },
    name: label, // Имя трассировки
    customdata: [],
  };

  const lessonCounterValues = filteredData.map(item => item.lesson_counter);

  trace2 = {
    x: lessonCounterValues.map(() => 0),
    y: lessonCounterValues,
    mode: 'lines',
    line: {
      color: 'rgba(0, 0, 0, 0)', // Прозрачная линия, чтобы скрыть ее отображение на графике
    },  
    name: 'yaxis2 counter',
    yaxis: 'y2',
    // type: 'scatter',
  };
  
  

  // Добавление значений посещаемости и успеваемости из каждого студента в трассировку
  item.result1.forEach(student => {
    trace.x.push(student['Посещаемость']);
    trace.y.push(student['Успеваемость']);
    // trace.text.push(label); 
    // trace.customdata.push(student['stud_id']); 
  });
  data.push(trace);
  
  dataArray.push(trace); // Добавление трассировки в массив данных
});
// data.push(trace2);

  console.log('data',data)

const layoutMany = {
  width: 400, // Ширина окна
  height: 300, // Высота окна
  responsive: true,
  legend: {
    display: true,
    orientation: "h" 
  },
  title: {
    text: ``,
  },
  xaxis: {
    title: 'Посещаемость', 
  },
  yaxis: {
    title: 'Успеваемость (баллы)', 
  },
  hovermode: 'closest',
  hoverlabel: {
    namelength: -1,
  },
  hovertemplate: '%{text}<extra></extra>',
};

const layoutOne = {
  responsive: true,
  legend: {
    display: true,
    orientation: "h" 
  },
  title: {
    text: `Студенты`,
  },
  xaxis: {
    title: 'Посещаемость'
  },
  yaxis: {
    title: 'Успеваемость (баллы)', 
  },
  yaxis2: {
    title: 'Counter',
    // titlefont: {color: 'rgb(148, 103, 189, 0)'},
    // tickfont: {color: 'rgb(148, 103, 189,0)'},
    overlaying: 'y',
    side: 'right'
  },
  hovermode: 'closest',
  hoverlabel: {
    namelength: -1,
  },
  hovertemplate: `%{customdata}<extra></extra>`,

};
  const config = { displayModeBar: false };

  const params = new URLSearchParams({
    token: tokenUsers,
    type_group_by,
    ...(teacher_list && { teacher_list: Array.isArray(teacher_list) ? teacher_list.join(',') : teacher_list }),
    ...(speciality_list && { speciality_list: Array.isArray(speciality_list) ? speciality_list.join(',') : speciality_list }),
    ...(team_list && { team_list: Array.isArray(team_list) ? team_list.join(',') : team_list })
  });

  const requestUrl = `http://moais-dashboard.ru:8082/api/stud_scatter_plot?${params.toString()}`;




  const handleUpdateRequests = (updatedRequests) => {
    setRequests(updatedRequests);
  };



  return (
    <>
     
<Select
  ml={'auto'}
  mr={'auto'}
  mb={4}
  borderRadius="lg" 
  boxShadow="lg"
  width='270px'
  borderWidth={1}
  fontFamily='Trebuchet MS'
  placeholder="Выберите учебную встречу"
  borderColor='black'
  _active={{ borderColor: "black" }} 
  _hover={{ color: "blue" }}
  _selected={{ bg: "black.500", borderColor: "red.500", color: "white" }}
  onChange={(e) => handleNameSelect(e.target.value, e.target.selectedOptions[0].text)} // Changed from label to text
  value={selectedName}
>
  {Array.isArray(uniqueNames) && uniqueNames.length > 0 ? (
    uniqueNames.map((nameOfMeeting) => (
      <option key={nameOfMeeting} value={nameOfMeeting}>
        {nameOfMeeting}
      </option>
    ))
  ) : (
    <option disabled>data is not available</option> 
  )}
</Select>

<RequestCheckbox
        requestUrl={requestUrl}
        requestName="Диаграмма рассеяния по студентам"
        onUpdateRequests={handleUpdateRequests}
      />


      {CheckboxOne && (
        <Flex direction={'column'}>
          <Flex>
            <div style={{ width: '100%', height: '100%' }}>
              <Plot config={config} data={data} layout={layoutOne} style={{ width: '100%', height: '50%' }} />
            </div>
          </Flex>
        </Flex>
      )}

      {CheckboxMany && (
        <Flex direction={'column'}>
          <Flex mt={2} wrap={'wrap'} justifyContent={'center'}>
            {dataArray.map((trace, index) => (
              <div key={index} style={{ width: '400px', height: '300px' }}>
                <Plot config={config} data={[trace]} layout={{ ...layoutMany, title: { text: trace.name } }} style={{ width: '100%', height: '100%' }} />
              </div>
            ))}
          </Flex>
        </Flex>
      )}
    
  
</>
)}
export default ScatterPlotDiagram;