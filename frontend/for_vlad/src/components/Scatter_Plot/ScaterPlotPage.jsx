import React, { useState,useEffect} from 'react';
import ScaterPlotDiagram from './ScaterPlotDiagram'
import ScaterPlotBySection from './ScaterPlotBySection';
import { useAuth } from '../useAuth';
import {fetchWithTokenRefresh} from '../RefreshToken'
import {Checkbox,Flex,Box,Select, Spacer ,Heading,Text,Button,  Menu, MenuButton, MenuList, MenuItem, Center } from '@chakra-ui/react';

import {Tooltip } from '@chakra-ui/react';
import { QuestionOutlineIcon } from '@chakra-ui/icons'

const ScaterPlotPage = () => {

    const { userToken } = useAuth();

    const [TeamData, SetTeamData] = useState(null); //storage team on request
    const [SelectedTeam, setSelectedTeam] = useState([]); //storage choise team after click
    const [TeamsForSelectedTeacher, setTeamsForSelectedTeacher] = useState(null) //storage teams for selected teacher
    const [TeamsForSelectedSpeciality, setTeamsForSelectedSpeciality] = useState(null); //storage arr teams of choise speciality


    const [TeacherData, SetTeacherData] = useState(null); // storage teaher on request
    const [SelectedTeacher, setSelectedTeacher] = useState([]); //storage choise team after click
    const [TeachersForSelectedSpeciality, setTeachersForSelectedSpeciality] = useState(null); //storage arr teachers of choise speciality

    const [SpecialityData, SetSpecialityData] = useState(null); //storage speciality on request
    const [SelectedSpeciality, setSelectedSpeciality] = useState([]); //storage choise speciality after click
    const [SpecialityForSelectedTeacher, setSpecialityForSelectedTeacher] = useState(null) //storage speciality for selected teacher

    const [CheckboxOne, setCheckboxOne] = useState(false);
    const [CheckboxMany, setCheckboxMany] = useState(false);


    const [SelectedMode, setSelectedMode] = useState(null);
    
    const fetchTeamForTeacher = async () => {
        try {
          const response = await fetchWithTokenRefresh(`http://moais-dashboard.ru:8082/api/get_teams_for_user_without_lect?token=${userToken}`);
          const result = await response.json();
          SetTeamData(result);
        //   console.log('fetchTeamForTeacher:', result);
      } catch (error) {
          console.error('Error fetching data from fetchTeamForTeacher:', error);
        }
      };

      const fetchSpecialityForTeacher = async () => {
        try {
          const response = await fetchWithTokenRefresh(`http://moais-dashboard.ru:8082/api/get_all_specialities?token=${userToken}`);
          const result = await response.json();
          SetSpecialityData(result);
        //   console.log('fetchSpecialityForTeacher:', result);
      } catch (error) {
          console.error('Error fetching data from fetchSpecialityForTeacher:', error);
        }
      };

      const fetchTeacher = async () => {
        try {
          const response = await fetchWithTokenRefresh(`http://moais-dashboard.ru:8082/api/get_all_teachers_unique?token=${userToken}`);
          const result = await response.json();
          SetTeacherData(result);
        //   console.log('fetchTeacher:', result);
      } catch (error) {
          console.error('Error fetching data from fetchTeacher:', error);
        }
      };

      const fetchTeamForChoiseTeacher = async () => {
        try {
          const response = await fetchWithTokenRefresh(`http://moais-dashboard.ru:8082/api/get_teams_for_param_without_lect?teacher_arr=${SelectedTeacher}`);
          const result = await response.json();
          setTeamsForSelectedTeacher(result);
        //   console.log('fetchTeamForChoiseTeacher:', result);
      } catch (error) {
          console.error('Error fetching data from fetchTeamForChoiseTeacher:', error);
        }
      };

      const fetchSpecialityForChoiseTeacher = async () => {
        try {
          const response = await fetchWithTokenRefresh(`http://moais-dashboard.ru:8082/api/get_all_specialities_by_teacher_arr?token=${userToken}&teacher_list=${SelectedTeacher}`);
          const result = await response.json();
          setSpecialityForSelectedTeacher(result);
        //   console.log('fetchSpecialityForChoiseTeacher:', result);
      } catch (error) {
          console.error('Error fetching data from fetchSpecialityForChoiseTeacher:', error);
        }
      };

      const fetchTeacherForChoiseSpeciality = async () => {
        try {
          const response = await fetchWithTokenRefresh(`http://moais-dashboard.ru:8082/api/get_all_teachers_by_speciality_arr?token=${userToken}&speciality_list=${SelectedSpeciality}`);
          const result = await response.json();
          setTeachersForSelectedSpeciality(result);
        //   console.log('fetchTeamForChoiseTeacher:', result);
      } catch (error) {
          console.error('Error fetching data from fetchTeacherForChoiseSpeciality:', error);
        }
      };

      const fetchTeamsForChoiseSpeciality = async () => {
        try {
          const response = await fetchWithTokenRefresh(`http://moais-dashboard.ru:8082/api/get_all_teams_by_speciality_arr?token=${userToken}&speciality_list=${SelectedSpeciality}`);
          const result = await response.json();
          setTeamsForSelectedSpeciality(result);
        //   console.log('fetchSpecialityForChoiseTeacher:', result);
      } catch (error) {
          console.error('Error fetching data from fetchTeamsForChoiseSpeciality:', error);
        }
      };

      useEffect(() => {
        const fetchData = async () => {
          await fetchTeamForTeacher();
          await fetchSpecialityForTeacher();
          await fetchTeacher();
          
        }
        if (userToken) 
            {fetchData();} 
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
        

    const handleCheckboxOneChange = (event) => {
        setCheckboxOne(event.target.checked);
        };
    
        const handleCheckboxManyChange = (event) => {
        setCheckboxMany(event.target.checked);
        };
        

    const handleTeacherSelect = (teacherId) => {
        if (SelectedTeacher.includes(teacherId)) {
            setSelectedTeacher(SelectedTeacher.filter((id) => id !== teacherId));
        } else {
            setSelectedTeacher([...SelectedTeacher, teacherId]);
        }
        console.log('SelectedTeacher',SelectedTeacher)
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
  
    const handleModeChange = (event) => { // FOR CHOISE MODE 1 2 3  
        const newMode = parseInt(event.target.value, 10);
        setSelectedMode(newMode);};


return( 
<>
<Box p={4} display="flex" justifyContent={'start'} alignItems={'center'} >

    <Heading 
        p={4} 
        as="h2" 
        size="lg"
    >Диаграмма рассеяния

        <Tooltip label="Диаграмма отображающая взаимосвязь между успеваемостью и посещаемостью" aria-label="A tooltip">
            <QuestionOutlineIcon ml={2} boxSize={4} cursor="pointer" />
        </Tooltip>

    </Heading>

            <Box mr={4}>
                <Checkbox mr={4} 
                isChecked={CheckboxOne} 
                onChange={handleCheckboxOneChange}
                >
                Общий график
                </Checkbox>
                
                <Checkbox 
                isChecked={CheckboxMany} 
                onChange={handleCheckboxManyChange}
                >
                N-диаграмм
                </Checkbox>
            </Box>

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
                        Выбрать преподавателей
                    </MenuButton>
                    <MenuList minWidth="240px">
                    { SelectedSpeciality.length > 0 && TeachersForSelectedSpeciality ? (
                            TeachersForSelectedSpeciality.map((team) => (
                                <MenuItem key={team.id}>
                                    <Checkbox
                                        isChecked={SelectedTeacher.includes(team.id)}
                                        onChange={() => handleTeacherSelect(team.id)}
                                    >
                                        {team.name}
                                    </Checkbox>
                                </MenuItem>
                            ))
                        ) : (
                    TeacherData && TeacherData.map((teacher) => (
                        <MenuItem key={teacher.id}>
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
                Выбрать направления
            </MenuButton>
            <MenuList minWidth="240px">
                {SelectedTeacher.length > 0 && SpecialityForSelectedTeacher ? (
                    SpecialityForSelectedTeacher.map((spec) => (
                        <MenuItem key={spec.id}>
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
                        <MenuItem key={spec.id}>
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
        </Box>

        {/* <Flex> */}
        <Box flex="1" p={2}>
            {SelectedMode && <ScaterPlotDiagram
            CheckboxMany={CheckboxMany}
            CheckboxOne={CheckboxOne}
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
        {/* </Flex> */}
    


    </>)
};
export default ScaterPlotPage;