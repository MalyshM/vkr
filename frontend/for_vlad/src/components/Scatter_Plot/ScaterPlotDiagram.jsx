import React, { useEffect, useState } from 'react';
import Plot from 'react-plotly.js';
import { fetchWithTokenRefresh } from '../RefreshToken';

const ScatterPlotDiagram = ({ tokenUsers, type_group_by, teacher_list, speciality_list, team_list }) => {
  const [scatterPlotData, setScatterPlotData] = useState(null);
  const [selectedName, setSelectedName] = useState(null);

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

  if (!scatterPlotData) {
    return <div>Loading...</div>;
  }

  const uniqueNames = [...new Set(scatterPlotData.map(item => item.name))];

  const handleNameSelect = event => {
    setSelectedName(event.target.value);
  };

  const filteredData = scatterPlotData.filter(item => item.name === selectedName);

  const data = [];
  const teamColors = {};

  filteredData.forEach((item, index) => {
    const teamId = item.team_id;
    if (!(teamId in teamColors)) {
      teamColors[teamId] = `rgba(${Math.floor(Math.random() * 256)}, ${Math.floor(Math.random() * 256)}, ${Math.floor(Math.random() * 256)}, 1)`;
    }

    const trace = {
      x: [],
      y: [],
      mode: 'markers',
      type: 'scatter',
      marker: {
        color: teamColors[teamId],
      },
      name: `Team ${teamId}`,
    };

    item.result1.forEach(student => {
      trace.x.push(student['Посещаемость']);
      trace.y.push(student['Успеваемость']);
    });

    data.push(trace);
  });

  const layout = {
    responsive: true,
    legend: {
      display: true,
    },
    title: {
      text: 'Scatter Chart',
    },
    hovermode: 'closest',
    hoverlabel: {
      namelength: -1,
    },
    hovertemplate: '%{text}<extra></extra>',
  };

  return (
    <>
      <div>
        <label htmlFor="nameSelect">Select Name:</label>
        <select id="nameSelect" value={selectedName} onChange={handleNameSelect}>
          <option value="">All Names</option>
          {uniqueNames.map(name => (
            <option key={name} value={name}>
              {name}
            </option>
          ))}
        </select>
      </div>
      <Plot data={data} layout={layout} />
    </>
  );
};

export default ScatterPlotDiagram;