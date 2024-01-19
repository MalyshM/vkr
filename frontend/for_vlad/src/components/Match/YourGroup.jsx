import React, { useState,useEffect} from 'react';
import { Box, Flex, Select,Spacer ,Heading,Text,Button,  Menu, MenuButton, MenuList, MenuItem} from '@chakra-ui/react';
import { useAuth } from '../useAuth';
import { HamburgerIcon ,LockIcon ,CloseIcon,StarIcon,ArrowBackIcon, ArrowUpDownIcon} from '@chakra-ui/icons';
import { Link } from 'react-router-dom';
import { Tabs, TabList, TabPanels, Tab, TabPanel } from '@chakra-ui/react'

import AllUsersAtenadance from './AllUsersAtenadance';
import AllUsersTotalPoint from './AllUsersTotalPoint';

// просто пишем делаем запрос - по токену, блять его тоже передавать, крч пробуем токен передать, а потом запрос пишем и получаем data и засовываем в 2 селекта с проверкой на !одинаковые команды

const YourGroup = () => {
    const { userToken } = useAuth();
    const [userTeams, setUserTeams] = useState(null); // Новый стейт для данных о командах

    const [selectedTeam1, setSelectedTeam1] = useState(null);
    const [selectedTeam2, setSelectedTeam2] = useState(null);


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
          console.error('MATCH2TEAM - Failed to fetch user teams data');
        }
      } catch (error) {
        console.error('MATCH2TEAM- Error during fetch user teams data:', error);
      }
  } 

  useEffect(() => {
    const fetchData = async () => {
      await fetchUserTeams();
      
    }
    if (userToken) {
      // Если токен существует, запускаем запрос
      fetchData();
    }
  }, [userToken]);

  // const handleTeamChange1 = (teamId) => {
  //   setSelectedTeam1(teamId);
  // };

  // const handleTeamChange2 = (teamId) => {
  //   setSelectedTeam2(teamId);
  // };

  const handleTeamChange1 = (value) => {
    setSelectedTeam1(value);
   
  };

  const handleTeamChange2 = (value) => {
    setSelectedTeam2(value);
   
  };

 
return( 
<>
  <Box p={6} display="flex" justifyContent={'space-between'}>
    <Heading as="h2" size="lg">Ваши группы</Heading>
    
    
    </Box>

  

    <Flex direction={'column'} >

        <Box h={[380]}>
            {<AllUsersAtenadance tokenUsers={userToken}/>}
        </Box>

        <Box h={[380]}>
            {<AllUsersTotalPoint tokenUsers={userToken}/>}
        </Box>
        
    </Flex>
    

    </>)

};
 
export default YourGroup;