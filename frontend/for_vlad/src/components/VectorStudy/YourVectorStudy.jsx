import React, { useState,useEffect} from 'react';
import { Box, Flex, Select,Spacer ,Heading,Text,Button,  Menu, MenuButton, MenuList, MenuItem} from '@chakra-ui/react';
import { useAuth } from '../useAuth';
import { HamburgerIcon ,LockIcon ,CloseIcon,StarIcon,ArrowBackIcon, ArrowUpDownIcon} from '@chakra-ui/icons';
import { Link } from 'react-router-dom';
import { Tabs, TabList, TabPanels, Tab, TabPanel } from '@chakra-ui/react'

import VecStudyAllUsersAt from './VecStudyAllUsersAt';
import VecStudyAllUsersTP from './VecStudyAllUsersTP';

// просто пишем делаем запрос - по токену, блять его тоже передавать, крч пробуем токен передать, а потом запрос пишем и получаем data и засовываем в 2 селекта с проверкой на !одинаковые команды

const YourVectorStudy = () => {
    const { userToken } = useAuth();
    const [userTeams, setUserTeams] = useState(null); // Новый стейт для данных о командах

    

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
          console.error('VecStudy_MATCH2TEAM - Failed to fetch user teams data');
        }
      } catch (error) {
        console.error('VecStudy_MATCH2TEAM- Error during fetch user teams data:', error);
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
 
return( 
<>
  <Box p={6} display="flex" justifyContent={'space-between'}>
    <Heading as="h2" size="lg">Ваши направления</Heading>
    
    
    </Box>

  

    <Flex direction={'column'} >

        <Box h={[380]}>
            {<VecStudyAllUsersAt tokenUsers={userToken}/>}
        </Box>

        <Box h={[380]}>
            {<VecStudyAllUsersTP tokenUsers={userToken}/>}
        </Box>
        
    </Flex>
    

    </>)

};
 
export default YourVectorStudy;