import React, { useState, useEffect, useRef } from 'react';
import { Row, Col, Select, notification, Layout, Typography } from 'antd';
import { useNavigate, useParams } from 'react-router-dom';
import { useAuth } from './useAuth';
import AtendenceTotalPoints from './chart/AtendenceTotalPoints';
import NumCountStudInLern from './chart/NumCountStudInLern';
import StataOfGroup from './chart/StataOfGroup';
import TableOfGroup from './chart/TableOfGroup';
import { fetchWithTokenRefresh } from './RefreshToken';

const { Option } = Select;
const { Header, Content } = Layout;
const { Title } = Typography;

const MainPage = () => {
  const { userToken } = useAuth();
  const [userTeams, setUserTeams] = useState([]);
  const [selectedTeam, setSelectedTeam] = useState(null);
  const [selectedTeamName, setSelectedTeamName] = useState(null);
  const [selectedLessonMainPage, setSelectedLessonMainPage] = useState(null);

  const navigate = useNavigate();
  const { id_team } = useParams();
  const notificationSentRef = useRef(false);

  const fetchUserTeams = async () => {
    try {
      const response = await fetchWithTokenRefresh(`http://moais-dashboard.ru:8082/api/get_teams_for_user_without_lect?token=${userToken}`);
      const result = await response.json();
      setUserTeams(result);

      if (id_team) {
        const selectedTeam = result.find((team) => team.id.toString() === id_team);
        if (selectedTeam) {
          setSelectedTeam(selectedTeam.id);
          setSelectedTeamName(selectedTeam.name);
        } else {
          notification.error({
            message: 'Ошибка',
            description: 'Группа с указанным ID не найдена.',
          });
        }
      }
    } catch (error) {
      console.error('Error fetching data from UserTeams:', error);
    }
  };

  useEffect(() => {
    fetchUserTeams();
  }, [userToken]);

  useEffect(() => {
    if (!selectedTeam && !id_team && !notificationSentRef.current) {
      notification.info({
        message: 'Выбор группы',
        description: 'Пожалуйста, выберите группу из списка.',
        duration: 1.2,
      });
      notificationSentRef.current = true;
    }
  }, [selectedTeam, id_team]);

  const handleTeamChange = (value) => {
    const selectedTeam = userTeams.find((team) => team.id === value);
    setSelectedTeam(value);
    setSelectedTeamName(selectedTeam.name);
    navigate(`/main/${value}`);
  };

  const handleLessonSelect = (lesson) => {
    setSelectedLessonMainPage(lesson);
  };

  return (

    <Layout style={{ minHeight: '90vh' }}>

        <Select
          style={{ width: 270, marginTop:5, marginLeft:5 }}
          placeholder="Выберите группу"
          onChange={handleTeamChange}
          value={selectedTeam}
        >
          {Array.isArray(userTeams) ? (
            userTeams.map((team) => (
              <Option key={team.id} value={team.id}>
                {team.name}
              </Option>
            ))
          ) : (
            <Option disabled>Группа не выбрана</Option>
          )}
        </Select>

      <Content style={{ padding: '12px' }}>
        {selectedTeam ? (
          <>
            <Row gutter={[16, 16]} style={{ marginBottom: '24px' }}>

              <Col xs={24} md={16}>
                <AtendenceTotalPoints teamId={selectedTeam} teamName={selectedTeamName} />
              </Col>

              <Col xs={24} md={8}>
                <StataOfGroup teamId={selectedTeam} teamName={selectedTeamName} />
              </Col>

            </Row>

            <Row gutter={[16, 16]}>

              <Col xs={24} md={14}>
                <NumCountStudInLern teamId={selectedTeam} onLessonSelect={handleLessonSelect} />
              </Col>

              <Col xs={24} md={10}>
                <TableOfGroup teamName={selectedTeamName} teamId={selectedTeam} selectedLesson={selectedLessonMainPage} />
              </Col>
              
            </Row>

          </>
        ) : (
          <Row justify="center">
            
          </Row>
        )}
      </Content>
    </Layout>
  );
};

export default MainPage;
