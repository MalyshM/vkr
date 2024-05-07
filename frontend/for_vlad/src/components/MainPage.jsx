import React, { useState, useEffect } from 'react';
import { useAuth } from './useAuth';

import { Flex, Box, Select, Avatar } from '@chakra-ui/react';
import { useDisclosure } from '@chakra-ui/react'

import { Tooltip } from '@chakra-ui/react'

import AtendenceTotalPoints from './chart/AtendenceTotalPoints';
import NumCountStudInLern from './chart/NumCountStudInLern';
import StataOfGroup from './chart/StataOfGroup';
import TableOfGroup from './chart/TableOfGroup';

import { fetchWithTokenRefresh } from './RefreshToken';

const MainPage = () => {
  const [isHovered, setIsHovered] = useState(false);
  const { userToken } = useAuth(); // Извлекаем userToken из контекста с помощью useAuth
  const [userData, setUserData] = useState(null); // Стейт для хранения данных пользователя
  const [userTeams, setUserTeams] = useState(null); // Новый стейт для данных о командах
  
  const [selectedTeam, setSelectedTeam] = useState(null); //Данные о посещаемости
  const [selectedTeamName, setSelectedTeamName] = useState(null);

  const [selectedLessonMainPage, setSelectedLessonMainPage] = useState(null);

    // ПОЛУЧИЛИ ИНФУ ОБ ЮЗЕРЕ (1 ЗАПРОС)

    const fetchUserTeams = async () => {
      if (!userToken) {
        console.error('User token is missing');
        return;
      }

      // 2 ЗАПРОС - ПОЛУЧАЕМ ИНФУ О КОМАНДАХ ЮЗЕРА
      try {
        // Отправляем GET-запрос для получения данных о командах пользователя
        const response = await fetchWithTokenRefresh(`http://moais-dashboard.ru:8082/api/get_teams_for_user_without_lect?token=${userToken}`, {
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
          console.error('Failed to fetch user teams data');
        }
      } catch (error) {
        console.error('Error during fetch user teams data:', error);
      }
    };

   
    
  useEffect(() => {
    const fetchData = async () => {
      // Функция для запуска запроса, вызывается при монтировании компонент
      // await fetchUserData();
      await fetchUserTeams();
      };
  
    if (userToken) {
      // Если токен существует, запускаем запрос
      fetchData();
    }
  }, [userToken]);

  const handleTeamChange = (teamId,teamName) => {
    setSelectedTeam(teamId);
    setSelectedTeamName(teamName);
   
  };

  const handleLessonSelect = (lesson) => {
    setSelectedLessonMainPage(lesson);
  };

  const handleMouseEnter = () => {
    setIsHovered(true);
  };

  const handleMouseLeave = () => {
    setIsHovered(false);
  };

  console.log('isHovered:', isHovered);
  console.log('userData:', userData);

  const getRoleTooltip = (userData) => {
    if (!userData) {
      return null;
    }
  
    const roles = [];
    if (userData.isadmin) {
      roles.push('Администратор');
    }
    if (userData.iscurator) {
      roles.push('Куратор');
    }
    if (userData.isteacher) {
      roles.push('Учитель');
    }
  
    return roles.length > 0 ? `${userData.fio}, Вы вошли как: ${roles.join(', ')}` : 'Без ролей';
  };
  

return (
  <Flex direction="column" minHeight="90vh">
    
    <Flex justifyContent="flex-end" alignItems="center" p={2}>
      <Select width='270px' borderWidth={1} fontFamily='Trebuchet MS'
        placeholder="Выберите вашу группу"
        borderColor='black'
        _active={{ borderColor: "black" }} 
        _hover={{ color: "blue" }}
        _selected={{ bg: "black.500", borderColor: "red.500", color: "white" }}
        onChange={(e) => handleTeamChange(e.target.value, e.target.selectedOptions[0].label)}
        value={selectedTeam}>
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

      <Tooltip mr={4} borderRadius='lg' fontFamily='Trebuchet MS' label={getRoleTooltip(userData)} fontSize='md'>
        <Avatar bg='gray.500' ml={3} mr={3} 
          onMouseEnter={() => console.log('Mouse entered')}
          onMouseLeave={() => console.log('Mouse left')}
        />
      </Tooltip>
    </Flex>

    <Flex flex="1" flexDirection={{ base: 'column', md: 'row' }}>
      <Box flex="1" minWidth={{ base: '100%', md: '70%' }} p={4}>
        {selectedTeam && <AtendenceTotalPoints teamId={selectedTeam} teamName={selectedTeamName} />}
      </Box>

      <Box flex="1" minWidth={{ base: '100%', md: '30%' }} p={4}>
        {selectedTeam && <StataOfGroup teamId={selectedTeam} teamName={selectedTeamName} />}
      </Box>
    </Flex>

    <Flex flex="1" flexDirection={{ base: 'column', md: 'row' }}>
      <Box flex="1" minWidth={{ base: '100%', md: '60%' }} p={4}>
        {selectedTeam && <NumCountStudInLern teamId={selectedTeam} teamName={selectedTeamName} onLessonSelect={handleLessonSelect} />}
      </Box>

      <Box flex="1" minWidth={{ base: '100%', md: '40%' }} p={4}>
        {selectedTeam && <TableOfGroup teamName={selectedTeamName} teamId={selectedTeam} selectedLesson={selectedLessonMainPage}/>}
      </Box>
    </Flex>
  </Flex>
);


    };


export default MainPage;