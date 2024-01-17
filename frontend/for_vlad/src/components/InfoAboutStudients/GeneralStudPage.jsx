import React, { useState, useEffect } from 'react';
import { useParams,Link } from 'react-router-dom';
import { Line } from 'react-chartjs-2';

import { Box, Button, Heading, Menu, MenuButton, MenuList, MenuItem ,Avatar} from '@chakra-ui/react'
import { HamburgerIcon ,LockIcon ,CloseIcon,StarIcon, ArrowUpDownIcon,ArrowBackIcon} from '@chakra-ui/icons';

import { Flex, Center, Spacer} from '@chakra-ui/react'

import StudentInfo from './StudentInfo'

const GeneralStudPage = () => {
  const { studentId, teamId, userTeams,teamName } = useParams();

  const [attendanceData, setAttendanceData] = useState(null);
  const [attendanceDynamicData, setAttendanceDynamicData] = useState(null);
  const [attendanceStaticData, setAttendanceStaticData] = useState(null);
  const [isTest, setIsTest] = useState(false);



  useEffect(() => {
    fetch(`http://localhost:8090/api/cum_sum_points_for_stud_for_team?id_team=${teamId}&id_stud=${studentId}&isTest=${isTest}`)
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
  }, [teamId, studentId,isTest]);


    const chartAttendanceData = {
      labels: attendanceData ? attendanceData.map(item => item.name): [],
      datasets: [
        {
          label: 'cum_sum',
          data: attendanceData ? attendanceData.map(item => item.cum_sum): [],
          fill: true,
          borderColor: 'rgb(0,174,239)',
          pointBackgroundColor: attendanceData ? attendanceData.map(item => item.isTest ? 'red' : 'rgb(0,174,239)') : [],

        },
      ],
    };

    const charDynamictData = {
      labels: attendanceDynamicData ? attendanceDynamicData.map(item => item.name) : [],
      datasets: [
        {
          label: 'dynamical_arrival',
          data: attendanceDynamicData ? attendanceDynamicData.map(item => item.dynamical_arrival) : [],
          fill: true,
          borderColor: 'rgb(95,122,208)',
          // pointBackgroundColor: attendanceDynamicData ? attendanceDynamicData.map(item => item.isTest ? 'red' : 'rgb(0,174,239)') : [],
        },
      ],
    };
    


    const chartStaticData = {
      labels: attendanceStaticData ? attendanceStaticData.map(item => item.name): [],
      datasets: [
        {
          label: 'static_arrival',
          data: attendanceStaticData ? attendanceStaticData.map(item => item.static_arrival): [],
          fill: true,
          
          // backgroundColor: 'rgb(251,157,47)',
          borderColor: 'rgb(251,157,47)',
          // pointBackgroundColor: attendanceStaticData ? attendanceStaticData.map(item => item.isTest ? 'red' : 'rgb(0,174,239)') : [],
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
          left: 0,
          right: 0,
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
          ticks: {
            callback: function (value) {
              return value + '%';
            },
          },
    
        },
      },
      plugins: {
        title: {
          display: true,
          text: 'Динамическое посещение студента',
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
          left: 0,
          right: 0,
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
          ticks: {
            callback: function (value) {
              return value + '%';
            },
          },
    
        },
      },
      plugins: {
        title: {
          display: true,
          text: 'Статическое посещение студента',
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
          left: 0,
          right: 0,
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


  return (<>

<Flex direction="column" height="100vh">

        <Flex  flex="1">

          <Box  flex="1">
            <Button as={Link} to="/main" leftIcon={<ArrowBackIcon />} colorScheme="purple" m={3} >
              Вернуться назад
            </Button>
         
          <Flex direction="column" alignItems={'center'}>

          <Avatar size={'2xl'} src='https://bit.ly/broken-link' mr={5} />
          {studentId && <StudentInfo studentId={studentId} teamName={teamName} />}
          </Flex>


          </Box>

          
          <Box flex="1" h={[400]}>
              <Line data={chartAttendanceData} options={OptionsChartAttendance} />
          </Box>
          
        </Flex>


        <Flex flex="1">

          <Box flex="1" h={[400]}>
            <Line data={chartStaticData} options={OptionsStaticChart} />
          </Box>

          <Box flex="1" h={[400]}>
            <Line data={charDynamictData} options={OptionsDynamicChart} />  
          </Box>

        </Flex>

     </Flex>
    
     
     </>);
};

export default GeneralStudPage;

