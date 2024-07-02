import React, { useEffect, useState } from 'react';
import Plot from 'react-plotly.js';
import { fetchWithTokenRefresh } from '../RefreshToken';
import RequestCheckbox from '../ReportSystem/RequestCheckbox';
import { Spin, Select, Layout, Typography,Col } from 'antd';

const { Option } = Select;
const { Title } = Typography;
const { Content } = Layout;

const ScatterPlotDiagram = ({ tokenUsers, type_group_by, teacher_list, speciality_list, team_list, CheckboxOne, CheckboxMany }) => {
  const [scatterPlotData, setScatterPlotData] = useState(null);
  const [selectedName, setSelectedName] = useState("Аттестация00");
  const [requests, setRequests] = useState([]);
  const [loading, setLoading] = useState(false); // state for spin

  const handleNameSelect = value => { // click on select for choose name of learn meeting
    setSelectedName(value);
  };

  useEffect(() => {
    setLoading(true);
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
      } finally {
        setLoading(false); // Устанавливаем состояние загрузки в false после завершения запроса
      }
    };
    fetchScatterPlot();
  }, [tokenUsers, type_group_by, teacher_list, speciality_list, team_list]);

  if (!scatterPlotData) {
    return <Spin spinning={loading} tip="Loading" size="large" style={{ position: 'absolute', top: '50%', left: '50%', transform: 'translate(-50%, -50%)', zIndex: 10 }} />;
  }

  const uniqueNames = [...new Set(scatterPlotData.map(item => item.name))]; // Получение уникальных имен (названий) встреч
  const filteredData = scatterPlotData.filter(item => item.name === selectedName); // Фильтрация данных по выбранному имени (названию) встречи

  console.log('filteredData-', filteredData)

  // Вычисляем количество команд и студентов
  const numTeams = filteredData.length;
  const numStudents = filteredData.reduce((total, currentItem) => total + currentItem.result1.length, 0);

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
      text: [],
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
    };

    // Добавление значений посещаемости и успеваемости из каждого студента в трассировку
    item.result1.forEach(student => {
      const fullName = student['stud_name'].split(' ');
      if (fullName.length >= 3) {
        const [lastName, firstName, middleName] = fullName;
        const initials = `${firstName[0]}. ${middleName[0]}.`;
        const shortName = `${lastName} ${initials}`;
    
        trace.x.push(student['Посещаемость']);
        trace.y.push(student['Успеваемость']);
        trace.customdata.push(shortName);
        trace.text.push(shortName);
      } else {
        trace.x.push(student['Посещаемость']);
        trace.y.push(student['Успеваемость']);
        trace.customdata.push(student['stud_name']);  // Или другой обработчик ошибки
        trace.text.push(student['stud_name']);       // Или другой обработчик ошибки
      }
    });
    
    data.push(trace);
    dataArray.push(trace); // Добавление трассировки в массив данных
  });

  console.log('data', data)


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
      // title: 'Посещаемость',
      // tickmode: 'array',
      // tickvals: scatterPlotData
      // .flatMap(item => item.result1.map(student => student['Посещаемость']))
      // .filter((value, index, self) => self.indexOf(value) === index && Number.isInteger(value)),
      // tickangle: 0, // Настройка угла меток оси X

      title: 'Посещаемость',
      
    tickmode: 'auto',
    nticks: 4, // Количество меток на оси X
    // tickangle: 0, // Настройка угла меток оси X
    tickformat: ',d', // Формат меток: только целые числа


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
      text: `Студенты: ${numStudents } (группы: ${numTeams})`,
    },
    xaxis: {
    title: {
      text: 'Посещаемость',
      standoff: 0,
    },
    side: 'top',
    tickmode: 'linear',
    nticks: scatterPlotData.length-1,  // Количество меток равно количеству элементов в данных
    
  },

    yaxis: {
      title: 'Успеваемость (баллы)',
    },
    yaxis2: {
      title: 'Counter',
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
    <Layout style={{ padding: '12px' }}>
      <Content >

        <Spin spinning={loading} tip="Loading" size="large" style={{ position: 'absolute', top: '50%', left: '50%', transform: 'translate(-50%, -50%)', zIndex: 10 }} />

        <div style={{ display: 'flex', justifyContent: 'center', align: "center"}}>
          <Col>
        <Select
          style={{ width: '270px', marginBottom: '16px', marginRight:"10px" }}
          placeholder="Выберите учебную встречу"
          onChange={handleNameSelect}
          value={selectedName}
        >
          {Array.isArray(uniqueNames) && uniqueNames.length > 0 ? (
            uniqueNames.map((nameOfMeeting) => (
              <Option key={nameOfMeeting} value={nameOfMeeting}>
                {nameOfMeeting.slice(0, -2)}
              </Option>
            ))
          ) : (
            <Option disabled>Данные недоступны</Option>
          )}
        </Select>

        <RequestCheckbox
          requestUrl={requestUrl}
          requestName="Диаграмма рассеяния по студентам"
          onUpdateRequests={handleUpdateRequests}
        />
        </Col>
        </div>

        {CheckboxOne && (
          <div style={{ width: '100%', height: '50%' }}>
          <Plot config={config} data={data} layout={layoutOne} style={{ width: '100%', height: '60%' }} />
        </div>
        )}

        {CheckboxMany && (

          <div style={{ display: 'flex', flexWrap: 'wrap', justifyContent: 'center', marginTop: '16px' }}>
            {dataArray.map((trace, index) => (

              <div key={index} style={{ width: '400px', height: '300px', margin: '8px' }}>
                <Plot config={config} data={[trace]} layout={{ ...layoutMany, title: { text: trace.name } }} style={{ width: '100%', height: '100%' }} />
              </div>

            ))}
          </div>

        )}
      </Content>
    </Layout>
  );
};

export default ScatterPlotDiagram;
