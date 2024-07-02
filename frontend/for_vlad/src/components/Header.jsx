import React, { useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { Button, Layout, Typography, Space, Select, Tabs, Row, Col } from 'antd';
import { SearchOutlined, DownloadOutlined, FundViewOutlined, TrophyOutlined, TeamOutlined, FallOutlined, BoxPlotOutlined, AppstoreOutlined, GlobalOutlined, DotChartOutlined, QuestionCircleOutlined, LogoutOutlined } from '@ant-design/icons';

import ExportData from './ReportSystem/ExportData';
import SearchStudentButton from './SearchStudentButton';

import '.././thems/style.css';

const { Header } = Layout;
const { Text } = Typography;
const { Option } = Select;
const { TabPane } = Tabs;

const CustomHeader = () => {
  const location = useLocation();
  const currentPath = location.pathname;
  const navigate = useNavigate();

  const [modalVisible, setModalVisible] = useState(false);
  const [searchModal, setSearchModal] = useState(false);
  const [selectedSemester, setSelectedSemester] = useState('1 семестр - 2022-2023гг.');

  const handleTabChange = (key) => {
    navigate(key);
  };

  const handleSelectChange = (value) => {
    setSelectedSemester(value);
  };

  const isAuthPage = ["/login", "/register", "/"].includes(currentPath);

  if (isAuthPage) {
    return null;
  }

  return (
    <Header  style={{ backgroundColor: '#e4e4e4' }}>
      <Row align="middle" style={{ flexWrap: 'nowrap', justifyContent: 'start', width: '68%' }}>
        <Col>
          <Space>
            <Text style={{ whiteSpace: 'nowrap' }}>Плотоненко Юрий Анатольевич</Text>

            <Select defaultValue="1 семестр - 2022-2023гг." style={{ width: '200px', marginLeft: '0px' }} onChange={handleSelectChange}>
              <Option value="1 семестр - 2022-2023гг.">1 семестр - 2022-2023гг.</Option>
            </Select>
          </Space>
        </Col>
        <Col>
          <Space style={{ marginLeft: '10px' }}>
            <Button shape="round" size='middle' icon={<SearchOutlined />} onClick={() => setSearchModal(true)} />
            <SearchStudentButton visible={searchModal} onClose={() => setSearchModal(false)} />

            <Button  shape="round" size='middle' icon={<DownloadOutlined />} style={{ marginRight: '10px', backgroundColor: '#58c600' }} type="primary" onClick={() => setModalVisible(true)} />
            <ExportData visible={modalVisible} onClose={() => setModalVisible(false)} />
          </Space>
        </Col>
        <Col flex="auto">
          <Tabs defaultActiveKey={currentPath} onChange={handleTabChange} tabBarStyle={{ margin: 0 }}>
            <TabPane tab={<span><FundViewOutlined /> Обзор группы</span>} key="/main" />
            <TabPane tab={<span><TrophyOutlined /> Топы студентов</span>} key="/tops_stud" />
            <TabPane tab={<span><TeamOutlined /> Топы команд</span>} key="/tops_team" />
            <TabPane tab={<span><FallOutlined /> Отстающие</span>} key="/least" />
            <TabPane tab={<span><BoxPlotOutlined /> Обзор КР</span>} key="/analys_kr" />
            <TabPane tab={<span><AppstoreOutlined /> Ваши группы</span>} key="/your_group" />
            <TabPane tab={<span><GlobalOutlined /> Ваши направления</span>} key="/your_vectorstudy" />
            <TabPane tab={<span><DotChartOutlined /> Диаграмма рассеяния</span>} key="/scater_plot" />
            <TabPane tab={<span><QuestionCircleOutlined /> Карта сайта</span>} key="/map_site" />
            <TabPane tab={<span><LogoutOutlined className="logout-icon" /> Выход</span>} key="/" />
          </Tabs>
        </Col>
      </Row>
    </Header>
  );
};

export default CustomHeader;
