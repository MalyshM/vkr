import React, { useState, useEffect } from 'react';
import { useParams,Link } from 'react-router-dom';
import { Line } from 'react-chartjs-2';

import { fetchWithTokenRefresh } from '../RefreshToken';

import { Box, Button, Heading, Menu, MenuButton, MenuList, MenuItem ,Avatar} from '@chakra-ui/react'
import { HamburgerIcon ,LockIcon ,CloseIcon,StarIcon, ArrowUpDownIcon,ArrowBackIcon} from '@chakra-ui/icons';

import { Flex, Center, Spacer} from '@chakra-ui/react'

import StudentInfo from './StudentInfo'

const GeneralStudPage = () => {

  const { studentId, teamName } = useParams();
  const [attendanceData, setAttendanceData] = useState(null);
  const [attendanceDynamicData, setAttendanceDynamicData] = useState(null);
  const [attendanceStaticData, setAttendanceStaticData] = useState(null);
  const [isTest, setIsTest] = useState(false);
  const [teamId, setTeamId] = useState(null);

  const handleTeamIdFetch = (teamId) => {
    setTeamId(teamId);
  };


  useEffect(() => {
    const fetchData = async () => {
      try {
        const urls = [
          `http://moais-dashboard.ru:8082/api/cum_sum_points_for_stud_for_team?id_team=${teamId}&id_stud=${studentId}`,
          `http://moais-dashboard.ru:8082/api/attendance_dynamical_for_stud_for_team?id_team=${teamId}&id_stud=${studentId}`,
          `http://moais-dashboard.ru:8082/api/attendance_static_for_stud_for_team?id_team=${teamId}&id_stud=${studentId}`
        ];

        const responses = await Promise.all(urls.map(url => fetchWithTokenRefresh(url)));
        const data = await Promise.all(responses.map(response => response.json()));

        setAttendanceData(data[0]);
        setAttendanceDynamicData(data[1]);
        setAttendanceStaticData(data[2]);

      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };

    fetchData();

  }, [teamId, studentId, isTest]);

  console.log("NOW GeneralStudPage: ", attendanceData);


  const chartAttendanceData = {
    labels: attendanceData && Array.isArray(attendanceData) ? attendanceData.map(item => item.name) : [],
    datasets: [
      {
        label: 'cum_sum',
        data: attendanceData && Array.isArray(attendanceData) ? attendanceData.map(item => item.cum_sum) : [],
        fill: true,
        borderColor: 'rgb(0,174,239)',
        pointBackgroundColor: attendanceData && Array.isArray(attendanceData) ? attendanceData.map(item => item.test ? 'red' : 'rgb(0,174,239)') : [],
      },
    ],
  };
  
  const charDynamictData = {
    labels: attendanceDynamicData && Array.isArray(attendanceDynamicData) ? attendanceDynamicData.map(item => item.name) : [],
    datasets: [
      {
        label: 'dynamical_arrival',
        data: attendanceDynamicData && Array.isArray(attendanceDynamicData) ? attendanceDynamicData.map(item => item.dynamical_arrival) : [],
        fill: true,
        borderColor: 'rgb(95,122,208)',
      },
    ],
  };
  
  const chartStaticData = {
    labels: attendanceStaticData && Array.isArray(attendanceStaticData) ? attendanceStaticData.map(item => item.name) : [],
    datasets: [
      {
        label: 'static_arrival',
        data: attendanceStaticData && Array.isArray(attendanceStaticData) ? attendanceStaticData.map(item => item.static_arrival) : [],
        fill: true,
        borderColor: 'rgb(251,157,47)',
      },
    ],
  };
  
   
    const OptionsChartAttendance = {
      scales: {
        x: {
          ticks: {
            callback: (value, index, values) => {
                  const counterValues = attendanceData && Array.isArray(attendanceData) ? attendanceData.map(item => item.counter) : [];
                  return counterValues[index] || '';
                },
            display: true,
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
        datalabels: {
          display: false,
          anchor: 'end',
          align: 'end',
          color: 'black', // Цвет текста
          formatter: (value, context) => {
            return `${attendanceStaticData[context.dataIndex].avg_total_points.toFixed(0)} Б`;
  
          },
        },
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
      maintainAspectRatio: false, 

      layout: {
        padding: {
          left: 20,
          right: 20,
          top: 20,
          bottom: 20,
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
            callback: (value, index, values) => {
              const counterValues = attendanceData && Array.isArray(attendanceData) ? attendanceData.map(item => item.counter) : [];
              return counterValues[index] || '';
            },
        display: true,
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
        datalabels: {
          display: false,
          anchor: 'end',
          align: 'end',
          color: 'black', // Цвет текста
          
        },
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
      maintainAspectRatio: false, 

      layout: {
        padding: {
          left: 20,
          right: 20,
          top: 20,
          bottom: 20,
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
            callback: (value, index, values) => {
              const counterValues = attendanceData && Array.isArray(attendanceData) ? attendanceData.map(item => item.counter) : [];
              return counterValues[index] || '';
            },
        display: true,
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
        datalabels: {
          display: false,
          anchor: 'end',
          align: 'end',
          color: 'black', // Цвет текста
          
        },
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
      maintainAspectRatio: false, 

      layout: {
        padding: {
          left: 20,
          right: 20,
          top: 20,
          bottom: 20,
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

      <Flex direction="column" minHeight="90vh">

            <Flex flex="1" flexDirection={{ base: 'column', md: 'row' }}>

              <Box h={'40vh'} flex="1" minWidth={{ base: '100%', md: '50%' }} p={4}>

              <Flex mt={14} direction="column" alignItems="center" justifyContent="center">
                  <Avatar size="2xl" src="https://bit.ly/broken-link" mr={5} />
                  {studentId && <StudentInfo studentId={studentId} onTeamIdFetch={handleTeamIdFetch} />}
                </Flex>
              </Box>

              
              <Box h={'40vh'} flex="1" minWidth={{ base: '100%', md: '50%' }} p={4}>
                <Line data={chartAttendanceData} options={OptionsChartAttendance} />
              </Box>
              
            </Flex>

            <Flex flex="1" flexDirection={{ base: 'column', md: 'row' }}>

              <Box h={'40vh'} flex="1" minWidth={{ base: '100%', md: '50%' }} p={4}>
                {<Line data={chartStaticData} options={OptionsStaticChart} />}
              </Box>

              <Box h={'40vh'} flex="1"  minWidth={{ base: '100%', md: '50%' }} p={4}>
                {<Line data={charDynamictData} options={OptionsDynamicChart}/>}
              </Box>

          </Flex>

      </Flex>

      // <Flex direction="column" height="90vh">
    
      //   <Flex mt={10} justifyContent="space-around">

      //     <Box mr={5} h={[400]} bg={'white'} borderRadius={20} flex="1">

      //       <Flex mt={14} direction="column" alignItems="center" justifyContent="center">
      //         <Avatar size="2xl" src="https://bit.ly/broken-link" mr={5} />
      //         {studentId && <StudentInfo studentId={studentId} teamName={teamName} />}
      //       </Flex>
      //     </Box>

      //     <Box ml={5} h={[400]} bg={'white'} borderRadius={20} flex="1">
      //       <Line data={chartAttendanceData} options={OptionsChartAttendance} />
      //     </Box>

      //   </Flex>
    
      //   <Flex mt={5} justifyContent="space-around">

      //     <Box mr={5} h={[400]} bg={'white'} borderRadius={20} flex="1">
      //       <Line data={chartStaticData} options={OptionsStaticChart} />
      //     </Box>

      //     <Box ml={5} h={[400]} bg={'white'} borderRadius={20} flex="1">
      //       <Line data={charDynamictData} options={OptionsDynamicChart} />
      //     </Box>
      
      //   </Flex>
    
      // </Flex>
    );
    
};

export default GeneralStudPage;

