import React, { useState, useEffect } from 'react';
import {  Table, Thead, Tbody, Tr, Th, Td, IconButton, chakra } from "@chakra-ui/react";
import { ChevronUpIcon, ChevronDownIcon } from '@chakra-ui/icons';
import {TableContainer,Text,Flex} from '@chakra-ui/react'

import { fetchWithTokenRefresh } from '../RefreshToken';

const StudentInfo = ({ studentId, onTeamIdFetch  }) => {
  const [StudentInfoData, setStudentInfo] = useState(null);

  useEffect(() => {
    const fetchStudentInfo = async () => {
      try {
        if (studentId !== null) {
          const response = await fetchWithTokenRefresh(`http://moais-dashboard.ru:8082/api/get_student?id_stud=${studentId}`);
          const result = await response.json();

          // Обновляем состояние с полученными данными
          setStudentInfo(result);
          
          // Вызов callback-функции с team_id
          if (result && result.length > 0 && onTeamIdFetch) {
            onTeamIdFetch(result[0].team_id);
          }
        }
      } catch (error) {
        console.error('Error fetching StudentInfo data:', error);
      }
    };
    fetchStudentInfo();
  }, [studentId, onTeamIdFetch]);
  
  console.log("StudentInfoData = ", StudentInfoData)


  return (<>
  
  {StudentInfoData && (
    <Flex direction="column">
        <Text fontSize={20}>ID Студента: {studentId}</Text>
        <Text fontSize={20}>
  ФИО студента: {
    (() => {
      const words = StudentInfoData[0].name.split(' ');

      if (words.length < 3) {
        return words.join(' '); // Если слов меньше трех, вернуть оригинальное значение
      }

      const firstNamePart = words[0].substring(0, 3);
      const secondNamePart = words[1].substring(0, 1) + '.';
      const thirdNamePart = words[2].substring(0, 1) + '.';

      return `${firstNamePart} ${secondNamePart}${thirdNamePart}`;
    })()
  }
</Text>

        <Text fontSize={20}>Подгруппа: {StudentInfoData[0].team_name}</Text>
        <Text fontSize={20}>Специальность: {StudentInfoData[0].speciality}</Text>
        <Text fontSize={20}>Email студента: {StudentInfoData[0].email}</Text>
        <Text fontSize={20}>Преподаватель: {StudentInfoData[0].teacher_name}</Text>
    </Flex>
  )}

  </>);
};

export default StudentInfo;