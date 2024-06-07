import React, { useState, useEffect,useRef } from 'react';
import { Select, Table, Typography, Cascader, Spin,Button} from 'antd';
import { useAuth } from '../useAuth';
import {fetchWithTokenRefresh} from '../RefreshToken'
import { useNavigate } from 'react-router-dom';
import { Tooltip } from 'antd';
import RequestCheckbox from '../ReportSystem/RequestCheckbox';

const { Option } = Select;
const { Title } = Typography;

const TopPage = () => {

  const [requests, setRequests] = useState([]);

  const { userToken } = useAuth();
  const navigate = useNavigate();
  const fetchTimer = useRef(null);

  const [isGroupBy, setIsGroupBy] = useState(true);
  const [isByMark, setIsByMark] = useState(true);
  const [typeGroupBy, setTypeGroupBy] = useState(0);

  const [TeacherData, SetTeacherData] = useState(null);
  const [SelectedTeacher, setSelectedTeacher] = useState([]);

  const [SpecialityData, SetSpecialityData] = useState(null);
  const [SelectedSpeciality, setSelectedSpeciality] = useState([]);

  const [TeamData, SetTeamData] = useState(null);
  const [SelectedTeam, setSelectedTeam] = useState([]);

  const [Top_10_most_and_least, setTop_10_most_and_least] = useState([])
  
  const [uniqueKRNames, setUniqueKRNames] = useState([]);
  const [selectedKR, setSelectedKR] = useState("Аттестация00");
  const [filteredData, setFilteredData] = useState([]); 

  const [options_, setOptions] = useState([]);

  const [loading, setLoading] = useState(false); // Состояние загрузки
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
  
      if (isGroupBy === true) {
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
      
  
      const response = await fetchWithTokenRefresh(`http://moais-dashboard.ru:8082/api/top_10_most_and_least_studs?${params.toString()}`);
  
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const data = await response.json();
       
      setTop_10_most_and_least(data);    
      // setFilteredData(data);

      const updatedTop10 = data.map(group => {
        const updatedTop10best = (group.top_10_best || []).map(item => ({
            ...item,
            name: group.name,
            teacher_name: group.teacher_name,
            team_name: group.team_name,
            lesson_counter: group.lesson_counter,
            speciality: group.speciality,

        }));
        const updatedTop10least = (group.top_10_least || []).map(item => ({
          ...item,
          name: group.name,
          teacher_name: group.teacher_name,
          team_name: group.team_name,
          lesson_counter: group.lesson_counter,
          speciality: group.speciality,
      }));
        return {
            ...group,
            top_10_best: updatedTop10best,
            top_10_least: updatedTop10least,
        };
        
    });
    

    if (selectedKR) {
      setStudentsBest(updatedTop10.filter(item => item.name === selectedKR));
      setStudentsLeast(updatedTop10.filter(item => item.name === selectedKR));
  } else {
      setStudentsBest(updatedTop10);
      setStudentsLeast(updatedTop10);
  }

    } catch (error) {
      console.error('Error fetching data:', error);
    } finally {
      setLoading(false); // Устанавливаем состояние загрузки в false после завершения запроса
    }
    console.log('Top_10_most_and_least',Top_10_most_and_least)

  };
  console.log("studentsBest", studentsBest)
  console.log("studentsLeast", studentsLeast)

  const fetchTeam = async () => {
    try {
        const response = await fetchWithTokenRefresh(`http://moais-dashboard.ru:8082/api/get_teams_for_user_without_lect?token=${userToken}`);
        const result = await response.json();
        SetTeamData(result);
      console.log('fetchTeamForTeacher:', result);
    } catch (error) {
        console.error('Error fetching data from fetchTeamForTeacher:', error);
    }
    };

    const fetchTeacher = async () => {
        try {
          const response = await fetchWithTokenRefresh(`http://moais-dashboard.ru:8082/api/get_all_teachers_unique?token=${userToken}`);
          const result = await response.json();
          SetTeacherData(result);
          console.log('fetchTeacher:', result);
      } catch (error) {
          console.error('Error fetching data from fetchTeacher:', error);
        }
      };

      const fetchSpeciality = async () => {
        try {
          const response = await fetchWithTokenRefresh(`http://moais-dashboard.ru:8082/api/get_all_specialities?token=${userToken}`);
          const result = await response.json();
          SetSpecialityData(result);
          console.log('fetchSpecialityForTeacher:', result);
      } catch (error) {
          console.error('Error fetching data from fetchSpecialityForTeacher:', error);
        }
      };

  useEffect(() => { //request get students table
    if (userToken && isGroupBy){
    fetch_Top_10_most_and_least();}
  }, [isGroupBy, isByMark, typeGroupBy, SelectedTeacher, SelectedSpeciality, SelectedTeam, selectedKR]);

  useEffect(() => {
    const fetchData = async () => {
        fetchTeam();
        fetchTeacher();
        fetchSpeciality();
    }
if (userToken) {fetchData();} }, [userToken]);


  useEffect(() => { // limit requests
    if (userToken) {
        if (fetchTimer.current) {
            clearTimeout(fetchTimer.current);
        }
        fetchTimer.current = setTimeout(fetch_Top_10_most_and_least, 1000); // Limit requests to once per second
    }
    return () => clearTimeout(fetchTimer.current); // Cleanup on unmount or dependency change
}, [isGroupBy, isByMark, typeGroupBy, SelectedTeacher, SelectedSpeciality, SelectedTeam, userToken]);


  useEffect(() => { // condition for show kr name
    if (Top_10_most_and_least && Top_10_most_and_least.length > 0) {
      const names = Top_10_most_and_least.map(item => item.name);
      const uniqueNames = [...new Set(names)];
      setUniqueKRNames(uniqueNames);
      console.log('uniqueKRNames',uniqueKRNames)
    }
  }, [Top_10_most_and_least]);


  useEffect(() => { // condition for update table - if changes KR
    if (selectedKR) {
        setFilteredData(Top_10_most_and_least.filter(item => item.name === selectedKR));
    } else {
        setFilteredData(Top_10_most_and_least);
    }
    console.log('UPDATE TABLE - CJOISE OTHER KR')
    console.log('FilteredData',filteredData)
}, [selectedKR, Top_10_most_and_least]);


useEffect(() => {
  if (Top_10_most_and_least && Top_10_most_and_least.length > 0) {
    const options = createGroupByOptions(Top_10_most_and_least, typeGroupBy);
    setOptions(options);
  }
}, [Top_10_most_and_least, typeGroupBy]);


  const handleChangeTeam = (value) => {
    const teamValues = Array.isArray(value) ? value.map(v => v.toString()) : [value.toString()];
    setSelectedTeam(teamValues);
  };

  const handleChangeTeacher = (value) => {
    const teacherValues = Array.isArray(value) ? value.map(v => v.toString()) : [value.toString()];
    setSelectedTeacher(teacherValues);
};

const handleChangeSpeciality = (value) => {
    const specialityValues = Array.isArray(value) ? value.map(v => v.toString()) : [value.toString()];
    setSelectedSpeciality(specialityValues);
};
  
 
  const handleKRChange = (value) => { // condition - 
    setSelectedKR(value);
    if (value) {
      setFilteredData(Top_10_most_and_least.filter(item => item.name === value));
    } else {
      setFilteredData(Top_10_most_and_least);
    }
    console.log('CHANGES KR')
  };

 
  const createGroupByOptions = (data, typeGroupBy) => {
    const uniqueSet = new Set();
    if (typeGroupBy === 0) { // По командам
      return data
        .filter(item => item.team_id)
        .map(item => ({
          value: item.team_id,
          label: item.team_name,
        }))
        .filter(option => {
          if (uniqueSet.has(option.value)) return false;
          uniqueSet.add(option.value);
          return true;
        });
    } else if (typeGroupBy === 1) { // По направлениям
      return data
        .filter(item => item.speciality)
        .map(item => ({
          value: item.speciality,
          label: item.speciality,
        }))
        .filter(option => {
          if (uniqueSet.has(option.value)) return false;
          uniqueSet.add(option.value);
          return true;
        });
    } else if (typeGroupBy === 2) { // По преподавателям
      return data
        .filter(item => item.teacher_id)
        .map(item => ({
          value: item.teacher_id,
          label: item.teacher_name,
        }))
        .filter(option => {
          if (uniqueSet.has(option.value)) return false;
          uniqueSet.add(option.value);
          return true;
        });
    }
    return [];
  };
  

  const columnsForFiltr = [
    { title: 'ID Студента', dataIndex: 'stud_id', key: 'stud_id',
    render: (text, record) => (
      <a
          onClick={() => navigate(`/student/${record.stud_id}`)}
      >
        {text}
      </a>
    ),
  },
    { title: 'Успеваемость (баллы)', dataIndex: 'Успеваемость', key: 'marks' },
    { title: 'Посещаемость (макс 22)', dataIndex: 'Посещаемость', key: 'attendance' },
    ...(selectedKR === null ? [
      { title: 'Контрольная точка', dataIndex: 'name', key: 'name' }
    ] : []),
    { title: 'Количество занятий', dataIndex: 'lesson_counter', key: 'lesson_counter' },
  ];

  const columnsForStudents = [
    { title: 'ID Студента', dataIndex: 'stud_id', key: 'stud_id',
    render: (text, record) => (
      <a
        onClick={() => navigate(`/student/${record.stud_id}`)}
      >
        {text}
      </a>
    ),
     },
    { title: 'Успеваемость (баллы)', dataIndex: 'Успеваемость', key: 'marks' },
    { title: 'Посещаемость (макс 22)', dataIndex: 'Посещаемость', key: 'attendance' },
    ...(selectedKR === null ? [
      { title: 'Контрольная точка', dataIndex: 'name', key: 'name' }
    ] : []),
    { title: 'Количество занятий', dataIndex: 'lesson_counter', key: 'lesson_counter' },
  ];

  const columnsForStudentsWithTeacherAndTeam = [
    ...columnsForStudents,
    { title: 'Преподаватель', dataIndex: 'teacher_name', key: 'teacher_name' }, // Add teacher_name column
    { title: 'Группа', dataIndex: 'team_name', key: 'team_name' }, 
  ];

  const columnsForStudentsWithSpeciality = [
    ...columnsForStudents,
    { title: 'Направление', dataIndex: 'speciality', key: 'speciality' }, 
  ];

  const columnsForStudentsWithTeacher = [
    ...columnsForStudents,
    { title: 'Преподаватель', dataIndex: 'teacher_name', key: 'teacher_name' }, // Add teacher_name column
  ];
  
  const params = new URLSearchParams({
    token: userToken,
    is_by_mark: isByMark,
    is_group_by: isGroupBy,
  });

  if (isGroupBy === true) {
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

  const requestUrl = `http://moais-dashboard.ru:8082/api/top_10_most_and_least_studs?${params.toString()}`;
    
      const handleUpdateRequests = (updatedRequests) => {
        setRequests(updatedRequests);
      };


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


<div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center',marginTop: "10px" }}>
    <Title level={2} >Топ студентов</Title>
  </div>

  <div style={{ display: 'flex', justifyContent: 'space-evenly', flexWrap: 'wrap', alignItems: 'center'}}>

          <Tooltip title="Укажите режим">
          <Select
          allowClear
            style={{ width: 200 }}
            placeholder="Группировать? *"
            value={isGroupBy}
            onChange={value => setIsGroupBy(value)}
          >
            <Option value={true}>С группировкой</Option>
            <Option value={false}>Без группировки</Option>
          </Select>
          </Tooltip>

          <Tooltip title="Укажите тип сортировки">
          <Select
          allowClear
            style={{ width: 200 }}
            placeholder="Сортировать по *"
            value={isByMark}
            onChange={value => setIsByMark(value)}
          >
            <Option value={true}>Успеваемость</Option>
            <Option value={false}>Посещаемость</Option>
          </Select>
          </Tooltip>

          {isGroupBy && (
          <Tooltip title="Укажите тип, если группируете">
            <Select
            allowClear
              style={{ width: 200 }}
              placeholder="Тип группировки *"
              value={typeGroupBy}
              onChange={value => setTypeGroupBy(value)}
            >
              <Option value={0}>По командам</Option>
              <Option value={1}>По направлениям</Option>
              <Option value={2}>По преподавателям</Option>
            </Select>
          </Tooltip>
          )}
          
          <Tooltip title="Укажите контрольную точку для отсеивания друих">
          <Select
            style={{ width: 200 }}
            placeholder="Контрольная точка *"
            value={selectedKR}
            onChange={handleKRChange}
            allowClear
          >
            {uniqueKRNames.map(name => (
              <Option key={name} value={name}>
                {name}
              </Option>
            ))}
          </Select>
          </Tooltip>


          <Tooltip title="Укажите желаемые учебные групыы">
          <Select
            mode="multiple"
            allowClear
            style={{ width: 200 }}
            placeholder="Выберите группу"
            onChange={handleChangeTeam}
            >
              {TeamData && TeamData.map(team => (
                  <Option key={team.id} value={team.id}>
                      {team.name}
                  </Option>
              ))} 
            </Select>
            </Tooltip>
    

            <Tooltip title="Укажите желаемые направления">
            <Select
            mode="multiple"
            allowClear
            style={{ width: 280 }}
            placeholder="Выберите направление"
            onChange={handleChangeSpeciality}
            >
                  {SpecialityData && SpecialityData.map(spec => (
              <Option key={spec.speciality} value={spec.peciality}>
                  {spec.peciality}
              </Option>
            ))} 
            </Select>
            </Tooltip>
    
            <Tooltip title="Укажите желаемых преподавателей">
            <Select
          mode="multiple"
          allowClear
          style={{ width: 280 }}
          placeholder="Выберите преподавателя"
          onChange={handleChangeTeacher}
            >
                 {TeacherData && TeacherData.map((teacher, index) => (
            <Option key={`${teacher.id}-${index}`} value={teacher.name}> 
                {teacher.name}
            </Option>
        ))}
        </Select>
        </Tooltip>

        <RequestCheckbox
        requestUrl={requestUrl}
        requestName="Топ студентов"
        onUpdateRequests={handleUpdateRequests}
        />

          {/* <Button style={{background: "green", color: "white"}} onClick={handleDownload}>Скачать данные</Button> */}

    </div>

        {isGroupBy ? (
          <div style={{ display: 'flex', justifyContent: 'center', gap: '20px', marginTop: 20 }}>
          <Table
          // dataSource={(studentsBest || []).flatMap(group => group.top_10_best.map((item, i) => ({
            dataSource={studentsBest && studentsBest.flatMap(group => group.top_10_best.map((item, i) => ({
              ...item,
              key: i,
              Успеваемость: item.Успеваемость,
              Посещаемость: item.Посещаемость,
              stud_id: item.stud_id,
              name: item.name,
              lesson_counter: item.lesson_counter,
              teacher_name: group.teacher_name,
              team_name: group.team_name,
            })))}
            columns={typeGroupBy === 0 ? columnsForStudentsWithTeacherAndTeam :
              typeGroupBy === 1 ? columnsForStudentsWithSpeciality :
              columnsForStudentsWithTeacher
              }
            
            rowKey="stud_id"
            title={() => 'Топ 10 преуспевающих'}
          />
          <Table
              // dataSource={(studentsLeast || []).flatMap(group => group.top_10_least.map((item, i) => ({
                dataSource={studentsLeast && studentsLeast.flatMap(group => group.top_10_least.map((item, i) => ({
              ...item,
              key: i,
              Успеваемость: item.Успеваемость,
              Посещаемость: item.Посещаемость,
              stud_id: item.stud_id,
              name: item.name,
              lesson_counter: item.lesson_counter,
              teacher_name: group.teacher_name,
              team_name: group.team_name,
            })))}
            columns={typeGroupBy === 0 ? columnsForStudentsWithTeacherAndTeam :
              typeGroupBy === 1 ? columnsForStudentsWithSpeciality :
              columnsForStudentsWithTeacher
              }
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
  </>
)}

export default TopPage;   