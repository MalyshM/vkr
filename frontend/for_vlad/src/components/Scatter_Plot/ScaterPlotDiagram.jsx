import React, { useEffect, useState } from 'react';
import Plot from 'react-plotly.js';
import { fetchWithTokenRefresh } from '../RefreshToken';
import {Heading,Select,Box,Flex} from '@chakra-ui/react';

const ScatterPlotDiagram = ({ tokenUsers, type_group_by, teacher_list, speciality_list, team_list }) => {
  const [scatterPlotData, setScatterPlotData] = useState(null);
  const [selectedName, setSelectedName] = useState(null);

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
          const response = await fetchWithTokenRefresh(`http://moais-dashboard.ru:8082/api/stud_scatter_plot?token=${tokenUsers}&type_group_by=${type_group_by}${teacher_list ? `&teacher_list=${Array.isArray(teacher_list) ? teacher_list.join(',') : teacher_list}` : ''}${speciality_list ? `&speciality_list=${Array.isArray(speciality_list) ? speciality_list.join(',') : speciality_list}` : ''}${team_list ? `&team_list=${Array.isArray(team_list) ? team_list.join(',') : team_list}` : ''}`);
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

  const uniqueNames = [...new Set(scatterPlotData.map(item => item.name))]; // get name of learn meeting (kr) from object's array

  const filteredData = scatterPlotData.filter(item => item.name === selectedName);

  // console.log('filteredData - ', filteredData)


  const data = [];
  const teamColors = {};

  filteredData.forEach((item, index) => {
    const teamId = item.team_id;
    const speciality = item.speciality;
    const teacher_id
    = item.teacher_id;

    let label = ""; 

    if (teamId) {
      label = `Team ${teamId}`;
    } else if (speciality) {
      label = `${speciality}`;
    } else if (teacher_id
    ) {
      label = `Teacher ${teacher_id
      }`;
    }

    const key = `${label}`;   

    if (!(key in teamColors)) {
      teamColors[key] = `rgba(${Math.floor(Math.random() * 256)}, ${Math.floor(Math.random() * 256)}, ${Math.floor(Math.random() * 256)}, 1)`;
    }

    const trace = {
      x: [],
      y: [],
      mode: 'markers',
      type: 'scatter',
      marker: {
        color: teamColors[key],
        size: 10,
      },
      name: label,
    };

    item.result1.forEach(student => {
      trace.x.push(student['Посещаемость']);
      trace.y.push(student['Успеваемость']);
    });

    data.push(trace);
  });

  const layout = {
    width: 890, // Ширина окна
    height: 730, // Высота окна
    responsive: true,
    legend: {
      display: true,
      orientation: "h" 

    },
    title: {
      text: 'Студенты',
    },
    xaxis: {
      title: 'Посещаемость', 
    },
    xaxis2: {
      title: 'Вторая ось X',
      overlaying: 'x',
      // side: 'top',
    },

    yaxis: {
      title: 'Успеваемость',
    },
    hovermode: 'closest',
    hoverlabel: {
      namelength: -1,
    },
    hovertemplate: '%{text}<extra></extra>',
  };

  const config = {
    displayModeBar: false
  };
  
  return (
    <>
     
<Select
  borderRadius="lg" 
  boxShadow="lg"
  mr={4}
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


            <div style={{ width: '100%', height: '100vh' }}>
                <Plot config={config} data={data} layout={layout} style={{ width: '100%', height: '100%' }} />
            </div>

    </>
  );
};

export default ScatterPlotDiagram;