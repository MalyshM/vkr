import React, { useEffect, useState } from 'react';
import Plot from 'react-plotly.js';
import { fetchWithTokenRefresh } from '../RefreshToken';
import {Spin, Select, Row, Col,Layout } from 'antd';
import RequestCheckbox from '../ReportSystem/RequestCheckbox';

const { Option } = Select;
const { Content } = Layout;

const ScaterPlotBySection = ({ tokenUsers, type_group_by, teacher_list, speciality_list, team_list }) => {
  const [ScaterPlotBySectionData, setScatterPlotData] = useState(null);
  const [selectedName, setSelectedName] = useState("Аттестация00");
  const [requests, setRequests] = useState([]);
  const [loading, setLoading] = useState(false); // state for spin

  const handleNameSelect = value => {
    setSelectedName(value);
  };

  useEffect(() => {
    setLoading(true);
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
      }finally {
        setLoading(false); // Устанавливаем состояние загрузки в false после завершения запроса
      }
    };
    fetchScaterPlotBySection();
  }, [tokenUsers, type_group_by, teacher_list, speciality_list, team_list]);

  if (!ScaterPlotBySectionData) {
    return <Spin spinning={loading} tip="Loading" size="large" style={{ position: 'absolute', top: '50%', left: '50%', transform: 'translate(-50%, -50%)', zIndex: 10 }} />;
  }

  const uniqueNames = [...new Set(ScaterPlotBySectionData.map(item => item.name))];
  const filteredData = ScaterPlotBySectionData.filter(item => item.name === selectedName);

  const numTeams = filteredData.length;

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
      text: type_group_by === 3 ? `Группы: ${numTeams}` :
          type_group_by === 1 ? `Направления: ${numTeams}` :
          type_group_by === 2 ? `Преподаватели: ${numTeams}` :
          '',
    },
    xaxis: {
      title: {
        text: 'Медианная посещаемость',
        standoff: 0,
      },
      side: 'top',
      tickmode: 'linear',
      nticks: ScaterPlotBySectionData.length-1,
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
      <Layout style={{ padding: '12px' }}>
        <Content>
        <div style={{ display: 'flex', justifyContent: 'center', width: '100%' }}>
          <div>

          <div style={{ display: 'flex', justifyContent: 'center', align: "center"}}>
            <Col>
          <Select
            style={{ width: '270px', marginBottom: '16px', marginRight:"10px" }}
            placeholder="Выберите учебную встречу"
            onChange={(value) => handleNameSelect(value)}
            value={selectedName}
            
          >
            {Array.isArray(uniqueNames) && uniqueNames.length > 0 ? (
              uniqueNames.map((nameOfMeeting) => (
                <Option key={nameOfMeeting} value={nameOfMeeting}>
                  {nameOfMeeting.slice(0, -2)}
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
          </Col>
          </div>
  
            <Plot config={config} data={data} layout={layout} style={{ width: '100%', height: '100%' }} />
          </div>
        </div>

        </Content>
      </Layout>
    </>
  );
  
};


export default ScaterPlotBySection;
