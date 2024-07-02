import React, { useState, useEffect } from 'react';
import { Typography, Row, Col, Select, Checkbox, Menu, Dropdown, Button, Tooltip } from 'antd';
import { QuestionCircleOutlined } from '@ant-design/icons';
import { useAuth } from '../useAuth';
import { fetchWithTokenRefresh } from '../RefreshToken';
import AnalysKrSimple from './AnalysKrSimple';
import AnalysKrFiltres from './AnalysKrFiltres';
import { Center } from '@chakra-ui/react';

const { Title } = Typography;
const { Option } = Select;

const AnalysRr = () => {
    const { userToken } = useAuth();

    const [TeamData, setTeam] = useState(null);
    const [SelectedTeam, setSelectedTeam] = useState([]);
    const [TeamsForSelectedTeacher, setTeamsForSelectedTeacher] = useState(null);
    const [TeamsForSelectedSpeciality, setTeamsForSelectedSpeciality] = useState(null);

    const [SelectedTeacher, setSelectedTeacher] = useState([]);
    const [TeacherData, setNameTeachers] = useState(null);
    const [TeachersForSelectedSpeciality, setTeachersForSelectedSpeciality] = useState(null);

    const [SpecialityData, setSpeciality] = useState(null);
    const [SelectedSpeciality, setSelectedSpeciality] = useState(["02.03.03 Математическое обеспечение и администрирование информационных систем"]);
    const [SpecialityForSelectedTeacher, setSpecialityForSelectedTeacher] = useState(null);

    const [selectedKRSimple, setSelectedKRSimple] = useState("Организация функций30");
    const [KRSimple, setKRSimple] = useState(null);

    const [selectedKRFiltr, setSelectedKRFiltr] = useState("Организация функций30");
    const [KRFiltr, setKRFiltr] = useState(null);

    const [selectedModeSimple, setSelectedModeSimple] = useState(0);
    const [selectedModeFiltr, setSelectedModeFiltr] = useState(0);

    const fetchNameKR = async () => {
        try {
            const response = await fetchWithTokenRefresh('http://moais-dashboard.ru:8082/api/get_all_kr');
            const result = await response.json();
            setKRSimple(result);
            setKRFiltr(result);
            console.log('Data from fetchNameKR:', result);
        } catch (error) {
            console.error('Error fetching data from fetchNameKR:', error);
        }
    };

    const fetchAllTeachers = async () => {
        try {
            const response = await fetchWithTokenRefresh(`http://moais-dashboard.ru:8082/api/get_all_teachers?token=${userToken}`);
            const result = await response.json();
            setNameTeachers(result);
            console.log('Data from fetchAllTeachers:', result);
        } catch (error) {
            console.error('Error fetching data from fetchAllTeachers:', error);
        }
    };

    const fetchAllSpeciality = async () => {
        try {
            const response = await fetchWithTokenRefresh(`http://moais-dashboard.ru:8082/api/get_all_specialities?token=${userToken}`);
            const result = await response.json();
            setSpeciality(result);
            console.log('Data from fetchAllSpeciality:', result);
        } catch (error) {
            console.error('Error fetching data from fetchAllSpeciality:', error);
        }
    };

    const fetchAllTeam = async () => {
        try {
            const response = await fetchWithTokenRefresh(`http://moais-dashboard.ru:8082/api/get_teams_for_user_without_lect?token=${userToken}`);
            const result = await response.json();
            setTeam(result);
            console.log('Data from fetchAllTeam:', result);
        } catch (error) {
            console.error('Error fetching data from fetchAllTeam:', error);
        }
    };

    const fetchTeamForChoiseTeacher = async () => {
        try {
            const response = await fetchWithTokenRefresh(`http://moais-dashboard.ru:8082/api/get_teams_for_param_without_lect?teacher_arr=${SelectedTeacher}`);
            const result = await response.json();
            setTeamsForSelectedTeacher(result);
            console.log('fetchTeamForChoiseTeacher:', result);
        } catch (error) {
            console.error('Error fetching data from fetchTeamForChoiseTeacher:', error);
        }
    };

    const fetchSpecialityForChoiseTeacher = async () => {
        try {
            const response = await fetchWithTokenRefresh(`http://moais-dashboard.ru:8082/api/get_all_specialities_by_teacher_arr?token=${userToken}&teacher_list=${SelectedTeacher}`);
            const result = await response.json();
            setSpecialityForSelectedTeacher(result);
            console.log('fetchSpecialityForChoiseTeacher:', result);
        } catch (error) {
            console.error('Error fetching data from fetchSpecialityForChoiseTeacher:', error);
        }
    };

    const fetchTeacherForChoiseSpeciality = async () => {
        try {
            const response = await fetchWithTokenRefresh(`http://moais-dashboard.ru:8082/api/get_all_teachers_by_speciality_arr?token=${userToken}&speciality_list=${SelectedSpeciality}`);
            const result = await response.json();
            setTeachersForSelectedSpeciality(result);
            console.log('fetchTeacherForChoiseSpeciality:', result);
        } catch (error) {
            console.error('Error fetching data from fetchTeacherForChoiseSpeciality:', error);
        }
    };

    const fetchTeamsForChoiseSpeciality = async () => {
        try {
            const response = await fetchWithTokenRefresh(`http://moais-dashboard.ru:8082/api/get_all_teams_by_speciality_arr?token=${userToken}&speciality_list=${SelectedSpeciality}`);
            const result = await response.json();
            setTeamsForSelectedSpeciality(result);
            console.log('fetchTeamsForChoiseSpeciality:', result);
        } catch (error) {
            console.error('Error fetching data from fetchTeamsForChoiseSpeciality:', error);
        }
    };

    useEffect(() => {
        const fetchData = async () => {
            await fetchNameKR();
            await fetchAllTeachers();
            await fetchAllSpeciality();
            await fetchAllTeam();
        };

        if (userToken) {
            fetchData();
        }
    }, [userToken]);

    useEffect(() => {
        if (SelectedTeacher.length > 0) {
            fetchTeamForChoiseTeacher();
            fetchSpecialityForChoiseTeacher();
        }
    }, [SelectedTeacher]);

    useEffect(() => {
        if (SelectedSpeciality.length > 0) {
            fetchTeacherForChoiseSpeciality();
            fetchTeamsForChoiseSpeciality();
        }
    }, [SelectedSpeciality]);

    const handleKRChangeSimple = (value) => {
        setSelectedKRSimple(value);
    };

    const handleKRChangeFiltr = (value) => {
        setSelectedKRFiltr(value);
    };

    const handleTeacherSelect = (value) => {
        setSelectedTeacher(value);
    };

    const handleTeamSelect = (value) => {
        setSelectedTeam(value);
    };

    const handleSpecialitySelect = (value) => {
        setSelectedSpeciality(value);
    };

    const handleModeChangeSimple = (value) => {
        setSelectedModeSimple(value);
    };

    const handleModeChangeFiltr = (value) => {
        setSelectedModeFiltr(value);
    };

    return (
        <>
            <Row justify="space-between" align="middle" style={{ padding: '12px' }}>

                <Row >
                    <Title level={2}>Обзор контрольных работ</Title>

                    <Tooltip title="Диаграмма отображающая распределения баллов студентов по КР через: Минимум, Первый квартиль, Медиана, Третий квартиль, Максимум, Выбросы">
                        <QuestionCircleOutlined style={{ marginLeft: 5, marginBottom: 5, fontSize: '20px', cursor: 'pointer' }} />
                    </Tooltip>
                </Row>

            
            <Row >
                <Col >
                    <Select
                        style={{ width: 250, marginRight: 8 }}
                        placeholder="Выберите контрольную точку"
                        onChange={handleKRChangeSimple}
                        value={selectedKRSimple}
                        allowClear
                    >
                        {Array.isArray(KRSimple) ? (
                            KRSimple.map((task) => (
                                <Option key={task.name} value={task.name}>
                                    {task.name}
                                </Option>
                            ))
                        ) : (
                            <Option disabled></Option>
                        )}
                    </Select>
                </Col>

                <Col>
                    <Select
                        style={{ width: 250 }}
                        placeholder="Выберите режим"
                        onChange={handleModeChangeSimple}
                        value={selectedModeSimple}
                        allowClear
                    >
                        <Option value={0}>По группам</Option>
                        <Option value={1}>По направлениям</Option>
                        <Option value={2}>По преподавателям</Option>
                    </Select>
                </Col>

            </Row>

            </Row>


            <Row>
                <Col span={24}>
                <div className="half-screen-height">
                    <AnalysKrSimple tokenUsers={userToken} type={selectedModeSimple} kr={selectedKRSimple} />
                </div>
                </Col>
            </Row>



            <Row justify="end" style={{ marginTop: '16px' }}>
    <Col>
        <Select
            style={{ width: 250, marginRight: '8px' }}
            placeholder="Выберите контрольную точку"
            onChange={handleKRChangeFiltr}
            value={selectedKRFiltr}
            allowClear
        >
            {Array.isArray(KRFiltr) ? (
                KRFiltr.map((task) => (
                    <Option key={task.name} value={task.name}>
                        {task.name}
                    </Option>
                ))
            ) : (
                <Option disabled></Option>
            )}
        </Select>
    </Col>

    <Col>
        <Select
            style={{ width: 250, marginRight: '8px' }}
            placeholder="Выберите режим"
            onChange={handleModeChangeFiltr}
            value={selectedModeFiltr}
            allowClear
        >
            <Option value={0}>По группам</Option>
            <Option value={1}>По преподавателям</Option>
            <Option value={2}>По направлениям</Option>
        </Select>
    </Col>

    <Col>
        <Select
            mode="multiple"
            style={{ width: 250, marginRight: '8px' }}
            placeholder="Выберите преподавателей"
            onChange={setSelectedTeacher}
            value={SelectedTeacher}
            allowClear
        >
            {SelectedSpeciality.length > 0 && TeachersForSelectedSpeciality
                ? TeachersForSelectedSpeciality.map((teacher) => (
                    <Option key={teacher.name} value={teacher.name}>
                        {teacher.name}
                    </Option>
                ))
                : TeacherData &&
                TeacherData.map((teacher) => (
                    <Option key={teacher.name} value={teacher.name}>
                        {teacher.name}
                    </Option>
                ))}
        </Select>
    </Col>

    <Col>
        <Select
            mode="multiple"
            style={{ width: 250, marginRight: '8px' }}
            placeholder="Выберите группы"
            onChange={setSelectedTeam}
            value={SelectedTeam}
            allowClear
        >
            {SelectedTeacher.length > 0 && TeamsForSelectedTeacher
                ? TeamsForSelectedTeacher.map((team) => (
                    <Option key={team.id} value={team.id}>
                        {team.name}
                    </Option>
                ))
                : SelectedSpeciality.length > 0 && TeamsForSelectedSpeciality
                    ? TeamsForSelectedSpeciality.map((team) => (
                        <Option key={team.id} value={team.id}>
                            {team.name}
                        </Option>
                    ))
                    : TeamData &&
                    TeamData.map((team) => (
                        <Option key={team.id} value={team.id}>
                            {team.name}
                        </Option>
                    ))}
        </Select>
    </Col>

    <Col>
        <Select
            mode="multiple"
            style={{ width: 250, marginRight: '8px' }}
            placeholder="Выберите направления"
            onChange={setSelectedSpeciality}
            value={SelectedSpeciality}
            allowClear
        >
            {SelectedTeacher.length > 0 && SpecialityForSelectedTeacher
                ? SpecialityForSelectedTeacher.map((spec) => (
                    <Option key={spec.speciality} value={spec.speciality}>
                        {spec.speciality}
                    </Option>
                ))
                : SpecialityData &&
                SpecialityData.map((spec) => (
                    <Option key={spec.speciality} value={spec.speciality}>
                        {spec.speciality}
                    </Option>
                ))}
        </Select>
    </Col>
</Row>

<Row>
    <Col span={24}>
        <div className="half-screen-height">
            <AnalysKrFiltres
                tokenUsers={userToken}
                type={selectedModeFiltr}
                kr={selectedKRFiltr}
                teacher={SelectedTeacher.length > 0 ? SelectedTeacher : ''}
                speciality={SelectedSpeciality.length > 0 ? SelectedSpeciality : ''}
                team={SelectedTeam.length > 0 ? SelectedTeam : ''}
            />
        </div>
    </Col>
</Row>

        </>
    );
};

export default AnalysRr;
