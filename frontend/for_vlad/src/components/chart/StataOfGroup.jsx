import React, { useEffect, useRef ,useState} from 'react';
import { Doughnut, Pie, PolarArea } from 'react-chartjs-2';
import { Flex, Box,Switch,Text, NumberInput, NumberInputField, NumberInputStepper, NumberIncrementStepper, NumberDecrementStepper, Center, Spacer  } from '@chakra-ui/react';
import 'chartjs-plugin-datalabels';
import { Avatar, AvatarBadge, AvatarGroup } from '@chakra-ui/react'
import styled from 'styled-components';

const StataOfGroup = ({teamId,teamName}) => {
    const [stataOfGroupData, setStataOfGroupData] = useState(null);

    useEffect(() => {
        const fetchSetStataOfGroupData = async () => {
          try {
            if (teamId !== null) {
                // const params = new URLSearchParams({ id_team: teamId });
                const response = await fetch(`http://localhost:8090/api/total_marks_for_team?id_team=${teamId}`);
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


      const chartData = {
        // labels: [],
        labels: stataOfGroupData.map(item => item.mark),
        datasets: [
          {
            data: stataOfGroupData.map(item => item.percent),
            backgroundColor: ['#BB1B1B', '#EC5500', '#FFE81B', '#7DC702'],
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
          

          {/* <Box mb={5} w={[1500]} maxW='2xl' borderWidth="3px" borderRadius="lg" boxShadow="xl">
            <Line data={chartAttendanceData} options={OptionsChartAttendance} />
          </Box> */}
            
            
          <Flex h={'370'} bg={'white'} borderRadius={20} mr={6} mt={14} borderWidth={0} p={2} borderColor='lavender' direction="column" align="center">

            <Flex>
              <Text as={'b'} color='#808080' fontFamily={'Trebuchet MS'} fontSize='2xl'>Оценки группы {teamName}</Text>
            </Flex>
            
            <Flex alignItems={'center'}>

          <Flex mb={10} direction="column" ml={5} mt={10}>
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

            <Box flex="1" height='370' >
                <Doughnut data={chartData} options={options} />
            </Box>
            </Flex>

        </Flex> 
            
            </>);
    };
    
    export default StataOfGroup;
    
    