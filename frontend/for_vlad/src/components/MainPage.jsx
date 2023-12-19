import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from './useAuth';

import { Box, Button, Heading, Select, Menu, MenuButton, MenuList, MenuItem, Text } from '@chakra-ui/react';
import { HamburgerIcon ,LockIcon ,CloseIcon,StarIcon,InfoOutlineIcon, ArrowUpDownIcon} from '@chakra-ui/icons';
import { Modal,ModalOverlay,ModalContent,ModalHeader,ModalFooter,ModalBody,ModalCloseButton,} from '@chakra-ui/react'
import { useDisclosure } from '@chakra-ui/react'
import { Tabs, TabList, TabPanels, Tab, TabPanel } from '@chakra-ui/react'

import MyChart from './chart/MyChart';
import TotalPointsChart from './chart/TotalPointsChart';
// import GeneralStudPage from './InfoAboutStudients/GeneralStudPage'

const MainPage = () => {
  const { userToken } = useAuth(); // Извлекаем userToken из контекста с помощью useAuth
  const [userData, setUserData] = useState(null); // Стейт для хранения данных пользователя
  const [userTeams, setUserTeams] = useState(null); // Новый стейт для данных о командах
  const { isOpen, onOpen, onClose } = useDisclosure();
  
  const [selectedTeam, setSelectedTeam] = useState(null); //Данные о посещаемости
  // const [attendanceData, setAttendanceData] = useState([]);
  const [selectedTab, setSelectedTab] = useState(null);
  

  const handleTabChange = (tab) => {
    setSelectedTab(tab);
  }

  
    const fetchUserData = async () => {
      // Функция для отправки запроса на сервер
      if (!userToken) {
        // Проверяем, что токен существует
        console.error('User token is missing');
        return;
      }
      
      // 1 ЗАПРОС - ПОЛУЧАЕМ ИНФУ ОБ ЮЗЕРЕ
      try {
        // Отправляем POST-запрос на сервер
        const response = await fetch(`http://localhost:8090/api/get_current_user_dev?token=${userToken}`, {
          method: 'POST',
        });

        if (response.ok) {
          // Если запрос успешен, получаем данные и обновляем состояние
          const userData = await response.json();
          console.log('User Data:', userData);
          setUserData(userData);
        } else {
          // Если запрос неудачен, выводим ошибку в консоль
          console.error('Failed to fetch user data');
          console.log('userToken: ', userToken);
        }
      } catch (error) {
        // Обрабатываем ошибку в случае неудачного запроса
        console.error('Error during fetch user data:', error);
      }
    };
    // ПОЛУЧИЛИ ИНФУ ОБ ЮЗЕРЕ (1 ЗАПРОС)

    const fetchUserTeams = async () => {
      if (!userToken) {
        console.error('User token is missing');
        return;
      }

      // 2 ЗАПРОС - ПОЛУЧАЕМ ИНФУ О КОМАНДАХ ЮЗЕРА
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
          console.error('Failed to fetch user teams data');
        }
      } catch (error) {
        console.error('Error during fetch user teams data:', error);
      }
    };
    
  useEffect(() => {
    const fetchData = async () => {
      // Функция для запуска запроса, вызывается при монтировании компонент
      await fetchUserData();
      await fetchUserTeams();
      // await fetchAttendanceData();
      // await fetchTotalPointsData(); // Вызываем функцию для запроса данных о командах после данных пользователя
    };
  
    if (userToken) {
      // Если токен существует, запускаем запрос
      fetchData();
    }
  }, [userToken]);

  const handleTeamChange = (teamId) => {
    setSelectedTeam(teamId);
    // fetchAttendanceData();
    // fetchTotalPointsData();
  };
  
  console.log("userTeams -", userTeams ) 
  
return (
  <>
  
  <div className="container">
    <Menu >
      <MenuButton m={2} as={Button} rightIcon={<HamburgerIcon />}>
        Меню
      </MenuButton>
      <MenuList>
        <MenuItem icon={<CloseIcon />} as={Link} to="/">Выход</MenuItem> 
        <MenuItem icon={<StarIcon />} as={Link} to="/main">Основная страница</MenuItem>
        <MenuItem icon={<InfoOutlineIcon />} onClick={onOpen}>Мой токен</MenuItem>
        <MenuItem icon={<ArrowUpDownIcon />} as={Link} to={{ pathname: '/match2team', state: { teamForMatch: userTeams } }}>
          Сравнение</MenuItem>
        <MenuItem icon={<LockIcon />} >В Разработке</MenuItem>
      </MenuList>
    </Menu>

  </div>
  <Box p={6} w={[1000]} m="auto" mt={1}  borderWidth="3px" borderRadius="lg" boxShadow="xl">
      
      <Heading as="h2" size="lg" mb={4}>
        Главная страница
      </Heading>
      {userData && (
        <Box mb={4}>
          <Text fontSize='xl'>Добро пожаловать, {userData.fio}!</Text>
        </Box>
      )}

      <Box mb={4} borderRadius="lg" boxShadow="lg">
        <Select colorScheme='twitter' 
          placeholder="Выберите вашу подгруппу"
          onChange={(e) => handleTeamChange(e.target.value)}
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
      </Box>
        
      <Text mb={4} fontSize='2xl' textAlign="center"> Выберите вариант отображения:</Text>

      <Box mt={3}>
        <Tabs isFitted variant='enclosed' colorScheme='twitter'>
          
          <TabList>
            <Tab onClick={() => handleTabChange('mychart')} >Посещаемость</Tab>
            <Tab onClick={() => handleTabChange('totalPoints')} >Успеваемость</Tab> 
          </TabList>

          <TabPanels>
            <TabPanel>
              {selectedTab === 'mychart' && <MyChart teamId={selectedTeam} />} 
            </TabPanel>

            <TabPanel>
              {selectedTab === 'totalPoints' && <TotalPointsChart teamId={selectedTeam} />}
            </TabPanel>
          </TabPanels>
        </Tabs>
      </Box>
 
    </Box>

    <Modal onClose={onClose} isOpen={isOpen} isCentered>
    <ModalOverlay />
    <ModalContent>
      <ModalHeader>Мой токен</ModalHeader>
      <ModalCloseButton />
      <ModalBody>
      {userToken ? (
          <p>User Token: {userToken}</p>
        ) : (
          <p>No user token available</p>
        )}
      </ModalBody>
      <ModalFooter>
        <Button onClick={onClose}>Close</Button>
      </ModalFooter>
    </ModalContent>
  </Modal>
  </>);};


export default MainPage;