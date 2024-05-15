import React, { useEffect, useState } from 'react';
import Plot from 'react-plotly.js';
import { fetchWithTokenRefresh } from '../RefreshToken';
import {Heading,Select,Box,Flex} from '@chakra-ui/react';

const ScaterPlotBySection = ({ tokenUsers, type_group_by, teacher_list, speciality_list, team_list }) => {
  const [ScaterPlotBySectionData, setScatterPlotData] = useState(null);
  const [selectedName, setSelectedName] = useState(null);

  const handleNameSelect = value => { // click on select for choose name of learn meeting
    setSelectedName(value);
  };

  // console.log('test teacher_list - ', teacher_list)
  // console.log('test team_list - ', team_list)
  // console.log('test speciality_list - ', speciality_list)


  useEffect(() => {
    const fetchScaterPlotBySection = async () => {
      try {
        if (tokenUsers !== null) {
          if (type_group_by === 3) {
            type_group_by = 0;
          }
          const response = await fetchWithTokenRefresh(`http://moais-dashboard.ru:8082/api/scatter_plot_by_section?token=${tokenUsers}&type_group_by=${type_group_by}${teacher_list ? `&teacher_list=${Array.isArray(teacher_list) ? teacher_list.join(',') : teacher_list}` : ''}${speciality_list ? `&speciality_list=${Array.isArray(speciality_list) ? speciality_list.join(',') : speciality_list}` : ''}${team_list ? `&team_list=${Array.isArray(team_list) ? team_list.join(',') : team_list}` : ''}`);
          const result = await response.json();
          setScatterPlotData(result);
        }
      } catch (error) {
        console.error('ScaterPlotBySection - Error fetching ScaterPlotBySection:', error);
      }
    };
    fetchScaterPlotBySection();
  }, [tokenUsers, type_group_by, teacher_list, speciality_list, team_list]);

  if (!ScaterPlotBySectionData) {
    return <div>Loading...</div>;
  }

  const uniqueNames = [...new Set(ScaterPlotBySectionData.map(item => item.name))]; // get name of learn meeting (kr) from object's array

  const filteredData = ScaterPlotBySectionData.filter(item => item.name === selectedName);

  const teamColors = {};
  
  const data = filteredData.map(item => {
    const teamId = item.team_id;
    const speciality = item.speciality;
    const teacher_id = item.teacher_id;
    
    let label = "";
    
    if (teamId) {
      label = `${teamId}`;
    } else if (speciality) {
      label = `${speciality}`;
    } else if (teacher_id) {
      label = `${teacher_id}`;
    }
    
    const key = `${label}`;
    
    if (!(key in teamColors)) {
        teamColors[key] = `rgba(${Math.floor(Math.random() * 256)}, ${Math.floor(Math.random() * 256)}, ${Math.floor(Math.random() * 256)}, 1)`;
      }


      const xValue = item['Медианная_посещаемость'];
      const yValue = item['Медианная_успеваемость'];

      
    
    return {
      x: [xValue], // Создаем массив с одним элементом, чтобы хранить значение x для каждого объекта
      y: [yValue], 
      mode: 'markers',
      type: 'scatter',
      marker: {
        color: teamColors[key],
        size: 10,
      },
      name: label,
    };
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
      text: 'Группы',
    },
    xaxis: {
      title: 'Медианная успеваемость', 
    },
    yaxis: {
      title: 'Медианная посещаемость',
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
  ml={'auto'}
  mr={'auto'}
  mb={4}
  borderRadius="lg" 
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


  <Flex direction={'column'}>
    <Flex ml={'auto'} mr={'auto'}>
      <div style={{ width: '100%', height: '100vh' }}>
        <Plot config={config} data={data} layout={layout} style={{ width: '100%', height: '100%' }} />
      </div>
    </Flex>
  </Flex>


    </>
  );
};

export default ScaterPlotBySection;