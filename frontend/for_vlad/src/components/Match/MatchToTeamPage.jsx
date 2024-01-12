import React, { useState,useEffect} from 'react';
import { Box, Flex, Select,Spacer ,Heading,Text,Button,  Menu, MenuButton, MenuList, MenuItem} from '@chakra-ui/react';
import { useAuth } from '../useAuth';
import { HamburgerIcon ,LockIcon ,CloseIcon,StarIcon,ArrowBackIcon, ArrowUpDownIcon} from '@chakra-ui/icons';
import { Link } from 'react-router-dom';
import { Tabs, TabList, TabPanels, Tab, TabPanel } from '@chakra-ui/react'

import MatchAttendanceTeams from './MatchAttendanceTeams';
import MatchTotalPointsTeams from './MatchTotalPointsTeams';

// просто пишем делаем запрос - по токену, блять его тоже передавать, крч пробуем токен передать, а потом запрос пишем и получаем data и засовываем в 2 селекта с проверкой на !одинаковые команды

const MatchToTeamPage = () => {
    const { userToken } = useAuth();
    const [userTeams, setUserTeams] = useState(null); // Новый стейт для данных о командах
    const [selectedTeam1, setSelectedTeam1] = useState(null);
    const [selectedTeam2, setSelectedTeam2] = useState(null);
    const [selectedTab, setSelectedTab] = useState(null);

    const handleTabChange = (tab) => {
      setSelectedTab(tab);
    }
  

    //  ПОЛУЧАЕМ ИНФУ О КОМАНДАХ ЮЗЕРА
    const fetchUserTeams = async () => {
    if (!userToken) {
      console.error('User token is missing');
      return;
    }
      try {
        // Отправляем GET-запрос для получения данных о командах пользователя
        const response = await fetch(`http://localhost:8090/api/get_teams_for_user?token=${userToken}`, {
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

  const handleTeamChange1 = (teamId) => {
    setSelectedTeam1(teamId);
  };

  const handleTeamChange2 = (teamId) => {
    setSelectedTeam2(teamId);
  };

 
return(

  <>
   <div className="container">
    <Menu >
      <MenuButton m={2} as={Button} rightIcon={<HamburgerIcon />}>
        Меню
      </MenuButton>
      <MenuList>
        <MenuItem icon={<CloseIcon />} as={Link} to="/">Выход</MenuItem> 
        <MenuItem icon={<StarIcon />} as={Link} to="/main">Основная страница</MenuItem>
        <MenuItem icon={<ArrowUpDownIcon />} as={Link} to={{ pathname: '/match2team', state: { teamForMatch: userTeams } }}>
          Сравнение</MenuItem>
        <MenuItem icon={<LockIcon />} >В Разработке</MenuItem>
      </MenuList>
    </Menu>

  </div>
  
  <Box p={6} w={[1200]} m="auto" mt={1}  borderWidth="3px" borderRadius="lg" boxShadow="xl" display="flex" alignItems="center">

  <Heading as="h2" size="lg" >
        Сравнение групп</Heading>
      <Text fontSize='xl' >Выберите группы для сравнения:</Text>
      
    <Flex justifyContent="space-between" width="100%">
      
    <Box  borderRadius="lg" boxShadow="lg">
      <Select colorScheme='twitter'
        placeholder="Выберите групп"
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

     

    <Box  borderRadius="lg" boxShadow="lg">
    <Select colorScheme='twitter'
      placeholder="Выберите группу"
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
  
  <Button as={Link} to="/main" leftIcon={<ArrowBackIcon />} colorScheme="twitter" ml={3}>Вернуться назад</Button>

</Flex>
</Box>

<Box p={6} w={[1000]} m="auto" mt={4}  borderWidth="3px" borderRadius="lg" boxShadow="xl" >

        <Text mb={4} fontSize='2xl' textAlign="center"> Выберите вариант отображения:</Text>

        <Tabs isFitted variant='enclosed' colorScheme='twitter'>
          
          <TabList>
            <Tab onClick={() => handleTabChange('match_attendance_for_teams')} >Посещаемость</Tab>
            <Tab onClick={() => handleTabChange('match_total_points_for_teams')} >Успеваемость</Tab> 
          </TabList>

          <TabPanels>
            <TabPanel>
              {selectedTab === 'match_attendance_for_teams' && <MatchAttendanceTeams teamId1={selectedTeam1} teamId2={selectedTeam2} />} 
            </TabPanel>

            <TabPanel>
              {selectedTab === 'match_total_points_for_teams' && <MatchTotalPointsTeams teamId1={selectedTeam1} teamId2={selectedTeam2} />}
            </TabPanel>
          </TabPanels>
        </Tabs>
      </Box>



</>
)
 


};

  
export default MatchToTeamPage;
  
  