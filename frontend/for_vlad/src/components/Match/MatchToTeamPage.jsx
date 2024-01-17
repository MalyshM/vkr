import React, { useState,useEffect} from 'react';
import { Box, Flex, Select,Spacer ,Heading,Text,Button,  Menu, MenuButton, MenuList, MenuItem} from '@chakra-ui/react';
import { useAuth } from '../useAuth';
import { HamburgerIcon ,LockIcon ,CloseIcon,StarIcon,ArrowBackIcon, ArrowUpDownIcon} from '@chakra-ui/icons';
import { Link } from 'react-router-dom';
import { Tabs, TabList, TabPanels, Tab, TabPanel } from '@chakra-ui/react'

import MatchAttendanceTeams from './MatchAttendanceTeams';
import MatchTotalPointsTeams from './MatchTotalPointsTeams';
import AllUsersAtenadance from './AllUsersAtenadance';
import AllUsersTotalPoint from './AllUsersTotalPoint';

// просто пишем делаем запрос - по токену, блять его тоже передавать, крч пробуем токен передать, а потом запрос пишем и получаем data и засовываем в 2 селекта с проверкой на !одинаковые команды

const MatchToTeamPage = () => {
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

    {/* <Button as={Link} to="/main" leftIcon={<ArrowBackIcon />} colorScheme="twitter" ml={3}>Вернуться назад</Button> */}

    <Heading as="h2" size="lg">Сравнение групп</Heading>

    <Flex direction={'column'} alignItems="center">
      <Text fontSize='xl'>Выберите группы для сравнения:</Text>

      <Flex p={2}>
        <Box mr={4} w="220px" borderRadius="lg" boxShadow="lg">
          <Select borderColor='purple'
            placeholder="Выберите 1-ю группу"
            onChange={(e) => handleTeamChange1(e.target.value)}
            value={selectedTeam1}>

            {Array.isArray(userTeams) ? (
              userTeams.map((team) => (
                <option key={team.id} value={team.id}>
                  {team.name}
                </option>
              ))
            ) : (
              <option disabled>No teams available</option>
            )}
          </Select>
        </Box>

        <Box w="220px" borderRadius="lg" boxShadow="lg">
          <Select borderColor='purple'
            placeholder="Выберите 2-ю группу"
            onChange={(e) => handleTeamChange2(e.target.value)}
            value={selectedTeam2}>

            {Array.isArray(userTeams) ? (
              userTeams.map((team) => (
                <option key={team.id} value={team.id}>
                  {team.name}
                </option>
              ))
            ) : (
              <option disabled>No teams available</option>
            )}
          </Select>
        </Box>
      </Flex>
    </Flex>

  </Box>
           {/*  */}

      

  <Flex direction={'column'} >

      <Box h={[380]}>
      {<AllUsersAtenadance tokenUsers={userToken}/>}
        {selectedTeam1 && selectedTeam2 && (
          <MatchAttendanceTeams teamId1={selectedTeam1} teamId2={selectedTeam2} />
        )}
      </Box>

    <Box h={[380]}>
    {<AllUsersTotalPoint tokenUsers={userToken}/>}
      {selectedTeam1 && selectedTeam2 && (
        <MatchTotalPointsTeams teamId1={selectedTeam1} teamId2={selectedTeam2} />
      )}
    </Box>
  </Flex>

    

    </>)

};
 
export default MatchToTeamPage;
  
  