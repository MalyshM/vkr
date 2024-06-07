import React, { useState, useEffect,useRef } from 'react';
import { Select, Table, Typography, Spin,} from 'antd';

import { useAuth } from '../useAuth';
import {fetchWithTokenRefresh} from '../RefreshToken'

import RequestCheckbox from '../ReportSystem/RequestCheckbox';

import { useNavigate } from 'react-router-dom';
import { InputNumber } from 'antd';
import { Tooltip } from 'antd';

const { Option } = Select;
const { Title } = Typography;

const LeastPage = () => {

  const [requests, setRequests] = useState([]);

    const navigate = useNavigate();
    const {userToken} = useAuth()
    const fetchTimer = useRef(null);

    const [isGroupBy, setGroupBy] = useState(true) // groun or not
    const [isByMark, setIsByMark] = useState(true); // atendace or mark
    const [isTypeGroup, setTypeGroupBy] = useState(0); // mode of group
    const [isThreshold, setThreshold] = useState(60) //threshold for stud-t

    const [TeacherData, SetTeacherData] = useState(null); //storage list of teacher
    const [SelectedTeacher, setSelectedTeacher] = useState([]);

    const [SpecialityData, SetSpecialityData] = useState(null); //storage list of speciality
    const [SelectedSpeciality, setSelectedSpeciality] = useState([]);

    const [TeamData, SetTeamData] = useState(null); //storage list of team
    const [SelectedTeam, setSelectedTeam] = useState([]);

    const [LaggingStudents, setLaggingStudents] = useState([]) //storage array object - stud-s


    const [uniqueKRNames, setUniqueKRNames] = useState([]); // kontrol point 
    const [selectedKR, setSelectedKR] = useState("Аттестация00"); // state for update table if changes kr
    const [loading, setLoading] = useState() // state for spin

    const [dataInTable,setDataInTable] = useState([]) // state for show data on table
    const [expandedGroups, setExpandedGroups] = useState({});


    const fetch_lagging_students = async () => {
        setLoading(true);
        try {
          const params = new URLSearchParams({
            token: userToken,
            is_group_by: isGroupBy,
            is_by_mark: isByMark,
            threshold: isThreshold,
            // type_group_by : isTypeGroup,
          });
          if (isGroupBy == true) {
            params.append('type_group_by', isTypeGroup);
          } else {}
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
      
          const response = await fetchWithTokenRefresh(`http://moais-dashboard.ru:8082/api/lagging_students?${params.toString()}`);
      
          if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
          }
          
          const data = await response.json();
          setLaggingStudents(data);

          const updatedLaggingStudents = data.map(group => {
            const updatedResult1 = group.result1.map(item => ({
                ...item,
                name: group.name,
                lesson_counter: group.lesson_counter,
            }));
            return {
                ...group,
                result1: updatedResult1,
            };
        });
        
        setLaggingStudents(updatedLaggingStudents);

        if (selectedKR) {
            setDataInTable(updatedLaggingStudents.filter(item => item.name === selectedKR));
        } else {
            setDataInTable(updatedLaggingStudents);
        }
            
    
        } catch (error) {
          console.error('Error fetching data:', error);
        } finally {
          setLoading(false); // Устанавливаем состояние загрузки в false после завершения запроса
        }
        
      };

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
            fetch_lagging_students();
        }
        }, [isGroupBy, isByMark, isThreshold, isTypeGroup, SelectedTeacher, SelectedSpeciality, SelectedTeam]);  

        useEffect(() => {
          const fetchData = async () => {
              fetchTeam();
              fetchTeacher();
              fetchSpeciality();
          }
      if (userToken) {fetchData();} }, [userToken]);
        
        useEffect(() => { //limit requests
          if (userToken) {
              if (fetchTimer.current) {
                  clearTimeout(fetchTimer.current);
              }
              fetchTimer.current = setTimeout(fetch_lagging_students, 1000); // Limit requests to once per second
          }
          return () => clearTimeout(fetchTimer.current); // Cleanup on unmount or dependency change
      }, [isGroupBy, isByMark, isThreshold, isTypeGroup, SelectedTeacher, SelectedSpeciality, SelectedTeam, userToken]);
  

        useEffect(() => { // condition for show kr name - UNICUE NAME
          if (LaggingStudents && LaggingStudents.length > 0) {
            const names = LaggingStudents.map(item => item.name);
            const uniqueNames = [...new Set(names)];
            setUniqueKRNames(uniqueNames);
            console.log('uniqueKRNames',uniqueKRNames)
          }
        }, [LaggingStudents]);


        useEffect(() => { // condition for update table - if changes KR
          if (selectedKR) {
              setDataInTable(LaggingStudents.filter(item => item.name === selectedKR));
          } else {
              setDataInTable(LaggingStudents);
          }
          console.log('UPDATE TABLE - CJOISE OTHER KR')
          console.log('dataInTable',dataInTable)
      }, [selectedKR, LaggingStudents]);


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

        const handleKRChange = (value) => { // condition - 
            setSelectedKR(value);
            if (value) {
              setDataInTable(LaggingStudents.filter(item => item.name === value));
            } else {
              setDataInTable(LaggingStudents);
            }
            console.log('CHANGES KR')
          };
       
        const columns = [
        { title: 'ID Студента', dataIndex: 'stud_id', key: 'stud_id',
        render: (text, record) => (
          <a
              onClick={() => navigate(`/student/${record.stud_id}`)}
          >
            {text}
          </a>
        ),
      },
        { title: 'Успеваемость', dataIndex: 'Успеваемость', key: 'Успеваемость' },
        { title: 'Посещаемость', dataIndex: 'Посещаемость', key: 'Посещаемость' },
        ...(selectedKR === null ? [
          { title: 'Контрольная точка', dataIndex: 'name', key: 'name' }
        ] : []),
        { title: 'Кол-во встреч', dataIndex: 'lesson_counter', key: 'lesson_counter' },
      ];

      const params = new URLSearchParams({
        token: userToken,
        is_group_by: isGroupBy,
        is_by_mark: isByMark,
        threshold: isThreshold,
      });
      if (isGroupBy === true) {
        params.append('type_group_by', isTypeGroup);
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
      const requestUrl = `http://moais-dashboard.ru:8082/api/lagging_students?${params.toString()}`;
    
      const handleUpdateRequests = (updatedRequests) => {
        setRequests(updatedRequests);
      };
    

        return(
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
    
    
    <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center',marginTop: "10px" }}>
          <Title level={2} style={{ margin: 0 }}>Отстающие</Title>
        </div>
        
        <div style={{ display: 'flex', justifyContent: 'space-evenly', flexWrap: 'wrap', alignItems: 'center' ,marginTop: "10px"}}>
          <Tooltip title="Укажите режим">
            <Select
              placeholder="* Группировать?"
              style={{ width: 150 }}
              value={isGroupBy}
              onChange={value => setGroupBy(value)}
              allowClear
            >
              <Option value={true}>Группировать</Option>
              <Option value={false}>Без группировки</Option>
            </Select>
          </Tooltip>

          <Tooltip title="Укажите тип сортировки">
            <Select
              placeholder="* Сортировать по:"
              style={{ width: 160 }}
              value={isByMark}
              onChange={value => setIsByMark(value)}
              allowClear
            >
              <Option value={true}>Успеваемость</Option>
              <Option value={false}>Посещаемость</Option>
            </Select>
          </Tooltip>

          <Tooltip title="Укажите, чтобы задать ограничение">
            <InputNumber
              placeholder="* Установите порог:"
              allowClear
              min={0}
              max={120}
              value={isThreshold}
              onChange={value => setThreshold(value)}
              style={{ width: 160 }}
            />
          </Tooltip>

        {isGroupBy && (
          <Tooltip title="Укажите тип, если группируете">
            <Select
              placeholder="Тип группировки:"
              style={{ width: 170 }}
              value={isTypeGroup}
              onChange={value => setTypeGroupBy(value)}
              allowClear
            >
              <Option value={0}>По командам</Option>
              <Option value={1}>По направлениям</Option>
              <Option value={2}>По преподавателям</Option>
            </Select>
          </Tooltip>
        )}

          <Tooltip title="Укажите контрольную точку для отсеивания других">
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
          </Tooltip>

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
            requestName="Список отстающих"
            onUpdateRequests={handleUpdateRequests}
          />
        </div>
      </div>

      <div style={{
        display: 'flex',
        flexWrap: 'wrap',
        gap: '20px',
        marginTop: 20
      }}>

        {isGroupBy && dataInTable && dataInTable.length > 0 && dataInTable.map((group, index) => (
          <Table
            key={index}
            style={{ width: '30%' }}
            dataSource={group.result1 ? group.result1.map((item, i) => ({ ...item, key: i })) : []}
            columns={columns}
            title={() => {
              switch (isTypeGroup) {
                case 0:
                  return `${group.team_id}`;
                case 1:
                  return `${group.speciality}`;
                case 2:
                  return `${group.teacher_id}`;
                default:
                  return '';
              }
            }}
          />
        ))}

      {!isGroupBy && (
          <Table
            style={{ width: '100%' }}
            dataSource={dataInTable.map((item, index) => ({ ...item, key: `${item.stud_id}-${index}` }))}
            columns={columns}
            rowKey="key"
          />
        )}

      </div>

    </>
    )
  }

export default LeastPage;
