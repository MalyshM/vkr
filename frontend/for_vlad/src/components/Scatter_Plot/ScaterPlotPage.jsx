import React, { useState,useEffect} from 'react';
// import { useAuth } from 'D:/2newvkr/vkr_true/frontend/for_vlad/src/components/useAuth';
import ScaterPlotDiagram from './ScaterPlotDiagram'
import { useAuth } from '../useAuth';
import {fetchWithTokenRefresh} from '../RefreshToken'
// import { fetchWithTokenRefresh } from 'D:/2newvkr/vkr_true/frontend/for_vlad/src/components/RefreshToken';
import {Heading,Select,Box,Flex} from '@chakra-ui/react';

const ScaterPlotPage = () => {

    const { userToken } = useAuth();

    
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

    const [TeamData, SetTeamData] = useState(null); //save team on request
    const [SelectedTeam, setSelectedTeam] = useState(null); //save choise team after click

    const [TeacherData, SetTeacherData] = useState(null); // save teaher on request
    const [SelectedTeacher, setSelectedTeacher] = useState(null); //save choise team after click
    
    const [SpecialityData, SetSpecialityData] = useState(null); //save speciality on request
    const [SelectedSpeciality, setSelectedSpeciality] = useState(null); //save choise speciality after click

    const [SelectedMode, setSelectedMode] = useState(null);

    const [teacher_list] = useState();
    const [speciality_list] = useState();
    const [team_list] = useState();
    
  
    const handleTeamChange = (value) => {
        setSelectedTeam(value);};

    const handleTeacherChange = (value) => {
        setSelectedTeacher(value);};

    const handleSpecialityChange = (value) => {
        setSelectedSpeciality(value);};
  
    const handleModeChange = (event) => {
        const newMode = parseInt(event.target.value, 10);
        setSelectedMode(newMode);};
  
return( 
<>

<Heading p={4} as="h2" size="lg">Диаграмма рассеяния</Heading>

     <Flex 
    // minHeight="100vh"
    direction="column">

    <Box p={4} display="flex" justifyContent={'start'} >

            <Select mr={4} width='270px' borderWidth={1} fontFamily='Trebuchet MS'
                placeholder="Выберите группу"
                borderColor='black'
                // _active={{ borderColor: "black" }} 
                // _hover={{ color: "blue" }}
                // _selected={{ bg: "black.500", borderColor: "red.500", color: "white" }}
                onChange={(e) => handleTeamChange(e.target.value, e.target.selectedOptions[0].label)}
                disabled 
                value={SelectedTeam}>

                {Array.isArray(TeamData) ? (
                    TeamData.map((team) => (
                    <option key={team.id} value={team.id}>
                        {team.name}
                    </option>
                    ))
                ) : (
                    <option disabled>data is not arrive</option>
                )}
            </Select>

            <Select mr={4} width='270px' borderWidth={1} fontFamily='Trebuchet MS'
                placeholder="Выберите преподавателя"
                borderColor='black'
                _active={{ borderColor: "black" }} 
                _hover={{ color: "blue" }}
                _selected={{ bg: "black.500", borderColor: "red.500", color: "white" }}
                onChange={(e) => handleTeacherChange(e.target.value, e.target.selectedOptions[0].label)}

                value={SelectedTeacher}>

                {Array.isArray(TeacherData) ? (
                    TeacherData.map((teacher) => (
                    <option key={teacher.id} value={teacher.name}>
                        {teacher.name}
                    </option>
                    ))
                ) : (
                    <option disabled>data is not arrive</option>
                )}
            </Select>

            <Select width='270px' borderWidth={1} fontFamily='Trebuchet MS'
                placeholder="Выберите направление"
                borderColor='black'
                _active={{ borderColor: "black" }} 
                _hover={{ color: "blue" }}
                _selected={{ bg: "black.500", borderColor: "red.500", color: "white" }}
                onChange={(e) => handleSpecialityChange(e.target.value, e.target.selectedOptions[0].label)}

                value={SelectedSpeciality}>

                {Array.isArray(SpecialityData) ? (
                    SpecialityData.map((spec) => (
                    <option key={spec.speciality} value={spec.speciality}>
                        {spec.speciality}
                    </option>
                    ))
                ) : (
                    <option disabled>data is not arrive</option>
                )}
            </Select> 

            <Box ml={4} w="330px" borderRadius="lg" boxShadow="lg">
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

        </Box>
    

        <Box flex="1" p={2}>
            {SelectedMode && <ScaterPlotDiagram
            tokenUsers={userToken}
            type_group_by={SelectedMode} 
            teacher_list={SelectedTeacher}
            speciality_list={SelectedSpeciality}
            team_list={SelectedTeam} 
            />}

        </Box>
    
    </Flex>


    </>)
};
export default ScaterPlotPage;