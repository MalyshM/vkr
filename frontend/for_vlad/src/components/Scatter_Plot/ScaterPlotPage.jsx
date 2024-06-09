import React, { useState, useEffect } from 'react';
import ScaterPlotDiagram from './ScaterPlotDiagram';
import ScaterPlotBySection from './ScaterPlotBySection';
import { useAuth } from '../useAuth';
import { fetchWithTokenRefresh } from '../RefreshToken';
import { Checkbox, Row, Col, Select, Typography, Tooltip, Button, Divider } from 'antd';
import { QuestionCircleOutlined } from '@ant-design/icons';

const { Title } = Typography;
const { Option } = Select;

const ScaterPlotPage = () => {
    const { userToken } = useAuth();

    const [TeamData, SetTeamData] = useState(null);
    const [SelectedTeam, setSelectedTeam] = useState([]);
    const [TeamsForSelectedTeacher, setTeamsForSelectedTeacher] = useState(null);
    const [TeamsForSelectedSpeciality, setTeamsForSelectedSpeciality] = useState(null);

    const [TeacherData, SetTeacherData] = useState(null);
    const [SelectedTeacher, setSelectedTeacher] = useState([]);
    const [TeachersForSelectedSpeciality, setTeachersForSelectedSpeciality] = useState(null);

    const [SpecialityData, SetSpecialityData] = useState(null);
    const [SelectedSpeciality, setSelectedSpeciality] = useState(["02.03.03 Математическое обеспечение и администрирование информационных систем"]);
    const [SpecialityForSelectedTeacher, setSpecialityForSelectedTeacher] = useState(null);

    const [CheckboxOne, setCheckboxOne] = useState(true);
    const [CheckboxMany, setCheckboxMany] = useState(true);
    const [SelectedMode, setSelectedMode] = useState(3);

    const fetchTeamForTeacher = async () => {
        try {
            const response = await fetchWithTokenRefresh(`http://moais-dashboard.ru:8082/api/get_teams_for_user_without_lect?token=${userToken}`);
            const result = await response.json();
            SetTeamData(result);
        } catch (error) {
            console.error('Error fetching data from fetchTeamForTeacher:', error);
        }
    };

    const fetchSpecialityForTeacher = async () => {
        try {
            const response = await fetchWithTokenRefresh(`http://moais-dashboard.ru:8082/api/get_all_specialities?token=${userToken}`);
            const result = await response.json();
            SetSpecialityData(result);
        } catch (error) {
            console.error('Error fetching data from fetchSpecialityForTeacher:', error);
        }
    };

    const fetchTeacher = async () => {
        try {
            const response = await fetchWithTokenRefresh(`http://moais-dashboard.ru:8082/api/get_all_teachers_unique?token=${userToken}`);
            const result = await response.json();
            SetTeacherData(result);
        } catch (error) {
            console.error('Error fetching data from fetchTeacher:', error);
        }
    };

    const fetchTeamForChoiseTeacher = async () => {
        try {
            const response = await fetchWithTokenRefresh(`http://moais-dashboard.ru:8082/api/get_teams_for_param_without_lect?teacher_arr=${SelectedTeacher}`);
            const result = await response.json();
            setTeamsForSelectedTeacher(result);
        } catch (error) {
            console.error('Error fetching data from fetchTeamForChoiseTeacher:', error);
        }
    };

    const fetchSpecialityForChoiseTeacher = async () => {
        try {
            const response = await fetchWithTokenRefresh(`http://moais-dashboard.ru:8082/api/get_all_specialities_by_teacher_arr?token=${userToken}&teacher_list=${SelectedTeacher}`);
            const result = await response.json();
            setSpecialityForSelectedTeacher(result);
        } catch (error) {
            console.error('Error fetching data from fetchSpecialityForChoiseTeacher:', error);
        }
    };

    const fetchTeacherForChoiseSpeciality = async () => {
        try {
            const response = await fetchWithTokenRefresh(`http://moais-dashboard.ru:8082/api/get_all_teachers_by_speciality_arr?token=${userToken}&speciality_list=${SelectedSpeciality}`);
            const result = await response.json();
            setTeachersForSelectedSpeciality(result);
        } catch (error) {
            console.error('Error fetching data from fetchTeacherForChoiseSpeciality:', error);
        }
    };

    const fetchTeamsForChoiseSpeciality = async () => {
        try {
            const response = await fetchWithTokenRefresh(`http://moais-dashboard.ru:8082/api/get_all_teams_by_speciality_arr?token=${userToken}&speciality_list=${SelectedSpeciality}`);
            const result = await response.json();
            setTeamsForSelectedSpeciality(result);
        } catch (error) {
            console.error('Error fetching data from fetchTeamsForChoiseSpeciality:', error);
        }
    };

    console.log("TeacherData",TeacherData)
    console.log('SelectedTeacher ',SelectedTeacher )

    useEffect(() => {
        const fetchData = async () => {
            await fetchTeamForTeacher();
            await fetchSpecialityForTeacher();
            await fetchTeacher();
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

    const handleCheckboxOneChange = (event) => {
        setCheckboxOne(event.target.checked);
    };

    const handleCheckboxManyChange = (event) => {
        setCheckboxMany(event.target.checked);
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

    const handleModeChange = (value) => {
        setSelectedMode(value);
    };

    return (
        <>
            <Row style={{ justifyContent: 'space-around', padding: '12px', alignItems: 'center' }}>
                <Col>
                    <Row align="middle">
                        <Title level={2}>Диаграмма рассеяния</Title>
                        <Tooltip title="Диаграмма отображающая взаимосвязь между успеваемостью и посещаемостью">
                            <QuestionCircleOutlined style={{ marginBottom:8, marginLeft: 5, fontSize: '20px', cursor: 'pointer' }} />
                        </Tooltip>
                    </Row>
                </Col>
                
                <Col>
                    <Checkbox checked={CheckboxOne} onChange={handleCheckboxOneChange}>
                        Общий график
                    </Checkbox>
                </Col>
                
                <Col>
                    <Checkbox checked={CheckboxMany} onChange={handleCheckboxManyChange}>
                        N-диаграмм
                    </Checkbox>
                </Col>
                
                <Col>
                    <Select
                        placeholder="Выбери режим"
                        style={{ width: 160 }}
                        onChange={handleModeChange}
                        value={SelectedMode}
                    >
                        <Option value={3}>По группам</Option>
                        <Option value={1}>По направлениям</Option>
                        <Option value={2}>По преподавателям</Option>
                    </Select>
                </Col>
                
                <Col>
                    <Select
                        mode="multiple"
                        placeholder="Выбрать группы"
                        style={{ width: 240 }}
                        onChange={handleTeamSelect}
                        value={SelectedTeam}
                        allowClear
                    >
                        {SelectedTeacher.length > 0 && TeamsForSelectedTeacher ? (
                            TeamsForSelectedTeacher.map((team) => (
                                <Option key={team.id} value={team.id}>
                                    {team.name}
                                </Option>
                            ))
                        ) : SelectedSpeciality.length > 0 && TeamsForSelectedSpeciality ? (
                            TeamsForSelectedSpeciality.map((team) => (
                                <Option key={team.id} value={team.id}>
                                    {team.name}
                                </Option>
                            ))
                        ) : (
                            TeamData &&
                            TeamData.map((team) => (
                                <Option key={team.id} value={team.id}>
                                    {team.name}
                                </Option>
                            ))
                        )}
                    </Select>
                </Col>
                
                <Col>
                    <Select
                        mode="multiple"
                        placeholder="Выбрать преподавателей"
                        style={{ width: 240 }}
                        onChange={handleTeacherSelect}
                        value={SelectedTeacher}
                        allowClear
                    >
                        {SelectedSpeciality.length > 0 && TeachersForSelectedSpeciality ? (
                            TeachersForSelectedSpeciality.map((teacher) => (
                                <Option key={teacher.id} value={teacher.name}>
                                    {teacher.name}
                                </Option>
                            ))
                        ) : (
                            TeacherData &&
                            TeacherData.map((teacher) => (
                                <Option key={teacher.id} value={teacher.name}>
                                    {teacher.name}
                                </Option>
                            ))
                        )}
                    </Select>
                </Col>
                
                <Col>
                    <Select
                        mode="multiple"
                        placeholder="Выбрать направления"
                        style={{ width: 240 }}
                        onChange={handleSpecialitySelect}
                        value={SelectedSpeciality}
                        allowClear
                    >
                        {SelectedTeacher.length > 0 && SpecialityForSelectedTeacher ? (
                            SpecialityForSelectedTeacher.map((spec) => (
                                <Option key={spec.id} value={spec.speciality}>
                                    {spec.speciality}
                                </Option>
                            ))
                        ) : (
                            SpecialityData &&
                            SpecialityData.map((spec) => (
                                <Option key={spec.id} value={spec.speciality}>
                                    {spec.speciality}
                                </Option>
                            ))
                        )}
                    </Select>
                </Col>
            </Row>
            <Row>
                <Col span={24} style={{ padding: '6px' }}>
                    {SelectedMode && (
                        <ScaterPlotDiagram
                            CheckboxMany={CheckboxMany}
                            CheckboxOne={CheckboxOne}
                            tokenUsers={userToken}
                            type_group_by={SelectedMode}
                            teacher_list={SelectedTeacher.length > 0 ? SelectedTeacher : ''}
                            speciality_list={SelectedSpeciality.length > 0 ? SelectedSpeciality : ''}
                            team_list={SelectedTeam.length > 0 ? SelectedTeam : ''}
                        />
                    )}
                </Col>
            </Row>
            <Row>
                <Col span={24} style={{ padding: '6px' }}>
                    {SelectedMode && (
                        <ScaterPlotBySection
                            tokenUsers={userToken}
                            type_group_by={SelectedMode}
                            teacher_list={SelectedTeacher.length > 0 ? SelectedTeacher : ''}
                            speciality_list={SelectedSpeciality.length > 0 ? SelectedSpeciality : ''}
                            team_list={SelectedTeam.length > 0 ? SelectedTeam : ''}
                        />
                    )}
                </Col>
            </Row>
        </>
    );
};

export default ScaterPlotPage;
