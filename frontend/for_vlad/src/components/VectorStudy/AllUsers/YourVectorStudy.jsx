import React, { useState,useEffect} from 'react';
import {Checkbox, Box, Flex ,Heading,Button,  Menu, MenuButton, MenuList, MenuItem} from '@chakra-ui/react';
import { useAuth } from '../../useAuth';
import {Tooltip } from '@chakra-ui/react';
import { QuestionOutlineIcon } from '@chakra-ui/icons'
import VecStudyAllusersAtTp from './VecStudyAllusersAtTp';

import { fetchWithTokenRefresh } from '../../RefreshToken';

const YourVectorStudy = () => {
    const { userToken } = useAuth();
    const [choiseGroupSpeciality_, setChoiseGroupSpeciality] = useState(false); //для чекбокса
    const [teachersData, setTeachers ] = useState(null); //хранит преподов по запросу 
    const [selectedTeachers, setSelectedTeachers] = useState([]);//выбранные преподы отправляются к запросу
    const [SpecialityData, setSpecialityData ] = useState(null);//хранит направления по запросу - чекает токен и выбранных преподов
    const [selectedSpeciality, setSelectedTSpeciality] = useState([]);

    useEffect(() => {
      const fetchAllTeachersData = async () => {
        try {
            if (userToken!== null) {
            const response = await fetchWithTokenRefresh (`http://moais-dashboard.ru:8082/api/get_all_teachers?token=${userToken}`);
            const result = await response.json();
            setTeachers(result);              
          }
        } catch (error) {
          console.error('teachersData - Error fetching attendance data:', error);
        }
      };
      fetchAllTeachersData();
    },[userToken]);

  console.log('teachersData:', teachersData )

  

  useEffect(() => {
    const fetchAllSpecialityData = async () => {
      try {
          if (userToken!== null) {
          const response = await fetchWithTokenRefresh (`http://moais-dashboard.ru:8082/api/get_all_specialities_by_teacher_arr?token=${userToken}&teacher_list=${selectedTeachers}`);
          const result = await response.json();
          setSpecialityData(result);              
        }
      } catch (error) {
        console.error('SpecialityData - Error fetching attendance data:', error);
      }
    };
    fetchAllSpecialityData();
  },[userToken,selectedTeachers]);

  // хэндл для чекбокса с группированием
  const handleCheckboxChange = (event) => {
    setChoiseGroupSpeciality(event.target.checked); 
    };


  // хэндл для выбора (чекбоксов) преподов 
  const handleTeacherSelect = (teacherId) => {
    if (selectedTeachers.includes(teacherId)) {
      setSelectedTeachers(selectedTeachers.filter((id) => id !== teacherId));
    } else {
      setSelectedTeachers([...selectedTeachers, teacherId]);
    }
  };

  // хэндл для выбора (чекбоксов) направлений 
  const handleSpecialitySelect = (spec) => {
    if (selectedSpeciality.includes(spec)) {
      setSelectedTSpeciality(selectedSpeciality.filter((id) => id !== spec));
    } else {
      setSelectedTSpeciality([...selectedSpeciality, spec]);
    }
  };


  

    // const onSelect = (selectedTeachers) => {
    //   // Здесь можете сделать что-то с выбранными преподавателями
    //   console.log('Selected teachers:', selectedTeachers);
    // };

    console.log('test SpecialityData for choose teacher: ', SpecialityData)

return( 
<>
  <Box p={6} display="flex" justifyContent={'space-between'}>
  <Flex direction='row' alignItems={'center'}>

    <Heading as="h2" size="lg">Ваши направления</Heading>  
      <Tooltip label="Диаграмма отображающая медианные посещения (динамическое. В %) и успеваемость (в баллах) направлений/специальностей после КР и атестации" aria-label="A tooltip">
            <QuestionOutlineIcon ml={2} boxSize={4} cursor="pointer" />
      </Tooltip>
      </Flex>

    <Checkbox
      onChange={handleCheckboxChange}
      isChecked={choiseGroupSpeciality_} // Устанавливаем значение чекбокса в соответствии с текущим состоянием
      >
        {choiseGroupSpeciality_ ? 'Группировать по направлениям' : 'Без группировки'}
    </Checkbox>

    <Menu closeOnSelect={false}>
      <MenuButton as={Button} colorScheme="blue">
        Выбрать преподавателей
      </MenuButton>
      <MenuList minWidth="240px">
      {teachersData && teachersData.map((teacher) => (
          <MenuItem key={teacher.id}>
            <Checkbox
              isChecked={selectedTeachers.includes(teacher.name)}
              onChange={() => handleTeacherSelect(teacher.name)}
            >
              {teacher.name}
            </Checkbox>
          </MenuItem>
        ))}
      </MenuList>
    </Menu>

    <Menu closeOnSelect={false}>
      <MenuButton as={Button} colorScheme="blue">
        Выбрать направление
      </MenuButton>
      <MenuList minWidth="240px">
      {SpecialityData && SpecialityData.map((spec) => (
          <MenuItem key={spec.id}>
            <Checkbox
              isChecked={selectedSpeciality.includes(spec.speciality)}
              onChange={() => handleSpecialitySelect(spec.speciality)}
            >
              {spec.speciality}
            </Checkbox>
          </MenuItem>
        ))}
      </MenuList>
    </Menu>
    
    </Box>

  

    <Flex direction={'column'} >

        <Box h={[700]}>
            {<VecStudyAllusersAtTp 
            tokenUsers={userToken}
            choiseGroupSpeciality={choiseGroupSpeciality_}
            selectedTeachers={selectedTeachers}
            selectedSpeciality={selectedSpeciality}
            />}
        </Box>

        {/* <Box h={[380]}>
            {<VecStudyAllUsersTP tokenUsers={userToken}/>}
        </Box> */}
        
    </Flex>
    

    </>)

};
 
export default YourVectorStudy;