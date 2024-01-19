import React, { useState,useEffect} from 'react';
import { Box, Flex, Select ,Heading} from '@chakra-ui/react';
import { useAuth } from '../useAuth';

import AnalysKrSimple from './AnalysKrSimple'
import AnalysKrFiltres from './AnalysKrFiltres'


// просто пишем делаем запрос - по токену, блять его тоже передавать, крч пробуем токен передать, а потом запрос пишем и получаем data и засовываем в 2 селекта с проверкой на !одинаковые команды

const AnalysRr = () => {
    const { userToken } = useAuth();
    const [userTeams, setUserTeams] = useState(null); // Новый стейт для данных о командах

    const [selectedNameTeacher, setSelectedNameTeacher] = useState(null);
    const [nameTeachers, setNameTeachers] = useState(null);

    const [speciality, setSpeciality] = useState(null);
    const [selectedSpeciality, setSelectedSpeciality] = useState(null);

    const [team, setTeam] = useState(null);
    const [selectedTeam, setSelectedTeam] = useState(null);




    const [selectedKRSimple, setSelectedKRSimple] = useState(null);
    const [KRSimple, setKRSimple] = useState(null);

    const [selectedKRFiltr, setSelectedKRFiltr] = useState(null);
    const [KRFiltr, setKRFiltr] = useState(null);

    const [selectedModeSimple, setSelectedModeSimple] = useState(null);
    const [selectedModeFiltr, setSelectedModeFiltr] = useState(null);

  //   //  ПОЛУЧАЕМ ИНФУ О КОМАНДАХ ЮЗЕРА
  //   const fetchUserTeams = async () => {
  //   if (!userToken) {
  //     console.error('User token is missing');
  //     return;
  //   }
  //     try {
  //       // Отправляем GET-запрос для получения данных о командах пользователя
  //       const response = await fetch(`http://localhost:8090/api/get_teams_for_user_without_lect?token=${userToken}`, {
  //         method: 'GET',
  //         headers: {
  //           'Content-Type': 'application/json',
  //           'Authorization': `Bearer ${userToken}`, // Используем Authorization заголовок для GET-запроса
  //         },
  //       });

  //       if (response.ok) {
  //         const userTeamsData = await response.json();
  //         console.log('User Teams Data:', userTeamsData);
  //         setUserTeams(userTeamsData);
  //       } else {
  //         console.error('fetchUserTeams|AnalysRr - Failed to fetch user teams data');
  //       }
  //     } catch (error) {
  //       console.error('AnalysRr- Error during fetch user teams data:', error);
  //     }
  // }


  const fetchNameKR = async () => {
  try {
    const response = await fetch('http://localhost:8090/api/get_all_kr');
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
      const response = await fetch(`http://localhost:8090/api/get_all_teachers?token=${userToken}`);
      const result = await response.json();
      setNameTeachers(result);
  
      console.log('Data from fetchAllTeachers:', result);
  
  } catch (error) {
      console.error('Error fetching data from fetchAllTeachers:', error);
    }
  };

  const fetchAllSpeciality = async () => {
    try {
      const response = await fetch(`http://localhost:8090/api/get_all_specialities?token=${userToken}`);
      const result = await response.json();
      setSpeciality(result);
  
      console.log('Data from fetchAllSpeciality:', result);
  
  } catch (error) {
      console.error('Error fetching data from fetchAllSpeciality:', error);
    }
  };

  const fetchAllTeam = async () => {
    try {
      const response = await fetch(`http://localhost:8090/api/get_teams_for_user_without_lect?token=${userToken}`);
      const result = await response.json();
      setTeam(result);
  
      console.log('Data from fetchAllTeam:', result);
  
  } catch (error) {
      console.error('Error fetching data from fetchAllTeam:', error);
    }
  };

  useEffect(() => {
    const fetchData = async () => {
      // await fetchUserTeams();
      await fetchNameKR();
      await fetchAllTeachers();
      await fetchAllSpeciality();
      await fetchAllTeam();
      
    }

    if (userToken) {
      fetchData();
    }
  }, [userToken]);


  const handleKRChangeSimple = (value) => {
    setSelectedKRSimple(value);
  };

  const handleKRChangeFiltr = (value) => {
    setSelectedKRFiltr(value);
  };

  const handleNameTeachersChange = (value) => {
    setSelectedNameTeacher(value);
  }

  const handleModeChangeSimple = (event) => {
    const newMode = parseInt(event.target.value, 10);
    setSelectedModeSimple(newMode);
  };

  const handleModeChangeFiltr = (event) => {
    const newMode = parseInt(event.target.value, 10);
    setSelectedModeFiltr(newMode);
  };

  const handleSpecialityChange = (value) => {
    setSelectedSpeciality(value);
  }

  const handleTeamChange = (value) => {
    setSelectedTeam(value);
  }

 
return( 
<>
  <Box p={6} display="flex" justifyContent={'space-between'}>
    <Heading as="h1" size="lg">Анализ Контрольных работ</Heading>

    <Box mr={4} w="250px" borderRadius="lg" boxShadow="lg">
          <Select borderColor='purple'
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
            borderColor='purple'
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
          <Select borderColor='purple'
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
            borderColor='purple'
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
  



        <Box w="360px" borderRadius="lg" boxShadow="lg" mr={3}>
          <Select borderColor='purple'
            placeholder="Дополнительно выберите преподавателя"
            onChange={(e) => handleNameTeachersChange(e.target.value)}
            value={selectedNameTeacher}>

            {Array.isArray(nameTeachers) ? (
              nameTeachers.map((teacher) => (
                <option key={teacher.name} value={teacher.name}>
                  {teacher.name}
                </option>
              ))
            ) : (
              <option disabled>No teacher available</option>
            )}
          </Select>
        </Box>

        <Box  w="330px" borderRadius="lg" boxShadow="lg" mr={3}>
          <Select borderColor='purple'
            placeholder="Дополнительно выберите направление"
            onChange={(e) => handleSpecialityChange(e.target.value)}
            value={selectedSpeciality}>

            {Array.isArray(speciality) ? (
              speciality.map((spec) => (
                <option key={spec.speciality} value={spec.speciality}>
                  {spec.speciality}
                </option>
              ))
            ) : (
              <option disabled>No speciality available</option>
            )}
          </Select>
        </Box>

        <Box  w="330px" borderRadius="lg" boxShadow="lg" mr={3}>
          <Select borderColor='purple'
            placeholder="Дополнительно выберите группу"
            onChange={(e) => handleTeamChange(e.target.value)}
            value={selectedTeam}>

            {Array.isArray(team) ? (
              team.map((team_) => (
                <option key={team_.name} value={team_.name}>
                  {team_.name}
                </option>
              ))
            ) : (
              <option disabled>No teams available</option>
            )}
          </Select>
        </Box>
      </Flex>

      

        <Box height={"380"}>

          {<AnalysKrFiltres tokenUsers={userToken} type={selectedModeFiltr} kr={selectedKRFiltr} teacher={selectedNameTeacher} speciality={selectedSpeciality} team={selectedTeam}/>}
        </Box>
        
        
        
    </Flex> 
    

    </>)

};
 
export default AnalysRr;