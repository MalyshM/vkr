import React, { useState, useEffect } from 'react';
import {  Table, Thead, Tbody, Tr, Th, Td, IconButton, chakra } from "@chakra-ui/react";
import { ChevronUpIcon, ChevronDownIcon } from '@chakra-ui/icons';
import {TableContainer,Text,Flex} from '@chakra-ui/react'

const StudentInfo = ({ studentId,teamName }) => {
  const [StudentInfoData, setStudentInfo] = useState(null);

   useEffect(() => {
    const fetchStudentInfo = async () => {
      try {
        if (studentId !== null) {
          const response = await fetch(`http://localhost:8090/api/get_student?id_stud=${studentId}`);
          const result = await response.json();
          const dataArray = Object.values(result);
   
          // Обновляем состояние с полученными данными
          setStudentInfo(dataArray);
        }
      } catch (error) {
        console.error('Error fetching StudentInfo data:', error);
      }
    };
    fetchStudentInfo();
  },[studentId]);
  
    console.log("StudentInfoData = ", StudentInfoData)
    // console.log('Специальность:', StudentInfoData.speciality);
    // console.log('ID студента:', StudentInfoData.id);
 


  return (<>
  {StudentInfoData && (
    <Flex direction="column">

        {/* <Text fontSize={20}>Студент: {StudentInfoData[0]}</Text> */}
        <Text fontSize={20}>Студент: {studentId}</Text>
        <Text fontSize={20}>Подгруппа: {teamName}</Text>
        <Text fontSize={20}>Специальность: {StudentInfoData[3]}</Text>
        <Text fontSize={20}>Email студента: {StudentInfoData[1]}</Text>
        <Text fontSize={20}>Дата добавления: {StudentInfoData[2]}</Text>
        

        {/* <Text fontSize={20}>Имя студента: {StudentInfoData[4]}</Text> */}
    </Flex>
  )}

  </>);
};

export default StudentInfo;