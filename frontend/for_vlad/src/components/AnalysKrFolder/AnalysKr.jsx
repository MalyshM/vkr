import React, { useState,useEffect} from 'react';
import { Box, Flex, Select,Spacer ,Heading,Text,Button,  Menu, MenuButton, MenuList, MenuItem} from '@chakra-ui/react';
import { useAuth } from '../useAuth';
import { HamburgerIcon ,LockIcon ,CloseIcon,StarIcon,ArrowBackIcon, ArrowUpDownIcon} from '@chakra-ui/icons';
import { Link } from 'react-router-dom';
import { Tabs, TabList, TabPanels, Tab, TabPanel } from '@chakra-ui/react'

import AnalysKrSimple from './AnalysKrSimple'
import AnalysKrFiltres from './AnalysKrFiltres'


// просто пишем делаем запрос - по токену, блять его тоже передавать, крч пробуем токен передать, а потом запрос пишем и получаем data и засовываем в 2 селекта с проверкой на !одинаковые команды

const AnalysRr = () => {
    const { userToken } = useAuth();
    const [userTeams, setUserTeams] = useState(null); // Новый стейт для данных о командах

    const [selectedKR, setSelectedKR] = useState(null);
    const [KR, setKR] = useState(null);

    const [selectedNameTeacher, setSelectedNameTeacher] = useState(null);
    const [nameTeachers, setNameTeachers] = useState(null);

    const [selectedMode, setSelectedMode] = useState(0);



    //  ПОЛУЧАЕМ ИНФУ О КОМАНДАХ ЮЗЕРА
    const fetchUserTeams = async () => {
    if (!userToken) {
      console.error('User token is missing');
      return;
    }
      try {
        // Отправляем GET-запрос для получения данных о командах пользователя
        const response = await fetch(`http://localhost:8090/api/get_teams_for_user_without_lect?token=${userToken}`, {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${userToken}`, // Используем Authorization заголовок для GET-запроса
          },
        });

        if (response.ok) {
          const userTeamsData = await response.json();
          console.log('User Teams Data:', userTeamsData);
          setUserTeams(userTeamsData);
        } else {
          console.error('fetchUserTeams|AnalysRr - Failed to fetch user teams data');
        }
      } catch (error) {
        console.error('AnalysRr- Error during fetch user teams data:', error);
      }
  }


  const fetchNameKR = async () => {
  try {
    const response = await fetch('http://localhost:8090/api/get_all_kr');
    const result = await response.json();
    const nameKR = result;
    setKR(nameKR);

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

  useEffect(() => {
    const fetchData = async () => {
      await fetchUserTeams();
      await fetchNameKR();
      await fetchAllTeachers();
      
    }
    if (userToken) {
      // Если токен существует, запускаем запрос
      fetchData();
    }
  }, [userToken]);


  const handleKRChange = (value) => {
    setSelectedKR(value);
  };

  const handleNameTeachersChange = (value) => {
    setSelectedNameTeacher(value);
  }

  const handleModeChange = (event) => {
    const newMode = parseInt(event.target.value, 10);
    setSelectedMode(newMode);
  };

 
return( 
<>
  <Box p={6} display="flex" justifyContent={'space-between'}>
    <Heading as="h2" size="lg">Анализ Контрольных работ. Да ничего нету и что</Heading>

    <Box mr={4} w="250px" borderRadius="lg" boxShadow="lg">
          <Select borderColor='purple'
            placeholder="Выберите контрольную работу"
            onChange={(e) => handleKRChange(e.target.value)}
            value={selectedKR}>

            {Array.isArray(KR) ? (
              KR.map((task) => (
                <option key={task.name} value={task.name}>
                  {task.name}
                </option>
              ))
            ) : (
              <option disabled>No teams available</option>
            )}
          </Select>
        </Box>

        <Box mr={4} w="330px" borderRadius="lg" boxShadow="lg">
          <Select borderColor='purple'
            placeholder="Выберите преподавателя"
            onChange={(e) => handleNameTeachersChange(e.target.value)}
            value={selectedNameTeacher}>

            {Array.isArray(nameTeachers) ? (
              nameTeachers.map((teacher) => (
                <option key={teacher.name} value={teacher.name}>
                  {teacher.name}
                </option>
              ))
            ) : (
              <option disabled>No teams available</option>
            )}
          </Select>
        </Box>

        <Box mr={4} w="330px" borderRadius="lg" boxShadow="lg">
        <Select
            borderColor='purple'
            id="modeSelect"
            value={selectedMode}
            onChange={handleModeChange}
            placeholder="Выбери режим"
        >
            <option value={0}>По командам</option>
            <option value={1}>По направлениям</option>
            <option value={2}>По преподавателям</option>
        </Select>
        </Box>
    
    
    
    </Box>


    {/* <Flex direction={'column'} > */}

        <Box h={[380]}>
          {<AnalysKrSimple tokenUsers={userToken} type={selectedMode} kr={selectedKR} />}
          
            
        </Box>

        {/* <Box h={[380]}>
            {<AnalysKrFiltres tokenUsers={userToken} type={selectedMode} kr={selectedKR} />}
        </Box>
        
    </Flex> */}
    

    </>)

};
 
export default AnalysRr;