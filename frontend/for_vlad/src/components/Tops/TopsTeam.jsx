import React, { useState, useEffect } from 'react';
import { Select, Table, Typography, Cascader, Spin,Button,Row} from 'antd';
import { useAuth } from '../useAuth';
import {fetchWithTokenRefresh} from '../RefreshToken'
import { useNavigate } from 'react-router-dom';
import { SelectProps } from 'antd';

import RequestCheckbox from '../ReportSystem/RequestCheckbox';

const { Option } = Select;
const { Title } = Typography;

const TopsTeam = () => {
  const [requests, setRequests] = useState([]);

    const { userToken } = useAuth();
    
    const navigate = useNavigate();

    const [isByMark, setIsByMark] = useState(true);
    const [isTypeGroup, setTypeGroupBy] = useState(0);

    const [TeacherData, SetTeacherData] = useState(null);
    const [SelectedTeacher, setSelectedTeacher] = useState([]);

    const [SpecialityData, SetSpecialityData] = useState(null);
    const [SelectedSpeciality, setSelectedSpeciality] = useState([]);

    const [TeamData, SetTeamData] = useState(null);
    const [SelectedTeam, setSelectedTeam] = useState([]);

    const [Top_10_most_and_least_team, setTop_10_most_and_least_team] = useState([])
    
    const [uniqueKRNames, setUniqueKRNames] = useState([]);
    const [selectedKR, setSelectedKR] = useState("Аттестация00");


    const [loading, setLoading] = useState(false); // Состояние загрузки

    const [dataInTable,setDataInTable] = useState([])

    const fetch_Top_10_most_and_least_team = async () => {
        setLoading(true);
        try {
          const params = new URLSearchParams({
            token: userToken,
            is_by_mark: isByMark,
            type_group_by : isTypeGroup,
          });
          if (SelectedTeacher && SelectedTeacher.length > 0) {
            params.append('teacher_list', SelectedTeacher.join(','));
          }
          if (SelectedSpeciality && SelectedSpeciality.length > 0) {
            params.append('speciality_list', SelectedSpeciality.join(','));
          }
          if (SelectedTeam && SelectedTeam.length > 0) {
            params.append('team_list', SelectedTeam.join(','));
          }
          
          // console.log('Request URL:', `http://moais-dashboard.ru:8082/api/top_10_most_and_least_studs?${params.toString()}`);
      
          const response = await fetchWithTokenRefresh(`http://moais-dashboard.ru:8082/api/top_10_most_and_least_teams?${params.toString()}`);
      
          if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
          }
          
          const data = await response.json();
          setTop_10_most_and_least_team(data);  
            
    
        } catch (error) {
          console.error('Error fetching data:', error);
        } finally {
          setLoading(false); // Устанавливаем состояние загрузки в false после завершения запроса
        }
        
      };
      console.log('Top_10_most_and_least_team',Top_10_most_and_least_team)

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
        if (userToken){
            fetch_Top_10_most_and_least_team();
        }
        }, [isByMark, isTypeGroup, SelectedTeacher, SelectedSpeciality, SelectedTeam]);      

    useEffect(() => {
        const fetchData = async () => {
            fetchTeam();
            fetchTeacher();
            fetchSpeciality();
        }
    if (userToken) {fetchData();} }, [userToken]);

      useEffect(() => { // condition for show kr name - UNICUE NAME
        if (Top_10_most_and_least_team && Top_10_most_and_least_team.length > 0) {
          const names = Top_10_most_and_least_team.map(item => item.name);
          const uniqueNames = [...new Set(names)];
          setUniqueKRNames(uniqueNames);
          console.log('uniqueKRNames',uniqueKRNames)
        }
      }, [Top_10_most_and_least_team]);

      
      useEffect(() => { // condition for update table - if changes KR
        if (selectedKR) {
            setDataInTable(Top_10_most_and_least_team.filter(item => item.name === selectedKR));
        } else {
            setDataInTable(Top_10_most_and_least_team);
        }
        console.log('UPDATE TABLE - CJOISE OTHER KR')
        console.log('dataInTable',dataInTable)
    }, [selectedKR, Top_10_most_and_least_team]);


    const handleChangeTeacher = (value) => {
        const teacherValues = Array.isArray(value) ? value.map(v => v.toString()) : [value.toString()];
        setSelectedTeacher(teacherValues);
    };

    const handleChangeSpeciality = (value) => {
        const specialityValues = Array.isArray(value) ? value.map(v => v.toString()) : [value.toString()];
        setSelectedSpeciality(specialityValues);
    };

    const handleChangeTeam = (value) => {
        const teamValues = Array.isArray(value) ? value.map(v => v.toString()) : [value.toString()];
        setSelectedTeam(teamValues);
    };

    const params = new URLSearchParams({
      token: userToken,
      is_by_mark: isByMark,
      type_group_by : isTypeGroup,
    });
    if (SelectedTeacher && SelectedTeacher.length > 0) {
      params.append('teacher_list', SelectedTeacher.join(','));
    }
    if (SelectedSpeciality && SelectedSpeciality.length > 0) {
      params.append('speciality_list', SelectedSpeciality.join(','));
    }
    if (SelectedTeam && SelectedTeam.length > 0) {
      params.append('team_list', SelectedTeam.join(','));
    }

    const handleUpdateRequests = (updatedRequests) => {
      setRequests(updatedRequests);
    };
  
    const requestUrl = `http://moais-dashboard.ru:8082/api/top_10_most_and_least_teams?${params.toString()}`;


      const handleKRChange = (value) => { // condition - 
        setSelectedKR(value);
        if (value) {
          setDataInTable(Top_10_most_and_least_team.filter(item => item.name === value));
        } else {
          setDataInTable(Top_10_most_and_least_team);
        }
        console.log('CHANGES KR')
      };

      const columns_team = [
        { title: 'Команда', 
        dataIndex: 'team_name', 
        key: 'team_name',

        render: (text, record) => (
          <a
              onClick={() => navigate(`/main/${record.team_id}`)}
          >
            {text}
          </a>
        ),

      },
        { 
            title: 'Преподаватель', 
            dataIndex: 'teacher_name', 
            key: 'teacher_name'
        },
        { 
          ...(selectedKR === null ? [
            { title: 'Контрольная точка', dataIndex: 'name', key: 'name' }
          ] : []),
        },
        { 
            title: 'Медианная Успеваемость', 
            dataIndex: 'Успеваемость_средняя', 
            key: 'Успеваемость_средняя',
            // sorter: (a, b) => b['Успеваемость_средняя'] - a['Успеваемость_средняя'],

        },
        { 
            title: 'Медианная Посещаемость', 
            dataIndex: 'Посещаемость_средняя', 
            key: 'Посещаемость_средняя',
            // sorter: (a, b) => b['Посещаемость_средняя'] - a['Посещаемость_средняя'],

        },
      ];  

      const columns_speciality = [
        { title: 'Направление', dataIndex: 'speciality', key: 'speciality',

        // render: (text, record) => (
        //   <a
        //       onClick={() => navigate(`/student/${record.stud_id}/${record.team_id}/${encodeURIComponent(record.team_name)}`)}
        //   >
        //     {text}
        //   </a>
        // ),

      },
        { 
            title: 'Контрольная точка', 
            dataIndex: 'name', 
            key: 'name'
        },
        { 
            title: 'Медианная Успеваемость', 
            dataIndex: 'Успеваемость_средняя', 
            key: 'Успеваемость_средняя',
            // sorter: (a, b) => b['Успеваемость_средняя'] - a['Успеваемость_средняя'],

        },
        { 
            title: 'Медианная посещаемость', 
            dataIndex: 'Посещаемость_средняя', 
            key: 'Посещаемость_средняя',
            // sorter: (a, b) => b['Посещаемость_средняя'] - a['Посещаемость_средняя'],

        },
      ];  

      const columns_teacher = [
        { 
            title: 'Преподаватель', 
            dataIndex: 'teacher_name', 
            key: 'teacher_name'
        },
        { 
            title: 'Контрольная точка', 
            dataIndex: 'name', 
            key: 'name'
        },
        { 
            title: 'Медианная Успеваемость', 
            dataIndex: 'Успеваемость_средняя', 
            key: 'Успеваемость_средняя',
            // sorter: (a, b) => b['Успеваемость_средняя'] - a['Успеваемость_средняя'],

        },
        { 
            title: 'Медианная посещаемость', 
            dataIndex: 'Посещаемость_средняя', 
            key: 'Посещаемость_средняя',
            // sorter: (a, b) => b['Посещаемость_средняя'] - a['Посещаемость_средняя'],

        },
      ];  

    
      const columns = 
      isTypeGroup === 0 ? columns_team :
      isTypeGroup === 1 ? columns_speciality :
      isTypeGroup === 2 ? columns_teacher :
      [];
      
      
    //   const getColumns = (isByMark) => [
    //     {
    //         title: 'Команда',
    //         dataIndex: 'team_name',
    //         key: 'team_name',
    //     },
    //     {
    //         title: 'Преподаватель',
    //         dataIndex: 'teacher_name',
    //         key: 'teacher_name',
    //     },
    //     {
    //         title: 'Контрольная точка',
    //         dataIndex: 'name',
    //         key: 'name',
    //     },
    //     {
    //         title: 'Медианная Успеваемость',
    //         dataIndex: 'Успеваемость_средняя',
    //         key: 'Успеваемость_средняя',
    //         sorter: isByMark ? (a, b) => b['Успеваемость_средняя'] - a['Успеваемость_средняя'] : undefined,
    //     },
    //     {
    //         title: 'Медианная посещаемость',
    //         dataIndex: 'Посещаемость_средняя',
    //         key: 'Посещаемость_средняя',
    //         sorter: !isByMark ? (a, b) => b['Посещаемость_средняя'] - a['Посещаемость_средняя'] : undefined,
    //     },
    // ];
      


    return (
      <>
        <div style={{ position: 'relative', minHeight: '100px' }}>
          <Spin
            spinning={loading}
            tip="Loading"
            size="large"
            style={{
              position: 'absolute',
              top: '8%',
              left: '50%',
              transform: 'translate(-50%, -50%)',
              zIndex: 10
            }}
          />
    
          <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', margin: '10px 0' }}>
              <Title level={2} style={{ margin: 0 }}>Топ команд</Title>
            </div>

            <div style={{ display: 'flex', justifyContent: 'space-evenly', flexWrap: 'wrap', alignItems: 'center' }}>
              <Select
                placeholder="Сортировать по: *"
                style={{ width: 200 }}
                value={isByMark}
                onChange={value => setIsByMark(value)}
                allowClear
              >
                <Option value={true}>Успеваемость</Option>
                <Option value={false}>Посещаемость</Option>
              </Select>
    
              <Select
                placeholder="Тип группировки: *"
                style={{ width: 200 }}
                value={isTypeGroup}
                onChange={value => setTypeGroupBy(value)}
                allowClear
              >
                <Option value={0}>По командам</Option>
                <Option value={1}>По направлениям</Option>
                <Option value={2}>По преподавателям</Option>
              </Select>
    
              <Select
                placeholder="Выберите контрольную точку"
                style={{ width: 200 }}
                value={selectedKR}
                onChange={handleKRChange}
                allowClear
              >
                {uniqueKRNames.map(point => (
                  <Option key={point} value={point}>
                    {point}
                  </Option>
                ))}
              </Select>
    
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
    
              <Select
                mode="multiple"
                allowClear
                style={{ width: 280 }}
                placeholder="Выберите направление"
                onChange={handleChangeSpeciality}
              >
                {SpecialityData && SpecialityData.map(spec => (
                  <Option key={spec.speciality} value={spec.speciality}>
                    {spec.speciality}
                  </Option>
                ))}
              </Select>
    
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
    
              <RequestCheckbox
                requestUrl={requestUrl}
                requestName="Топ команд"
                onUpdateRequests={handleUpdateRequests}
              />
            </div>
          </div>
    
          <div style={{
            display: 'flex',
            justifyContent: 'space-around',
            gap: '20px',
            marginTop: 20
          }}>
            <Table
              style={{ width: '50%' }}
              dataSource={dataInTable.slice(0, Math.ceil(dataInTable.length / 2))}
              columns={columns}
              rowKey="team_name"
              title={() => 'Отстающие'}
            />
            <Table
              style={{ width: '50%' }}
              dataSource={dataInTable.slice(Math.ceil(dataInTable.length / 2))}
              columns={columns}
              rowKey="team_name"
              title={() => 'Преуспевающие'}
            />
          </div>
      </>
    );
  }

export default TopsTeam;
