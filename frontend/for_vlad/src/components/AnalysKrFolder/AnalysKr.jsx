import React, { useState,useEffect} from 'react';
import { Box, Flex, Select ,Heading,Checkbox,MenuItem,MenuList,Button,MenuButton,Menu} from '@chakra-ui/react';
import { useAuth } from '../useAuth';
import { fetchWithTokenRefresh } from '../RefreshToken';
import AnalysKrSimple from './AnalysKrSimple'
import AnalysKrFiltres from './AnalysKrFiltres'
import {Tooltip } from '@chakra-ui/react';
import { QuestionOutlineIcon } from '@chakra-ui/icons'
const AnalysRr = () => {
    const { userToken } = useAuth();

    //team
    const [TeamData, setTeam] = useState(null);
    const [SelectedTeam, setSelectedTeam] = useState([]);
    const [TeamsForSelectedTeacher, setTeamsForSelectedTeacher] = useState(null) //storage teams for selected teacher
    const [TeamsForSelectedSpeciality, setTeamsForSelectedSpeciality] = useState(null); //storage arr teams of choise speciality


    //teacher
    const [SelectedTeacher, setSelectedTeacher] = useState([]);
    const [TeacherData, setNameTeachers] = useState(null);
    const [TeachersForSelectedSpeciality, setTeachersForSelectedSpeciality] = useState(null); //storage arr teachers of choise speciality

    //spec
    const [SpecialityData, setSpeciality] = useState(null);
    const [SelectedSpeciality, setSelectedSpeciality] = useState([]);
    const [SpecialityForSelectedTeacher, setSpecialityForSelectedTeacher] = useState(null) //storage speciality for selected teacher

    //other

    const [selectedKRSimple, setSelectedKRSimple] = useState(null);
    const [KRSimple, setKRSimple] = useState(null);

    const [selectedKRFiltr, setSelectedKRFiltr] = useState(null);
    const [KRFiltr, setKRFiltr] = useState(null);

    const [selectedModeSimple, setSelectedModeSimple] = useState(null);
    const [selectedModeFiltr, setSelectedModeFiltr] = useState(null);




  const fetchNameKR = async () => {
  try {
    const response = await fetchWithTokenRefresh('http://moais-dashboard.ru:8082/api/get_all_kr');
    const result = await response.json();
    setKRSimple(result);
    setKRFiltr(result);


    console.log('Data from fetchNameKR:', result);

} catch (error) {
    console.error('Error fetching data from fetchNameKR:', error);
  }
};

const fetchAllTeachers = async () => {
    try {
      const response = await fetchWithTokenRefresh(`http://moais-dashboard.ru:8082/api/get_all_teachers?token=${userToken}`);
      const result = await response.json();
      setNameTeachers(result);
  
      console.log('Data from fetchAllTeachers:', result);
  
  } catch (error) {
      console.error('Error fetching data from fetchAllTeachers:', error);
    }
  };

  const fetchAllSpeciality = async () => {
    try {
      const response = await fetchWithTokenRefresh(`http://moais-dashboard.ru:8082/api/get_all_specialities?token=${userToken}`);
      const result = await response.json();
      setSpeciality(result);
  
      console.log('Data from fetchAllSpeciality:', result);
  
  } catch (error) {
      console.error('Error fetching data from fetchAllSpeciality:', error);
    }
  };

  const fetchAllTeam = async () => {
    try {
      const response = await fetchWithTokenRefresh(`http://moais-dashboard.ru:8082/api/get_teams_for_user_without_lect?token=${userToken}`);
      const result = await response.json();
      setTeam(result);
  
      console.log('Data from fetchAllTeam:', result);
  
  } catch (error) {
      console.error('Error fetching data from fetchAllTeam:', error);
    }
  };

  const fetchTeamForChoiseTeacher = async () => {
    try {
      const response = await fetchWithTokenRefresh(`http://moais-dashboard.ru:8082/api/get_teams_for_param_without_lect?teacher_arr=${SelectedTeacher}`);
      const result = await response.json();
      setTeamsForSelectedTeacher(result);
      console.log('fetchTeamForChoiseTeacher:', result);
  } catch (error) {
      console.error('Error fetching data from fetchTeamForChoiseTeacher:', error);
    }
  };

  const fetchSpecialityForChoiseTeacher = async () => {
    try {
      const response = await fetchWithTokenRefresh(`http://moais-dashboard.ru:8082/api/get_all_specialities_by_teacher_arr?token=${userToken}&teacher_list=${SelectedTeacher}`);
      const result = await response.json();
      setSpecialityForSelectedTeacher(result);
      console.log('fetchSpecialityForChoiseTeacher:', result);
  } catch (error) {
      console.error('Error fetching data from fetchSpecialityForChoiseTeacher:', error);
    }
  };

  const fetchTeacherForChoiseSpeciality = async () => {
    try {
      const response = await fetchWithTokenRefresh(`http://moais-dashboard.ru:8082/api/get_all_teachers_by_speciality_arr?token=${userToken}&speciality_list=${SelectedSpeciality}`);
      const result = await response.json();
      setTeachersForSelectedSpeciality(result);
      console.log('fetchTeacherForChoiseSpeciality:', result);
  } catch (error) {
      console.error('Error fetching data from fetchTeacherForChoiseSpeciality:', error);
    }
  };

  const fetchTeamsForChoiseSpeciality = async () => {
    try {
      const response = await fetchWithTokenRefresh(`http://moais-dashboard.ru:8082/api/get_all_teams_by_speciality_arr?token=${userToken}&speciality_list=${SelectedSpeciality}`);
      const result = await response.json();
      setTeamsForSelectedSpeciality(result);
      console.log('fetchTeamsForChoiseSpeciality:', result);
  } catch (error) {
      console.error('Error fetching data from fetchTeamsForChoiseSpeciality:', error);
    }
  };


  useEffect(() => {
    const fetchData = async () => {
      await fetchNameKR();
      await fetchAllTeachers();
      await fetchAllSpeciality();
      await fetchAllTeam();      
    }

    if (userToken) {
      fetchData();
    }
  }, [userToken]);


  useEffect(() => {
    if (SelectedTeacher.length > 0) {
        fetchTeamForChoiseTeacher();
        fetchSpecialityForChoiseTeacher();
    }
}, [SelectedTeacher]);


useEffect(() => {
    if (SelectedSpeciality.length > 0) {
        fetchTeacherForChoiseSpeciality();
        fetchTeamsForChoiseSpeciality();
    }
}, [SelectedSpeciality]);



  const handleKRChangeSimple = (value) => {
    setSelectedKRSimple(value);
  };

  const handleKRChangeFiltr = (value) => {
    setSelectedKRFiltr(value);
  };

  const handleTeacherSelect = (teacher) => {
    if (SelectedTeacher.includes(teacher)) {
        setSelectedTeacher(SelectedTeacher.filter((id) => id !== teacher));
    } else {
        setSelectedTeacher([...SelectedTeacher, teacher]);
    }
    // console.log('SelectedTeacher',SelectedTeacher)
};

const handleTeamSelect = (team_id) => {
    if (SelectedTeam.includes(team_id)) {
        setSelectedTeam(SelectedTeam.filter((id) => id !== team_id));
    } else {
        setSelectedTeam([...SelectedTeam, team_id]);
    }
};

const handleSpecialitySelect = (SpecialityData) => {
    if (SelectedSpeciality.includes(SpecialityData)) {
        setSelectedSpeciality(SelectedSpeciality.filter((speciality) => SpecialityData !== SpecialityData));
    } else {
        setSelectedSpeciality([...SelectedSpeciality, SpecialityData]);
    }
};
  

  const handleModeChangeSimple = (event) => {
    const newMode = parseInt(event.target.value, 10);
    setSelectedModeSimple(newMode);
  };

  const handleModeChangeFiltr = (event) => {
    const newMode = parseInt(event.target.value, 10);
    setSelectedModeFiltr(newMode);
  };


 
return( 
<>
  <Box p={6} display="flex" justifyContent={'space-between'} alignItems={'center'}>
    <Heading as="h1" size="lg">Анализ Контрольных работ</Heading>
    <Tooltip label="Диаграмма отображающая распределения баллов студентов по КР через: Минимум, Первый квартиль, Медиана, Третий квартиль, Максимум, Выбросы" aria-label="A tooltip">
            <QuestionOutlineIcon ml={2} mt={2} boxSize={4} cursor="pointer" />
        </Tooltip>
    <Box ml={'auto'} mr={4} w="250px" borderRadius="lg" boxShadow="lg">
          <Select borderColor='black'
            placeholder="Выберите контрольную работу"
            onChange={(e) => handleKRChangeSimple(e.target.value)}
            value={selectedKRSimple}>

            {Array.isArray(KRSimple) ? (
              KRSimple.map((task) => (
                <option key={task.name} value={task.name}>
                  {task.name}
                </option>
              ))
            ) : (
              <option disabled>No kr available</option>
            )}
          </Select>
        </Box>
        

        <Box mr={4} w="330px" borderRadius="lg" boxShadow="lg">
        <Select
            borderColor='black'
            id="modeSelectSimple"
            value={selectedModeSimple}
            onChange={handleModeChangeSimple}
            placeholder="Выбери режим"
        >
            <option value={0}>По группам</option>
            <option value={1}>По направлениям</option>
            <option value={2}>По преподавателям</option>
        </Select>
        </Box>
  
    </Box>


    <Flex direction={'column'}>

        <Box height={"380"}>
          {<AnalysKrSimple tokenUsers={userToken} type={selectedModeSimple} kr={selectedKRSimple}  />}
        </Box>

      
      <Flex ml="auto" >

        <Box mr={4} w="290px" borderRadius="lg" boxShadow="lg">
          <Select borderColor='black'
            placeholder="Выберите контрольную работу"
            onChange={(e) => handleKRChangeFiltr(e.target.value)}
            value={selectedKRFiltr}>

            {Array.isArray(KRFiltr) ? (
              KRFiltr.map((task) => (
                <option key={task.name} value={task.name}>
                  {task.name}
                </option>
              ))
            ) : (
              <option disabled>No kr available</option>
            )}
          </Select>
        </Box>

        

        <Box mr={4} w="200px" borderRadius="lg" boxShadow="lg">
        <Select
            borderColor='black'
            id="modeSelectFiltr"
            value={selectedModeFiltr}
            onChange={handleModeChangeFiltr}
            placeholder="Выбери режим"
        >
            <option value={0}>По группам</option>
            <option value={1}>По преподавателям</option>
            <option value={2}>По направлениям</option>
        </Select>
        </Box>

        <Menu closeOnSelect={false}>
                    <MenuButton mr={4} as={Button} colorScheme="blue">
                        Выбрать преподавателей
                    </MenuButton>
                    <MenuList minWidth="240px">
                    { SelectedSpeciality.length > 0 && TeachersForSelectedSpeciality ? (
                            TeachersForSelectedSpeciality.map((teacher) => (
                                <MenuItem key={teacher.name}>
                                    <Checkbox
                                        isChecked={SelectedTeacher.includes(teacher.name)}
                                        onChange={() => handleTeacherSelect(teacher.name)}
                                    >
                                        {teacher.name}
                                    </Checkbox>
                                </MenuItem>
                            ))
                        ) : (
                    TeacherData && TeacherData.map((teacher) => (
                        <MenuItem key={teacher.name}>
                            <Checkbox
                            isChecked={SelectedTeacher.includes(teacher.name)}
                            onChange={() => handleTeacherSelect(teacher.name)}
                            >
                            {teacher.name}
                            </Checkbox>
                        </MenuItem>
                        )))}
                    </MenuList>
                </Menu>



        <Menu closeOnSelect={false}>
            <MenuButton mr={4} as={Button} colorScheme="blue">
                Выбрать группы
            </MenuButton>
            <MenuList minWidth="240px">
                {SelectedTeacher.length > 0 && TeamsForSelectedTeacher ? 
                (
                    TeamsForSelectedTeacher.map((team) => (
                        <MenuItem key={team.id}>
                            <Checkbox
                                isChecked={SelectedTeam.includes(team.id)}
                                onChange={() => handleTeamSelect(team.id)}
                            >
                                {team.name}
                            </Checkbox>
                        </MenuItem>
                    ))
                ) : SelectedSpeciality.length > 0 && TeamsForSelectedSpeciality ? (
                    TeamsForSelectedSpeciality.map((team) => (
                        <MenuItem key={team.id}>
                            <Checkbox
                                isChecked={SelectedTeam.includes(team.id)}
                                onChange={() => handleTeamSelect(team.id)}
                            >
                                {team.name}
                            </Checkbox>
                        </MenuItem>
                    ))
                ) : (
                    TeamData && TeamData.map((team) => (
                        <MenuItem key={team.id}>
                            <Checkbox
                                isChecked={SelectedTeam.includes(team.id)}
                                onChange={() => handleTeamSelect(team.id)}
                            >
                                {team.name}
                            </Checkbox>
                        </MenuItem>
                    ))
                )}
            </MenuList>
        </Menu>

                <Menu closeOnSelect={false}>
            <MenuButton mr={4} as={Button} colorScheme="blue">
                Выбрать направления
            </MenuButton>
            <MenuList minWidth="240px">
                {SelectedTeacher.length > 0 && SpecialityForSelectedTeacher ? (
                    SpecialityForSelectedTeacher.map((spec) => (
                        <MenuItem key={spec.speciality}>
                            <Checkbox
                                isChecked={SelectedSpeciality.includes(spec.speciality)}
                                onChange={() => handleSpecialitySelect(spec.speciality)}
                            >
                                {spec.speciality}
                            </Checkbox>
                        </MenuItem>
                    ))
                ) : (
                    SpecialityData && SpecialityData.map((spec) => (
                        <MenuItem key={spec.speciality}>
                            <Checkbox
                                isChecked={SelectedSpeciality.includes(spec.speciality)}
                                onChange={() => handleSpecialitySelect(spec.speciality)}
                            >
                                {spec.speciality}
                            </Checkbox>
                        </MenuItem>
                    ))
                )}
            </MenuList> 
        </Menu> 
      </Flex> 

      

        <Box height={"380"}>

          {
            <AnalysKrFiltres 
          tokenUsers={userToken} 
          type={selectedModeFiltr} 
          kr={selectedKRFiltr} 
          teacher={SelectedTeacher.length > 0 ? SelectedTeacher : ''} 
          speciality={SelectedSpeciality.length > 0 ? SelectedSpeciality : ''} 
          team={SelectedTeam.length > 0 ? SelectedTeam : ''}/>}
        </Box>
        
        
        
    </Flex> 
    

    </>)

};
 
export default AnalysRr;