import React, { useState, useEffect } from 'react';
import { Row, Col, Select, Checkbox, Tooltip, Typography, Button, Divider } from 'antd';
import { QuestionCircleOutlined } from '@ant-design/icons';
import { useAuth } from '../../useAuth';
import VecStudyAllusersAtTp from './VecStudyAllusersAtTp';
import { fetchWithTokenRefresh } from '../../RefreshToken';

const { Title } = Typography;
const { Option } = Select;

const YourVectorStudy = () => {
    const { userToken } = useAuth();
    const [choiseGroupSpeciality_, setChoiseGroupSpeciality] = useState(false); 
    const [teachersData, setTeachers] = useState(null);
    const [selectedTeachers, setSelectedTeachers] = useState([]);
    const [SpecialityData, setSpecialityData] = useState(null);
    const [selectedSpeciality, setSelectedTSpeciality] = useState(["02.03.03 Математическое обеспечение и администрирование информационных систем"]);

    useEffect(() => {
        const fetchAllTeachersData = async () => {
            try {
                if (userToken !== null) {
                    const response = await fetchWithTokenRefresh(`http://moais-dashboard.ru:8082/api/get_all_teachers?token=${userToken}`);
                    const result = await response.json();
                    setTeachers(result);
                    if (result.length > 0) {
                        setSelectedTeachers([result[22].name]);
                        console.log(result[22].name)
                    }
                }
            } catch (error) {
                console.error('teachersData - Error fetching attendance data:', error);
            }
        };
        fetchAllTeachersData();
    }, [userToken]);

    useEffect(() => {
        const fetchAllSpecialityData = async () => {
            try {
                if (userToken !== null) {
                    const response = await fetchWithTokenRefresh(`http://moais-dashboard.ru:8082/api/get_all_specialities_by_teacher_arr?token=${userToken}&teacher_list=${selectedTeachers}`);
                    const result = await response.json();
                    setSpecialityData(result);
                }
            } catch (error) {
                console.error('SpecialityData - Error fetching attendance data:', error);
            }
        };
        fetchAllSpecialityData();
    }, [userToken, selectedTeachers]);

    const handleCheckboxChange = (event) => {
        setChoiseGroupSpeciality(event.target.checked);
    };

    const handleTeacherSelect = (selectedItems) => {
        setSelectedTeachers(selectedItems);
    };

    const handleSpecialitySelect = (selectedItems) => {
        setSelectedTSpeciality(selectedItems);
    };

    return (
        <>
            <Row style={{ padding: '12px', alignItems: 'center' }}>
                <Col>
                    <Row align="middle">
                        <Title level={2}>Ваши направления</Title>
                        <Tooltip title="Диаграмма отображающая медианные посещения (динамическое. В %) и успеваемость (в баллах) направлений/специальностей после контрольных точек">
                            <QuestionCircleOutlined style={{ marginLeft: 5,marginBottom: 5, fontSize: '20px', cursor: 'pointer' }} />
                        </Tooltip>
                    </Row>
                </Col>
                
                <Col style={{ marginLeft: '16px' }}>
                    <Select
                        mode="multiple"
                        placeholder="Выбрать преподавателей"
                        style={{ minWidth: 240, maxWidth: 'auto' }}
                        onChange={handleTeacherSelect}
                        value={selectedTeachers}
                    >
                        {teachersData && teachersData.map((teacher) => (
                            <Option key={teacher.id} value={teacher.name}>
                                {teacher.name}
                            </Option>
                        ))}
                    </Select>
                </Col>
                
                <Col style={{ marginLeft: '16px' }}>
                    <Select
                        mode="multiple"
                        placeholder="Выбрать направление"
                        style={{ width: 240 }}
                        onChange={handleSpecialitySelect}
                        value={selectedSpeciality}
                    >
                        {SpecialityData && SpecialityData.map((spec) => (
                            <Option key={spec.id} value={spec.speciality}>
                                {spec.speciality}
                            </Option>
                        ))}
                    </Select>
                </Col>

                <Col style={{ marginLeft: '16px' }}>
                    <Checkbox onChange={handleCheckboxChange} checked={choiseGroupSpeciality_}>
                        {choiseGroupSpeciality_ ? 'Группировать по направлениям' : 'Без группировки'}
                    </Checkbox>
                </Col>
                
            </Row>

            <Row>
                <Col span={24}>
                    <div style={{ height: '700px' }}>
                        <VecStudyAllusersAtTp
                            tokenUsers={userToken}
                            choiseGroupSpeciality={choiseGroupSpeciality_}
                            selectedTeachers={selectedTeachers}
                            selectedSpeciality={selectedSpeciality}
                        />
                    </div>
                </Col>
            </Row>
        </>
    );
};

export default YourVectorStudy;
