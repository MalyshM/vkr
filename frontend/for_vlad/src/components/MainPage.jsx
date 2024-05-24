import { Flex, Box } from '@chakra-ui/react';
import React, { useState, useEffect } from 'react';
import { Select } from 'antd';
import { useAuth } from './useAuth';

import AtendenceTotalPoints from './chart/AtendenceTotalPoints';
import NumCountStudInLern from './chart/NumCountStudInLern';
import StataOfGroup from './chart/StataOfGroup';
import TableOfGroup from './chart/TableOfGroup';
import { fetchWithTokenRefresh } from './RefreshToken';

const { Option } = Select;


const MainPage = () => {
  const { userToken } = useAuth(); // Извлекаем userToken из контекста с помощью useAuth
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

      // ЗАПРОС - ПОЛУЧАЕМ ИНФУ О КОМАНДАХ ЮЗЕРА
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
      await fetchUserTeams();
      };
  
    if (userToken) {
      fetchData();
    }
  }, [userToken]);

  const handleTeamChange = (value) => {
    const selectedTeam = userTeams.find(team => team.id === value);
    setSelectedTeam(value);
    setSelectedTeamName(selectedTeam.name);
  };


  const handleLessonSelect = (lesson) => {
    setSelectedLessonMainPage(lesson);
  };


return (
  <Flex direction="column" minHeight="90vh">
    <Select
        style={{marginLeft:15, width: '270px', borderWidth: 1, fontFamily: 'Trebuchet MS',height: '40px', }}
        placeholder="Выберите вашу группу"
        onChange={handleTeamChange}
        value={selectedTeam}
        bordered={true}
      >
        {Array.isArray(userTeams) ? (
          userTeams.map((team) => (
            <Option key={team.id} value={team.id}>
              {team.name}
            </Option>
          ))
        ) : (
          <Option disabled>Группа не выбрана</Option>
        )}
      </Select>
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