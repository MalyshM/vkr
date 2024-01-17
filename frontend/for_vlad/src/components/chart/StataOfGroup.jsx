import React, { useEffect, useRef ,useState} from 'react';
import { Doughnut, Pie, PolarArea } from 'react-chartjs-2';
import { Flex, Box,Switch,Text, NumberInput, NumberInputField, NumberInputStepper, NumberIncrementStepper, NumberDecrementStepper, Center, Spacer  } from '@chakra-ui/react';
import 'chartjs-plugin-datalabels';

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
            backgroundColor: ['#FF3131', '#FF7B31', '#ecc94b', '#38c741'],
          },
        ],
      };
      
      const options = {
        responsive: true,
        plugins: {
            title: {
                display: true,
                text: `Оценки группы ${teamName}`,
                font: {
                  size: 22,
                  fontColor: 'black',
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
              left: 0,
              right: 0,
              top: 0,
              bottom: 0,
            },
          },
        
        
      };
      
    
      return (<>
          

          {/* <Box mb={5} w={[1500]} maxW='2xl' borderWidth="3px" borderRadius="lg" boxShadow="xl">
            <Line data={chartAttendanceData} options={OptionsChartAttendance} />
          </Box> */}
            
            
          <Flex mr={6}  mt={10} borderWidth={2} p={2} borderRadius={16} borderColor='lavender' direction="row" align="center" >
            <Box flex="1" height='370' >
                <Pie data={chartData} options={options} />
            </Box>
            <Box flex="1" ml={5} mt={10} >
                {stataOfGroupData.map((item) => (
                <Text fontSize='lg' key={item.mark}>{`Студентов с ${item.mark}: ${(item.percent * 100).toFixed(2)}%`}</Text>
                ))}
            </Box>
        </Flex>



       
            

            
            
            
            
            </>);
    };
    
    export default StataOfGroup;
    
    