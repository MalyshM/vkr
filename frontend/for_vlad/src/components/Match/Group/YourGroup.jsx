import React, { useState,useEffect} from 'react';
import { Box, Flex, Select,Spacer ,Heading,Text,Button,  Menu, MenuButton, MenuList, MenuItem} from '@chakra-ui/react';
import { useAuth } from '../../useAuth';
import { HamburgerIcon ,LockIcon ,CloseIcon,StarIcon,ArrowBackIcon, ArrowUpDownIcon} from '@chakra-ui/icons';
import { Link } from 'react-router-dom';
import { Tabs, TabList, TabPanels, Tab, TabPanel } from '@chakra-ui/react'
import { Checkbox, CheckboxGroup } from '@chakra-ui/react'
import { List, ListItem, MenuOptionGroup, MenuItemOption, MenuDivider } from "@chakra-ui/react";
import AllUsersAtendenceTotalPointsWitchGroup from './AllUsersAtendenceTotalPointsWitchGroup';

import { fetchWithTokenRefresh } from 'D:/2newvkr/vkr_true/frontend/for_vlad/src/components/RefreshToken';

const YourGroup = () => {
    const { userToken } = useAuth();
    const [choiseGroupTeacher_, setChoiseGroupTeacher] = useState(false);

    const [teachersData, setTeachers ] = useState(null);
    const [selectedTeachers, setSelectedTeachers] = useState([]);

    useEffect(() => {
      const fetchAllTeachersData = async () => {
        try {
            if (userToken!== null) {
            const response = await fetchWithTokenRefresh(`http://moais-dashboard.ru:8082/api/get_all_teachers?token=${userToken}`);
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

    
    const handleTeacherSelect = (teacherId) => {
      if (selectedTeachers.includes(teacherId)) {
        setSelectedTeachers(selectedTeachers.filter((id) => id !== teacherId));
      } else {
        setSelectedTeachers([...selectedTeachers, teacherId]);
      }
    };

  //   const handleTeacherSelect = (teacherName) => {
  //     setSelectedTeachers(prevSelected => {
  //         if (prevSelected.includes(teacherName)) {
  //             return prevSelected.filter(name => name !== teacherName);
  //         } else {
  //             return [...prevSelected, teacherName];
  //         }
  //     });
  // };


  const handleCheckboxChange = (event) => {
    setChoiseGroupTeacher(event.target.checked); 
    };

    const onSelect = (selectedTeachers) => {
      // Здесь можете сделать что-то с выбранными преподавателями
      console.log('Selected teachers:', selectedTeachers);
    };

    


 
return( 
<>
  <Box p={6} display="flex" justifyContent={'space-between'}>
    <Heading as="h2" size="lg">Посещаемость и успеваемость студентов после каждой КР</Heading>
  
    <Checkbox
      onChange={handleCheckboxChange}
      isChecked={choiseGroupTeacher_} // Устанавливаем значение чекбокса в соответствии с текущим состоянием
      >
        {choiseGroupTeacher_ ? 'Группировать по преподавателям' : 'Без группировки'}
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


  </Box>


  <Box ml={6} mr={6} display="flex" justifyContent={'space-between'}>

  {/* {teachersData && teachersData.map((teacher) => (
                    <Checkbox
                        key={teacher.id}
                        isChecked={selectedTeachers.includes(teacher.name)}
                        onChange={() => handleTeacherSelect(teacher.name)}
                    >
                        {teacher.name}
                    </Checkbox>
                ))} */}

  
    </Box>

  

    <Flex direction={'column'} >

        <Box h={[760]}>
            {<AllUsersAtendenceTotalPointsWitchGroup 
            selectedTeachers={selectedTeachers}
            tokenUsers={userToken}
            choiseGroupTeacher={choiseGroupTeacher_}
            allTeacherForLegend={teachersData}
            />}
        </Box>

        {/* <Box h={[380]}>
            {<AllUsersTotalPoint tokenUsers={userToken}/>}
        </Box> */}
        
    </Flex>
    

    </>)

};

 
export default YourGroup;