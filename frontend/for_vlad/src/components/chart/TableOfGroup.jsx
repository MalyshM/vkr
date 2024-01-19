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

  return (<>

    <Box borderWidth={2} mt={10} p={2} borderRadius={16} borderColor='lavender'>
    <Text  fontSize='xl'>{selectedLesson ? `Встреча: ${selectedLesson}` : 'Выберите встречу'}</Text>

    <TableContainer overflowY="scroll" maxH="300px" > 
    <Table variant="simple">
      <Thead>
        <Tr>
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
        {TableOfGroupData && sortedData.map((item) => (
          <Tr key={item.id}>
            <Td>{item.id}</Td>
            <Td>{item.Успеваемость}</Td>
            <Td>{item.Посещаемость}</Td>
          </Tr>
        ))}
      </Tbody>
    </Table>
  </TableContainer>
  </Box>
      
  </>);
};

export default TableOfGroup;
