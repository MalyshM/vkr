import React, { useState,useEffect} from 'react';
import ScaterPlotDiagram from './ScaterPlotDiagram'
import ScaterPlotBySection from './ScaterPlotBySection';
import { useAuth } from '../useAuth';
import {fetchWithTokenRefresh} from '../RefreshToken'
import {Checkbox,Flex,Box,Select, Spacer ,Heading,Text,Button,  Menu, MenuButton, MenuList, MenuItem, Center} from '@chakra-ui/react';

const ScaterPlotPage = () => {

    const { userToken } = useAuth();

    const [TeamData, SetTeamData] = useState(null); //save team on request
    const [SelectedTeam, setSelectedTeam] = useState([]); //save choise team after click

    const [TeacherData, SetTeacherData] = useState(null); // save teaher on request
    const [SelectedTeacher, setSelectedTeacher] = useState([]); //save choise team after click
    
    const [SpecialityData, SetSpecialityData] = useState(null); //save speciality on request
    const [SelectedSpeciality, setSelectedSpeciality] = useState([]); //save choise speciality after click

    const [SelectedMode, setSelectedMode] = useState(null);

    
    const fetchTeamForTeacher = async () => {
        try {
          const response = await fetchWithTokenRefresh(`http://moais-dashboard.ru:8082/api/get_teams_for_user_without_lect?token=${userToken}`);
          const result = await response.json();
          SetTeamData(result);
      
          console.log('fetchTeamForTeacher:', result);
      
      } catch (error) {
          console.error('Error fetching data from fetchTeamForTeacher:', error);
        }
      };

      const fetchSpecialityForTeacher = async () => {
        try {
          const response = await fetchWithTokenRefresh(`http://moais-dashboard.ru:8082/api/get_all_specialities?token=${userToken}`);
          const result = await response.json();
          SetSpecialityData(result);
      
          console.log('fetchSpecialityForTeacher:', result);
      
      } catch (error) {
          console.error('Error fetching data from fetchSpecialityForTeacher:', error);
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

      useEffect(() => {
        const fetchData = async () => {
          await fetchTeamForTeacher();
          await fetchSpecialityForTeacher();
          await fetchTeacher();
         
          
        }
    
        if (userToken) {
          fetchData();
        }
      }, [userToken]);

    // const handleTeamChange = (value) => {
    //     setSelectedTeam(value);};

    // const handleTeacherChange = (value) => {
    //     setSelectedTeacher(value);};

    const handleTeacherSelect = (teacherId) => {
        if (SelectedTeacher.includes(teacherId)) {
            setSelectedTeacher(SelectedTeacher.filter((id) => id !== teacherId));
        } else {
            setSelectedTeacher([...SelectedTeacher, teacherId]);
        }
    };

    const handleTeamSelect = (team_id) => {
        if (SelectedTeam.includes(team_id)) {
            setSelectedTeam(SelectedTeam.filter((id) => id !== team_id));
        } else {
            setSelectedTeam([...SelectedTeam, team_id]);
        }
    };

    const handleSpecialitySelect = (speciality) => {
        if (SelectedSpeciality.includes(speciality)) {
            setSelectedSpeciality(SelectedSpeciality.filter((speciality) => speciality !== speciality));
        } else {
            setSelectedSpeciality([...SelectedSpeciality, speciality]);
        }
    };

 
    // const handleSpecialityChange = (value) => {
    //     setSelectedSpeciality(value);};
  
    const handleModeChange = (event) => {
        const newMode = parseInt(event.target.value, 10);
        setSelectedMode(newMode);};
  
return( 
<>
<Box p={4} display="flex" justifyContent={'start'} alignItems={'center'} >

<Heading p={4} as="h2" size="lg">Диаграмма рассеяния</Heading>

            <Box mr={4} borderRadius="lg" boxShadow="l">
                <Select 
                    borderColor='black'
                    _active={{ borderColor: "black" }} 
                        _hover={{ color: "blue" }}
                        _selected={{ bg: "black.500", borderColor: "red.500", color: "white" }}
                    id="modeSelectSimple"
                    value={SelectedMode}
                    onChange={handleModeChange}
                    placeholder="Выбери режим"
                >
                    <option value={3}>По группам</option>
                    <option value={1}>По направлениям</option>
                    <option value={2}>По преподавателям</option>
                </Select>
            </Box>

                <Menu closeOnSelect={false}>
                    <MenuButton mr={4} as={Button} colorScheme="blue">
                        Выбрать группы
                    </MenuButton>
                    <MenuList minWidth="240px">
                    {TeamData && TeamData.map((team) => (
                        <MenuItem key={team.id}>
                            <Checkbox
                            isChecked={SelectedTeam.includes(team.id)}
                            onChange={() => handleTeamSelect(team.id)}
                            >
                            {team.name}
                            </Checkbox>
                        </MenuItem>
                        ))}
                    </MenuList>
                </Menu>

                <Menu closeOnSelect={false}>
                    <MenuButton mr={4} as={Button} colorScheme="blue">
                        Выбрать преподавателей
                    </MenuButton>
                    <MenuList minWidth="240px">
                    {TeacherData && TeacherData.map((teacher) => (
                        <MenuItem key={teacher.id}>
                            <Checkbox
                            isChecked={SelectedTeacher.includes(teacher.name)}
                            onChange={() => handleTeacherSelect(teacher.name)}
                            >
                            {teacher.name}
                            </Checkbox>
                        </MenuItem>
                        ))}
                    </MenuList>
                </Menu>


                <Menu closeOnSelect={false}>
                    <MenuButton
                        mr={4}
                        as={Button}
                        colorScheme="blue"
                        isDisabled={true}
                    >
                        Выбрать направления
                    </MenuButton>
                    <MenuList minWidth="240px">
                        {SpecialityData && SpecialityData.map((spec) => (
                            <MenuItem key={spec.id}>
                                <Checkbox
                                    isChecked={SelectedSpeciality.includes(spec.speciality)}
                                    onChange={() => handleTeacherSelect(spec.speciality)}
                                    isDisabled={true}
                                >
                                    {spec.speciality}
                                </Checkbox>
                            </MenuItem>
                        ))}
                    </MenuList>
                </Menu>
        </Box>

        <Flex>
        <Box flex="1" p={2}>
            {SelectedMode && <ScaterPlotDiagram
            tokenUsers={userToken}
            type_group_by={SelectedMode} 
            teacher_list={SelectedTeacher.length > 0 ? SelectedTeacher : ''}
            speciality_list={SelectedSpeciality.length > 0 ? SelectedSpeciality : ''}
            team_list={SelectedTeam.length > 0 ? SelectedTeam : ''}

            />}

        </Box>

        <Box flex="1" p={2}>
            {SelectedMode && <ScaterPlotBySection
            tokenUsers={userToken}
            type_group_by={SelectedMode} 
            teacher_list={SelectedTeacher.length > 0 ? SelectedTeacher : ''}
            speciality_list={SelectedSpeciality.length > 0 ? SelectedSpeciality : ''}
            team_list={SelectedTeam.length > 0 ? SelectedTeam : ''}

            />}

        </Box>
        </Flex>
    


    </>)
};
export default ScaterPlotPage;