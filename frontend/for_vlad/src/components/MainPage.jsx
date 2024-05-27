import React, { useState, useEffect,useRef  } from 'react';
import { Flex, Box } from '@chakra-ui/react';
import { Select , notification } from 'antd';
import { useNavigate, useParams } from 'react-router-dom';
import { useAuth } from './useAuth';
import AtendenceTotalPoints from './chart/AtendenceTotalPoints';
import NumCountStudInLern from './chart/NumCountStudInLern';
import StataOfGroup from './chart/StataOfGroup';
import TableOfGroup from './chart/TableOfGroup';
import { fetchWithTokenRefresh } from './RefreshToken';

const { Option } = Select;

const MainPage = () => {

  const { userToken } = useAuth(); 
  const [userTeams, setUserTeams] = useState([]); 
  const [selectedTeam, setSelectedTeam] = useState(null); 
  const [selectedTeamName, setSelectedTeamName] = useState(null);
  const [selectedLessonMainPage, setSelectedLessonMainPage] = useState(null);

  const navigate = useNavigate();
  const { id_team } = useParams();
  const notificationSentRef = useRef(false); 

    
    const fetchUserTeams = async () => {
      if (!userToken) {
        console.error('User token is missing');
        return;
      }

      try {
        const response = await fetchWithTokenRefresh(`http://moais-dashboard.ru:8082/api/get_teams_for_user_without_lect?token=${userToken}`, {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${userToken}`,
          },
        });

        if (response.ok) {
          const userTeamsData = await response.json();
          setUserTeams(userTeamsData);

           // Убедимся, что команда с id_team выбирается автоматически
           if (id_team) {
            const selectedTeam = userTeamsData.find((team) => team.id.toString() === id_team);
            if (selectedTeam) {
              setSelectedTeam(selectedTeam.id);
              setSelectedTeamName(selectedTeam.name);
            } else {
              // Если команда с таким id_team не найдена, показать уведомление
              notification.error({
                message: 'Ошибка',
                description: 'Группа с указанным ID не найдена.',
              });
            }
          }
        } else {
          console.error('Failed to fetch user teams data');
        }
      } catch (error) {
        console.error('Error during fetch user teams data:', error);
      }
    };
    if (userToken) {
      fetchUserTeams();
    }

    useEffect(() => {
      fetchUserTeams();
  }, [userToken]);


  // useEffect(() => {
  //   // Установить выбранную команду из URL после загрузки команд
  //   const setSelectedTeamFromUrl = () => {
  //     if (id_team && userTeams.length > 0) {
  //       const selectedTeam = userTeams.find((team) => team.id.toString() === id_team);
  //       if (selectedTeam) {
  //         setSelectedTeam(selectedTeam.id);
  //         setSelectedTeamName(selectedTeam.name);
  //       } else {
  //         notification.error({
  //           message: 'Ошибка',
  //           description: 'Группа с указанным ID не найдена.',
  //         });
  //       }
  //     }
  //   };

  //   setSelectedTeamFromUrl();
  // }, [id_team, userTeams]);

  
  useEffect(() => {
    if (!selectedTeam && !id_team && !notificationSentRef.current) {
      notification.info({
        message: 'Выбор группы',
        description: 'Пожалуйста, выберите группу из списка.',
      });
    }
  }, [selectedTeam, id_team]);


  const handleTeamChange = (value) => {
    const selectedTeam = userTeams.find((team) => team.id === value);
    setSelectedTeam(value);
    setSelectedTeamName(selectedTeam.name);
    // Переход на страницу с выбранной группой
    navigate(`/main/${value}`);
    
  };

  const handleLessonSelect = (lesson) => {
    setSelectedLessonMainPage(lesson);
  };

  return (
    <Flex direction="column" minHeight="90vh">
      <Select
        style={{ marginLeft: 15, width: '270px', borderWidth: 1, fontFamily: 'Trebuchet MS', height: '40px' }}
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
      {selectedTeam ? (
        <Flex flex="1" flexDirection={{ base: 'column', md: 'row' }}>
          <Box flex="1" minWidth={{ base: '100%', md: '70%' }} p={4}>
            <AtendenceTotalPoints teamId={selectedTeam} teamName={selectedTeamName} />
          </Box>

          <Box flex="1" minWidth={{ base: '100%', md: '30%' }} p={4}>
            <StataOfGroup teamId={selectedTeam} teamName={selectedTeamName} />
          </Box>
        </Flex>
      ) : (
        <Box>
        </Box>
      )}

      {selectedTeam && (
        <Flex flex="1" flexDirection={{ base: 'column', md: 'row' }}>
          <Box flex="1" minWidth={{ base: '100%', md: '60%' }} p={4}>
            <NumCountStudInLern teamId={selectedTeam} teamName={selectedTeamName} onLessonSelect={handleLessonSelect} />
          </Box>

          <Box flex="1" minWidth={{ base: '100%', md: '40%' }} p={4}>
            <TableOfGroup teamName={selectedTeamName} teamId={selectedTeam} selectedLesson={selectedLessonMainPage} />
          </Box>
        </Flex>
      )}
    </Flex>
  );
};

export default MainPage;