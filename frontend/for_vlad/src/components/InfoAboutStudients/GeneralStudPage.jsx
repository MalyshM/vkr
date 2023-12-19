import React, { useState, useEffect } from 'react';
import { useParams,Link } from 'react-router-dom';
import { Line } from 'react-chartjs-2';

import { Box, Button, Heading, Menu, MenuButton, MenuList, MenuItem ,Avatar} from '@chakra-ui/react'
import { HamburgerIcon ,LockIcon ,CloseIcon,StarIcon, ArrowUpDownIcon,ArrowBackIcon} from '@chakra-ui/icons';

import { Flex, Center, Spacer} from '@chakra-ui/react'

const GeneralStudPage = () => {
  const { studentId, teamId, userTeams } = useParams();

  const [attendanceData, setAttendanceData] = useState(null);
  const [attendanceDynamicData, setAttendanceDynamicData] = useState(null);
  const [attendanceStaticData, setAttendanceStaticData] = useState(null);


  useEffect(() => {
    fetch(`http://localhost:8090/api/cum_sum_points_for_stud_for_team?id_team=${teamId}&id_stud=${studentId}`)
      .then(response => response.json())
      .then(data => setAttendanceData(data))
      .catch(error => console.error('Error fetching attendance data:', error));

    fetch(`http://localhost:8090/api/attendance_dynamical_for_stud_for_team?id_team=${teamId}&id_stud=${studentId}`)
      .then(response => response.json())
      .then(data => setAttendanceDynamicData(data))
      .catch(error => console.error('Error fetching dynamic attendance data:', error));

    fetch(`http://localhost:8090/api/attendance_static_for_stud_for_team?id_team=${teamId}&id_stud=${studentId}`)
      .then(response => response.json())
      .then(data => setAttendanceStaticData(data))
      .catch(error => console.error('Error fetching static attendance data:', error));
  }, [teamId, studentId]);


    const chartAttendanceData = {
      labels: attendanceData ? attendanceData.map(item => item.name): [],
      datasets: [
        {
          label: 'cum_sum',
          data: attendanceData ? attendanceData.map(item => item.cum_sum): [],
          fill: false,
          
          borderColor: 'rgb(0,174,239)',
        },
      ],
    };

    const charDynamictData = {
      labels: attendanceDynamicData ? attendanceDynamicData.map(item => item.name): [],
      datasets: [
        {
          label: 'dynamical_arrival',
          data: attendanceDynamicData ? attendanceDynamicData.map(item => item.dynamical_arrival): [],
          fill: false,
          
          borderColor: 'rgb(0,174,239)',
        },
      ],
    };

    const chartStaticData = {
      labels: attendanceStaticData ? attendanceStaticData.map(item => item.name): [],
      datasets: [
        {
          label: 'static_arrival',
          data: attendanceStaticData ? attendanceStaticData.map(item => item.static_arrival): [],
          fill: false,
          
          borderColor: 'rgb(0,174,239)',
        },
      ],
    };
   
    const OptionsChartAttendance = {
      scales: {
        x: {
          ticks: {
            display: false,
          },
          display: true,
          type: 'category',
          position: 'bottom',
          title: {
            display: true,
            text: 'Изучаемая тема на паре',
            font: {
              size: 16, // Размер шрифта названия оси X
              fontColor: 'black',
              family: 'Trebuchet MS'
            },
          },
        },
        y: {
          type: 'linear', // изменение типа шкалы на категорию 
          position: 'left',
          title: {
            display: true,
            text: 'Баллы студента',
            font: {
              size: 16, // Размер шрифта названия оси X
              fontColor: 'black',
              family: 'Trebuchet MS'
            },
          },
        },
      },
      plugins: {
        title: {
          display: true,
          text: 'Кумулятивная сумма баллов студента по дисциплине ПиОА',
          font: {
            size: 20,
            fontColor: 'black',
            family: 'Trebuchet MS'
          },
        },
    
        legend: {
          display: false,
          position: 'top',
        },
      },
      layout: {
        padding: {
          left: 50,
          right: 50,
          top: 0,
          bottom: 0,
        },
      },
      elements: {
        bar: {
          barThickness: 400,
          borderRadius: 10, 
        },
      },
      animation: {
        duration: 2000,
        
    
      },
    };

    const OptionsDynamicChart = {
      scales: {
        x: {
          ticks: {
            display: false,
          },
          display: true,
          type: 'category',
          position: 'bottom',
          title: {
            display: true,
            text: 'Изучаемая тема на паре',
            font: {
              size: 16, // Размер шрифта названия оси X
              fontColor: 'black',
              family: 'Trebuchet MS'
            },
          },
        },
        y: {
          type: 'linear', // изменение типа шкалы на категорию 
          position: 'left',
          title: {
            display: true,
            text: 'Посещение',
            font: {
              size: 16, // Размер шрифта названия оси X
              fontColor: 'black',
              family: 'Trebuchet MS'
            },
          },
        },
      },
      plugins: {
        title: {
          display: true,
          text: 'посещения студента - если падает, то пропускает, если растет то посещает',
          font: {
            size: 20,
            fontColor: 'black',
            family: 'Trebuchet MS'
          },
        },
    
        legend: {
          display: false,
          position: 'top',
        },
      },
      layout: {
        padding: {
          left: 50,
          right: 50,
          top: 0,
          bottom: 0,
        },
      },
      elements: {
        bar: {
          barThickness: 400,
          borderRadius: 10, 
        },
      },
      animation: {
        duration: 2000,
        
    
      },
    }; 

    const OptionsStaticChart = {
      scales: {
        x: {
          ticks: {
            display: false,
          },
          display: true,
          type: 'category',
          position: 'bottom',
          title: {
            display: true,
            text: 'Изучаемая тема на паре',
            font: {
              size: 16, // Размер шрифта названия оси X
              fontColor: 'black',
              family: 'Trebuchet MS'
            },
          },
        },
        y: {
          type: 'linear', // изменение типа шкалы на категорию 
          position: 'left',
          title: {
            display: true,
            text: 'Посещение',
            font: {
              size: 16, // Размер шрифта названия оси X
              fontColor: 'black',
              family: 'Trebuchet MS'
            },
          },
        },
      },
      plugins: {
        title: {
          display: true,
          text: 'посещения студента - если не ходит, то не растёт',
          font: {
            size: 20,
            fontColor: 'black',
            family: 'Trebuchet MS'
          },
        },
    
        legend: {
          display: false,
          position: 'top',
        },
      },
      layout: {
        padding: {
          left: 50,
          right: 50,
          top: 0,
          bottom: 0,
        },
      },
      elements: {
        bar: {
          barThickness: 400,
          borderRadius: 10, 
        },
      },
      animation: {
        duration: 2000,
      },
    }; 


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
        <MenuItem icon={<ArrowUpDownIcon />} as={Link} to={{ pathname: '/match2team', state: { teamForMatch: userTeams } }}>
          Сравнение</MenuItem>
        <MenuItem icon={<LockIcon />} >В Разработке</MenuItem>
      </MenuList>
    </Menu>

  </div>
    
    <Box p={6} w={[1450]} h={[800]} m="auto" borderWidth="3px" borderRadius="lg" boxShadow="xl">

        <span>
          <Heading as="h1" size="xl" style={{ display: 'flex', alignItems: 'center' }} mb={4}>

            <Avatar src='https://bit.ly/broken-link' mr={3} />

            Студент - {studentId}, Подгруппа - {teamId}

            <Button as={Link} to="/main" leftIcon={<ArrowBackIcon />} colorScheme="twitter" ml={3}>
              Вернуться назад
            </Button>

          </Heading>
        </span>

        <Center>
          <Box mb={5} w={[1500]} maxW='2xl' borderWidth="3px" borderRadius="lg" boxShadow="xl">
            <Line data={chartAttendanceData} options={OptionsChartAttendance} />
          </Box>
        </Center>

        <Flex color='red'>

          <Box w={[1500]} maxW='2xl' borderWidth="3px" borderRadius="lg" boxShadow="xl">
            <Line data={chartStaticData} options={OptionsStaticChart} />
          </Box>
          <Spacer />
          <Box w={[1500]} maxW='2xl' borderWidth="3px" borderRadius="lg" boxShadow="xl">
            <Line data={charDynamictData} options={OptionsDynamicChart} />
          </Box>

        </Flex>
      </Box></>
  );
};

export default GeneralStudPage;

