import React, { useState, useEffect } from 'react';
import { Row, Col, Select, Checkbox, Tooltip ,Typography} from 'antd';
import { useAuth } from '../../useAuth';
import { Link } from 'react-router-dom';
import AllUsersAtendenceTotalPointsWitchGroup from './AllUsersAtendenceTotalPointsWitchGroup';
import { QuestionCircleOutlined } from '@ant-design/icons';
import { fetchWithTokenRefresh } from '../../RefreshToken';

const { Option } = Select;
const { Title } = Typography;

const YourGroup = () => {
    const { userToken } = useAuth();
    const [choiseGroupTeacher_, setChoiseGroupTeacher] = useState(false);

    const [teachersData, setTeachers] = useState(null);
    const [selectedTeachers, setSelectedTeachers] = useState([]);

    useEffect(() => {
        const fetchAllTeachersData = async () => {
            try {
                if (userToken !== null) {
                    const response = await fetchWithTokenRefresh(`http://moais-dashboard.ru:8082/api/get_all_teachers?token=${userToken}`);
                    const result = await response.json();
                    setTeachers(result);
                    if (result.length > 0) {
                        setSelectedTeachers([result[0].name]);
                    }
                }
            } catch (error) {
                console.error('teachersData - Error fetching attendance data:', error);
            }
        };
        fetchAllTeachersData();
    }, [userToken]);

    console.log('teachersData:', teachersData)

    const handleTeacherSelect = (selectedItems) => {
        setSelectedTeachers(selectedItems);
    };

    const handleCheckboxChange = (e) => {
        setChoiseGroupTeacher(e.target.checked);
    };

    return (
        // эталон alignItems: 'center'
        <> 
            <Row style={{ padding: '12px', alignItems: 'center' }}>  
                <Col>
                    <Row align="middle" >
                      <Title level={2}>Ваши группы</Title>
                        <Tooltip title="Диаграмма отображающая медианные посещения (динамическое. В %) и успеваемость (в баллах) учебных групп после контрольных точек">
                        <QuestionCircleOutlined style={{ marginLeft: 5, marginBottom: 5, fontSize: '20px', cursor: 'pointer' }} />
                        </Tooltip>
                    </Row>
                </Col>

                <Col style={{ marginLeft: '16px' }}>
                    <Select
                        mode="multiple"
                        placeholder="Выбрать преподавателей"
                        style={{ width: 400 }}
                        onChange={handleTeacherSelect}
                        value={selectedTeachers}
                        allowClear
                    >
                        {teachersData && teachersData.map((teacher) => (
                            <Option key={teacher.id} value={teacher.name}>
                                {teacher.name}
                            </Option>
                        ))}
                    </Select>
                </Col>

                <Col style={{ marginLeft: '16px' }}>
                    <Checkbox onChange={handleCheckboxChange} checked={choiseGroupTeacher_}>
                        {choiseGroupTeacher_ ? 'Группировать по преподавателям' : 'Без группировки'}
                    </Checkbox>
                </Col>
            </Row>


            <Row>
                <Col span={24}>
                    <div style={{ height: '80vh' }}>
                        <AllUsersAtendenceTotalPointsWitchGroup
                            selectedTeachers={selectedTeachers}
                            tokenUsers={userToken}
                            choiseGroupTeacher={choiseGroupTeacher_}
                            allTeacherForLegend={teachersData}
                        />
                    </div>
                </Col>
            </Row>
        </>
    );
};

export default YourGroup;
