// Import statements
import React, { useState, useEffect } from 'react';
import {  Table, Thead, Tbody, Tr, Th, Td, IconButton, Box } from "@chakra-ui/react";
import { ChevronUpIcon, ChevronDownIcon } from '@chakra-ui/icons';
import {TableContainer,Text} from '@chakra-ui/react'

const TableOfGroup = ({ teamId, selectedLesson }) => {
  const [TableOfGroupData, setTableOfGroupData] = useState(null);
  const [sortColumn, setSortColumn] = useState({ key: '', ascending: true });

   useEffect(() => {
    const fetchTableOfGroup = async () => {
      try {
        if (teamId !== null) {
          const response = await fetch(`http://localhost:8090/api/attendance_num_for_stud_for_team_stat_table?id_team=${teamId}&name_of_lesson=${selectedLesson}`);
          const result = await response.json();
          const dataArray = Object.values(result);
   
          // Обновляем состояние с полученными данными
          setTableOfGroupData(dataArray);
        }
      } catch (error) {
        console.error('Error fetching attendanceTotalPoints data:', error);
      }
    };
    fetchTableOfGroup();
  },[teamId,selectedLesson]);

console.log("dataArray - ", TableOfGroupData)

  const handleSort = (key) => {
    setSortColumn({ key, ascending: !sortColumn.ascending });
  };
  
  const sortedData = [...(TableOfGroupData || [])].sort((a, b)  => {
    const aValue = a[sortColumn.key];
    const bValue = b[sortColumn.key];

    if (aValue < bValue) return sortColumn.ascending ? -1 : 1;
    if (aValue > bValue) return sortColumn.ascending ? 1 : -1;

    return 0;
  }
  
  );

  const count = TableOfGroupData ? sortedData.length : 0;

  return (<>

    <Box borderWidth={0} mt={14} p={2}  borderColor='lavender' h={'330'} bg={'white'} borderRadius={20} >
    <Text ml={5} as={'b'} color='#808080' fontFamily={'Trebuchet MS'} fontSize='xl'>{selectedLesson ? `Встреча: ${selectedLesson}` : 'Выберите встречу'}</Text>

    {/* <Text as={'b'} color='#808080' fontFamily={'Trebuchet MS'} fontSize='2xl'>Оценки группы {teamName}</Text> */}

    <TableContainer overflowY="scroll" maxH="220px" > 
    <Table variant="simple">
      <Thead>
        <Tr>
          <Th>№</Th>
          <Th>ID</Th>
          <Th>
            Успеваемость
            <IconButton
              size="xs"
              icon={sortColumn.key === 'Успеваемость' && sortColumn.ascending ? <ChevronUpIcon /> : <ChevronDownIcon />}
              onClick={() => handleSort('Успеваемость!!!')}
            />
          </Th>
          <Th>
            Посещение
            <IconButton
              size="xs"
              icon={sortColumn.key === 'Посещаемость' && sortColumn.ascending ? <ChevronUpIcon /> : <ChevronDownIcon />}
              onClick={() => handleSort('Посещаемость')}
            />
          </Th>
        </Tr>
      </Thead>
      <Tbody>
        {TableOfGroupData && sortedData.map((item, index) => (
          <Tr key={item.id}>
            <Td>{index + 1}</Td>
            <Td>{item.id}</Td>
            <Td>{item.Успеваемость}</Td>
            <Td>{item.Посещаемость}</Td>
          </Tr>
        ))}
      </Tbody>
    </Table>
  </TableContainer>

  <Text mt={2} ml={4} color={'red'} >{`Количество студентов пропустивших занятие: ${count}`}</Text>
  </Box>
      
  </>);
};

export default TableOfGroup;
