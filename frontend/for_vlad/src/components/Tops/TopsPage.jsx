import React, { useState, useEffect } from 'react';
import { Select, Table, Typography, Cascader, Spin,Button} from 'antd';
import { useAuth } from '../useAuth';
import {fetchWithTokenRefresh} from '../RefreshToken'
import { useNavigate } from 'react-router-dom';

import { saveAs } from 'file-saver';
import * as XLSX from 'xlsx';

const { Option } = Select;
const { Title } = Typography;

const TopPage = () => {
  const { userToken } = useAuth();
  const navigate = useNavigate();

  const [isGroupBy, setIsGroupBy] = useState(null);
  const [isByMark, setIsByMark] = useState(null);
  const [typeGroupBy, setTypeGroupBy] = useState(null);

  const [TeacherData, SetTeacherData] = useState(null);
  const [SelectedTeacher, setSelectedTeacher] = useState([]);

  const [SpecialityData, SetSpecialityData] = useState(null);
  const [SelectedSpeciality, setSelectedSpeciality] = useState([]);

  const [TeamData, SetTeamData] = useState(null);
  const [SelectedTeam, setSelectedTeam] = useState([]);

  const [Top_10_most_and_least, setTop_10_most_and_least] = useState([])
  
  const [students, setStudents] = useState([]);

  const [uniqueKRNames, setUniqueKRNames] = useState([]);
  const [selectedKR, setSelectedKR] = useState(null);
  const [filteredData, setFilteredData] = useState([]); 

  const [options_, setOptions] = useState([]);

  const [loading, setLoading] = useState(false); // Состояние загрузки
  const [data, setData] = useState([]); // Данные для Select
  const [selectedGroupBy, setSelectedGroupBy] = useState(null);

  const [studentsBest, setStudentsBest] = useState(null)
  const [studentsLeast, setStudentsLeast] = useState(null)

  const [teacherName, setTeacherName] = useState(null)

  const fetch_Top_10_most_and_least = async () => {
    setLoading(true);
    try {
      const params = new URLSearchParams({
        token: userToken,
        is_by_mark: isByMark,
        is_group_by: isGroupBy,
      });
  
      if (isGroupBy === true && typeGroupBy !== null) {
        params.append('type_group_by', typeGroupBy);
      }
      if (SelectedTeacher && SelectedTeacher.length > 0) {
        params.append('teacher_list', SelectedTeacher.join(','));
      }
      if (SelectedSpeciality && SelectedSpeciality.length > 0) {
        params.append('speciality_list', SelectedSpeciality.join(','));
      }
      if (SelectedTeam && SelectedTeam.length > 0) {
        params.append('team_list', SelectedTeam.join(','));
      }
      
      console.log('Request URL:', `http://moais-dashboard.ru:8082/api/top_10_most_and_least_studs?${params.toString()}`);
  
      const response = await fetchWithTokenRefresh(`http://moais-dashboard.ru:8082/api/top_10_most_and_least_studs?${params.toString()}`);
  
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const data = await response.json();
      setData(data); 
      setTop_10_most_and_least(data);    
      setFilteredData(data);

    } catch (error) {
      console.error('Error fetching data:', error);
    } finally {
      setLoading(false); // Устанавливаем состояние загрузки в false после завершения запроса
    }

  };

  useEffect(() => { //request get students table
    fetch_Top_10_most_and_least();
  }, [isGroupBy, isByMark, typeGroupBy, TeacherData, SpecialityData, TeamData]);


  useEffect(() => { // condition for show kr name
    if (Top_10_most_and_least && Top_10_most_and_least.length > 0) {
      const names = Top_10_most_and_least.map(item => item.name);
      const uniqueNames = [...new Set(names)];
      setUniqueKRNames(uniqueNames);
    }
  }, [Top_10_most_and_least]);


  useEffect(() => {
    if (selectedKR) {
        const filtered = Top_10_most_and_least.filter(item => item.name === selectedKR);
        setFilteredData(filtered);
        setOptions(createGroupByOptions(filtered, typeGroupBy));

        if (isGroupBy) {
            if (selectedGroupBy && selectedGroupBy.length > 0) {
                const [id, subType] = selectedGroupBy;
                const selectedItem = filtered.find(item =>
                    item.team_id === id || item.speciality === id || item.teacher_id === id
                );

                if (selectedItem) {
                    setStudentsBest(selectedItem.top_10_best.map(student => ({
                        ...student,
                        team_id: selectedItem.team_id,
                        team_name: selectedItem.team_name
                    })));
                    setStudentsLeast(selectedItem.top_10_least.map(student => ({
                        ...student,
                        team_id: selectedItem.team_id,
                        team_name: selectedItem.team_name
                    })));
                } else {
                    setStudentsBest([]);
                    setStudentsLeast([]);
                }
            } 
        } else {
            const bestStudents = filtered.flatMap(item =>
                item.top_10_best.map(student => ({
                    ...student,
                    team_id: item.team_id,
                    team_name: item.team_name
                }))
            );
            const leastStudents = filtered.flatMap(item =>
                item.top_10_least.map(student => ({
                    ...student,
                    team_id: item.team_id,
                    team_name: item.team_name
                }))
            );
            setStudentsBest(bestStudents);
            setStudentsLeast(leastStudents);
        }
    } else {
        setFilteredData(Top_10_most_and_least);
        setStudentsBest([]);
        setStudentsLeast([]);
    }
}, [selectedKR, Top_10_most_and_least, typeGroupBy, isGroupBy, selectedGroupBy]);


  

  const exportToExcel = (bestData, leastData, allData, filename) => {
    const workbook = XLSX.utils.book_new();

    if (allData.length > 0) {
      const allDataWorksheet = XLSX.utils.json_to_sheet(allData);
      XLSX.utils.book_append_sheet(workbook, allDataWorksheet, 'All Students');
    } else {
      const bestWorksheet = XLSX.utils.json_to_sheet(bestData);
      const leastWorksheet = XLSX.utils.json_to_sheet(leastData);
      XLSX.utils.book_append_sheet(workbook, bestWorksheet, 'Best Students');
      XLSX.utils.book_append_sheet(workbook, leastWorksheet, 'Least Students');
    }

    const excelBuffer = XLSX.write(workbook, { bookType: 'xlsx', type: 'array' });
    const blob = new Blob([excelBuffer], { type: 'application/octet-stream' });
    saveAs(blob, `${filename}.xlsx`);
  };


  
  const handleDownload = () => {
    if (isGroupBy) {
      exportToExcel(studentsBest, studentsLeast, [], 'Данные по студентам');
    } else {
      exportToExcel([], [], filteredData, 'Данные по студентам');
    }
  };

  
  const handleGroupByChange = (value) => {
    setSelectedGroupBy(value); 
    if (!value) {
      setStudentsBest([]);
      setStudentsLeast([]);
      return;
    }
  
    const selectedItem = filteredData.find(item => 
      item.team_id === value || item.speciality === value || item.teacher_id === value
    );
    
    if (selectedItem) {
      // Добавляем teacher_name к top_10_best и top_10_least
      const studentsBestWithTeacher = selectedItem.top_10_best.map(student => ({
        ...student,
        teacher_name: selectedItem.teacher_name
      }));
      const studentsLeastWithTeacher = selectedItem.top_10_least.map(student => ({
        ...student,
        teacher_name: selectedItem.teacher_name
      }));
  
      setStudentsBest(studentsBestWithTeacher);
      setStudentsLeast(studentsLeastWithTeacher);
    } else {
      setStudentsBest([]);
      setStudentsLeast([]);
    }
    
  };
  
  const handleKRChange = (value) => {
    setSelectedKR(value);
  };
  
  const handleKRClear = () => {
    setSelectedKR(null);
    setStudentsBest([]);
    setStudentsLeast([]);
    setFilteredData(Top_10_most_and_least); 
    setOptions(createGroupByOptions(Top_10_most_and_least, typeGroupBy));
  };
  

  const createGroupByOptions = (data, typeGroupBy) => {
    if (typeGroupBy === 0) { // По командам
      return data
        .filter(item => item.team_id)
        .map(item => ({
          value: item.team_id,
          label: item.team_name,
        }));
    } else if (typeGroupBy === 1) { // По направлениям
      return data
        .filter(item => item.speciality)
        .map(item => ({
          value: item.speciality,
          label: item.speciality,
        }));
    } else if (typeGroupBy === 2) { // По преподавателям
      return data
        .filter(item => item.teacher_id)
        .map(item => ({
          value: item.teacher_id,
          label: item.teacher_name,
        }));
    }
    return [];
  };  
  
  
  console.log('Top_10_most_and_least',Top_10_most_and_least)
  // console.log('token', userToken)
  console.log('filteredData',filteredData)
  console.log('studentsLeast',studentsLeast)
  console.log('studentsBest',studentsBest)
  

  const columnsForFiltr = [
    { title: 'ID Студента', dataIndex: 'stud_id', key: 'stud_id',
    render: (text, record) => (
      <a
          onClick={() => navigate(`/student/${record.stud_id}/${record.team_id}/${encodeURIComponent(record.team_name)}`)}
      >
        {text}
      </a>
    ),
  },
    { title: 'Успеваемость (баллы)', dataIndex: 'Успеваемость', key: 'marks' },
    { title: 'Посещаемость (макс 22)', dataIndex: 'Посещаемость', key: 'attendance' },
    { title: 'Контрольная точка', dataIndex: 'name', key: 'name' },
    { title: 'Количество занятий', dataIndex: 'lesson_counter', key: 'lesson_counter' },
  ];

  const columnsForStudents = [
    { title: 'ID Студента', dataIndex: 'stud_id', key: 'stud_id',
    render: (text, record) => (
      <a
        onClick={() => navigate(`/student/${record.stud_id}/${record.team_id}/${encodeURIComponent(record.team_name)}`)}
      >
        {text}
      </a>
    ),
     },
    { title: 'Успеваемость (баллы)', dataIndex: 'Успеваемость', key: 'marks' },
    { title: 'Посещаемость (макс 22)', dataIndex: 'Посещаемость', key: 'attendance' },
  ];

  const columnsForStudentsWithTeacher = [
    ...columnsForStudents,
    { title: 'Преподаватель', dataIndex: 'teacher_name', key: 'teacher_name' }, // Add teacher_name column
  ];
  

  return (
    <>
     <div style={{ position: 'relative', minHeight: '100px' }}> 
     {/* Контейнер с position: relative */}
      <Spin 
        spinning={loading} 
        tip="Загрузка..." 
        style={{ 
          position: 'absolute', 
          top: '8%', 
          left: '50%', 
          transform: 'translate(-50%, -50%)', 
          zIndex: 10 
        }} 
      />

<div>
        <div style={{ display: 'flex', justifyContent: 'space-around', alignItems: 'center', margin: '10px 0' }}>
          <Title level={2} style={{ margin: 0 }}>Топ учеников</Title>

          <Select
            style={{ width: 200 }}
            placeholder="Группировать? *"
            value={isGroupBy}
            onChange={value => setIsGroupBy(value)}
          >
            <Option value={true}>С группировкой</Option>
            <Option value={false}>Без группировки</Option>
          </Select>

          <Select
            style={{ width: 200 }}
            placeholder="Сортировать по *"
            value={isByMark}
            onChange={value => setIsByMark(value)}
          >
            <Option value={true}>Успеваемость</Option>
            <Option value={false}>Посещаемость</Option>
          </Select>

          {isGroupBy && (
            <Select
              style={{ width: 200 }}
              placeholder="Тип группировки *"
              value={typeGroupBy}
              onChange={value => setTypeGroupBy(value)}
            >
              <Option value={0}>По командам</Option>
              <Option value={1}>По направлениям</Option>
              <Option value={2}>По преподавателям</Option>
            </Select>
          )}

          <Select
            style={{ width: 200 }}
            placeholder="Контрольная точка *"
            value={selectedKR}
            onChange={handleKRChange}
            onClear={handleKRClear}
            allowClear
          >
            {uniqueKRNames.map(name => (
              <Option key={name} value={name}>
                {name}
              </Option>
            ))}
          </Select>

          {isGroupBy && (
            <Select
              style={{ width: 300 }}
              options={options_}
              onChange={handleGroupByChange}
              placeholder="Группа/направление/преподаватель"
              allowClear
            />
          )}
          <Button style={{background: "green", color: "white"}} onClick={handleDownload}>Скачать данные</Button>
        </div>

        {isGroupBy ? (
          <div style={{ display: 'flex', justifyContent: 'center', gap: '20px', marginTop: 20 }}>
            <Table
              dataSource={studentsBest}
              columns={typeGroupBy === 0 ? columnsForStudentsWithTeacher : columnsForStudents}
              rowKey="stud_id"
              title={() => 'Топ 10 преуспевающих'}
            />
            <Table
              dataSource={studentsLeast}
              columns={typeGroupBy === 0 ? columnsForStudentsWithTeacher : columnsForStudents}
              rowKey="stud_id"
              title={() => 'Топ 10 отстающих'}
            />
          </div>
        ) : (
          <div style={{ display: 'flex', justifyContent: 'space-around', gap: '20px', marginTop: 20 }}>
            <Table
              dataSource={filteredData.slice(0, Math.ceil(filteredData.length / 2))}
              columns={columnsForFiltr}
              rowKey="stud_id"
              title={() => 'Отстающие'}
            />
            <Table
              dataSource={filteredData.slice(Math.ceil(filteredData.length / 2))}
              columns={columnsForFiltr}
              rowKey="stud_id"
              title={() => 'Преуспевающие'}
/>
          </div>
        )}
      </div>
    </div>
  </>
)}

export default TopPage;


      {/* <Select
        mode="multiple"
        style={{ width: 200, marginLeft: 10 }}
        placeholder="Выберите преподавателей"
        value={TeacherData}
        onChange={value => SetTeacherData(value)}
      >
        <Option value="teacher1">Преподаватель 1</Option>
        <Option value="teacher2">Преподаватель 2</Option>
      </Select>
      
      <Select
        mode="multiple"
        style={{ width: 200, marginLeft: 10 }}
        placeholder="Выберите направления"
        value={SpecialityData}
        onChange={value => SetSpecialityData(value)}
      >
        <Option value="speciality1">Направление 1</Option>
        <Option value="speciality2">Направление 2</Option>
      </Select>

      <Select
        mode="multiple"
        style={{ width: 200, marginLeft: 10 }}
        placeholder="Выберите группы"
        value={TeamData}
        onChange={value => SetTeamData(value)}
      >
        <Option value="team1">Группа 1</Option>
        <Option value="team2">Группа 2</Option>
      </Select> */}

     
