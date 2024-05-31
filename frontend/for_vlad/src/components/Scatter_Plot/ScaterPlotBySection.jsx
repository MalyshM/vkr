import React, { useEffect, useState } from 'react';
import Plot from 'react-plotly.js';
import { fetchWithTokenRefresh } from '../RefreshToken';
import { Select, Row, Col } from 'antd';
import RequestCheckbox from '../ReportSystem/RequestCheckbox';

const { Option } = Select;

const ScaterPlotBySection = ({ tokenUsers, type_group_by, teacher_list, speciality_list, team_list }) => {
  const [ScaterPlotBySectionData, setScatterPlotData] = useState(null);
  const [selectedName, setSelectedName] = useState(null);
  const [requests, setRequests] = useState([]);

  const handleNameSelect = value => {
    setSelectedName(value);
  };

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

  const uniqueNames = [...new Set(ScaterPlotBySectionData.map(item => item.name))];
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
      x: [xValue],
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
    width: 890,
    height: 730,
    responsive: true,
    legend: {
      display: true,
      orientation: "h"
    },
    title: {
      text: 'Группы',
    },
    xaxis: {
      title: 'Медианная посещаемость',
    },
    yaxis: {
      title: 'Медианная успеваемость',
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

  const requestUrl = `http://moais-dashboard.ru:8082/api/scatter_plot_by_section?token=${tokenUsers}&type_group_by=${type_group_by}${teacher_list ? `&teacher_list=${Array.isArray(teacher_list) ? teacher_list.join(',') : teacher_list}` : ''}${speciality_list ? `&speciality_list=${Array.isArray(speciality_list) ? speciality_list.join(',') : speciality_list}` : ''}${team_list ? `&team_list=${Array.isArray(team_list) ? team_list.join(',') : team_list}` : ''}`;

  const handleUpdateRequests = (updatedRequests) => {
    setRequests(updatedRequests);
  };

  return (
    <>
      <Select
        style={{ width: '270px', marginBottom: '16px' }}
        placeholder="Выберите учебную встречу"
        onChange={(value) => handleNameSelect(value)}
        value={selectedName}
      >
        {Array.isArray(uniqueNames) && uniqueNames.length > 0 ? (
          uniqueNames.map((nameOfMeeting) => (
            <Option key={nameOfMeeting} value={nameOfMeeting}>
              {nameOfMeeting}
            </Option>
          ))
        ) : (
          <Option disabled>Данные не доступны</Option>
        )}
      </Select>

      <RequestCheckbox
        requestUrl={requestUrl}
        requestName="Диаграмма рассеяния по группам"
        onUpdateRequests={handleUpdateRequests}
      />

      <Row justify="center">
        <Col span={24}>
          <div style={{ width: '100%', height: '100vh' }}>
            <Plot config={config} data={data} layout={layout} style={{ width: '100%', height: '100%' }} />
          </div>
        </Col>
      </Row>
    </>
  );
};

export default ScaterPlotBySection;
