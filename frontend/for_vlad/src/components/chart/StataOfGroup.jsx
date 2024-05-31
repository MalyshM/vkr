import React, { useEffect, useRef ,useState} from 'react';
import { Doughnut } from 'react-chartjs-2';
import { Flex, Box,Text } from '@chakra-ui/react';
import 'chartjs-plugin-datalabels';
import { Avatar } from '@chakra-ui/react'
import styled from 'styled-components';
import RequestCheckbox from '../ReportSystem/RequestCheckbox';

import {Tooltip } from '@chakra-ui/react';
import { QuestionOutlineIcon } from '@chakra-ui/icons'

import { fetchWithTokenRefresh } from '../RefreshToken';

const StataOfGroup = ({teamId,teamName}) => {
    const [stataOfGroupData, setStataOfGroupData] = useState(null);
    const [requests, setRequests] = useState([]);

    useEffect(() => {
        const fetchSetStataOfGroupData = async () => {
          try {
            if (teamId !== null) {
                // const params = new URLSearchParams({ id_team: teamId });
                const response = await fetchWithTokenRefresh(`http://moais-dashboard.ru:8082/api/total_marks_for_team?id_team=${teamId}`);
                const result = await response.json();

                // Обновляем состояние с полученными данными
                setStataOfGroupData(result);
            }
          } catch (error) {
            console.error('Error fetching fetch_stata_of_group_data data:', error);
          }
        };
        fetchSetStataOfGroupData();
      },[teamId]);
    
      if (!stataOfGroupData) {
        return <div>Loading...</div>;
      }


      const requestUrl = `http://moais-dashboard.ru:8082/api/total_marks_for_team?id_team=${teamId}`;

      const handleUpdateRequests = (updatedRequests) => {
        setRequests(updatedRequests);
      };

      const chartData = {
        // labels: [],
        labels: stataOfGroupData.map(item => item.mark),
        datasets: [
          {
            data: stataOfGroupData.map(item => item.percent),
            backgroundColor: ['#BB1B1B', '#7DC702', '#EC5500', '#FFE81B'],
          },
        ],
      };

      const StyledInfoIcon = styled(Avatar )`
      color: ${props => props.iconColor};`;

      
      const options = {
        responsive: true,
        plugins: {
          datalabels: {
            display: true,
              anchor: 'center',
              align: 'center',
              color: 'black',
              font: {
                size: 16,
                weight: "bold",
              },
        
              formatter: (value, context) => {
                const roundedValue = (value * 100).toFixed(2);
                return `${roundedValue}%`;
        
              },
            },
            title: {
                display: false,
                text: `Оценки группы ${teamName}`,
                padding: {
                  top: 1,
                  bottom: 1,
                },
                font: {
                  size: 24,
                  
                  family: 'Trebuchet MS',
                },
              },
          tooltip: {
            callbacks: {
              label: (context) => {
                const dataIndex = context.dataIndex;
                const avgTotalPoints = stataOfGroupData[dataIndex].avg_total_points.toFixed(2);
                return `Средний балл: ${avgTotalPoints}`;
              },
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
        
        
      };
     
      return (<>
            
          {/* <Flex h={'370'} bg={'white'} borderRadius={20} mr={6} mt={14} borderWidth={0} p={2} borderColor='lavender' direction="column" align="center"> */}

          <Flex  bg={'white'} borderRadius={20}  borderWidth={0} borderColor='lavender' direction="column" align="center">

            <Flex direction={'row'} alignItems={'center'}>
              <Tooltip label="Круговая диаграмма отображающая процентное кол-во студентов с определенной оценкой" aria-label="A tooltip">
                <QuestionOutlineIcon mr={2} boxSize={4} cursor="pointer" />
              </Tooltip>

              <Text as={'b'} color='#808080' fontFamily={'Trebuchet MS'} fontSize='2xl'>Оценки группы {teamName}</Text>

            </Flex>
            <RequestCheckbox
      requestUrl={requestUrl}
      requestName="Оценки группы"
      onUpdateRequests={handleUpdateRequests} />
            <Flex alignItems={'center'}>

          {/* <Flex mb={10} direction="column" ml={5} mt={10}> */}
          <Flex  direction="column" >
            {stataOfGroupData.map((item, index) => (
              <Flex alignItems="center" key={item.mark} >
                <Box
                  boxSize="1.5rem"
                  borderRadius="full"
                  backgroundColor={chartData.datasets[0].backgroundColor[index]}
                  mb={1}
                  mr={1}
                />
                <Text color='#808080' fontFamily={'Trebuchet MS'} fontSize='xl' textAlign="center">
                  {` ${item.mark}`}
                </Text>
              </Flex>
            ))}
            </Flex>

            <Box flex="1" h={'42vh'} >
                <Doughnut data={chartData} options={options} />
            </Box>
            
            </Flex>

        </Flex> 
            
            </>);
    };
    
    export default StataOfGroup;
    
    