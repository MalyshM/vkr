import React, { useState } from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import { Button, Layout, Menu, Dropdown, Typography, Space, Segmented, Avatar, Select } from 'antd';
import { UserOutlined, SearchOutlined, DownloadOutlined, FundViewOutlined, TrophyOutlined, TeamOutlined, FallOutlined, BoxPlotOutlined, AppstoreOutlined, GlobalOutlined, DotChartOutlined, QuestionCircleOutlined, LogoutOutlined } from '@ant-design/icons';

import ExportData from './ReportSystem/ExportData';
import SearchStudentButton from './SearchStudentButton';

import '.././thems/style.css';

const { Header } = Layout;
const { Text } = Typography;
const { Option } = Select;

const CustomHeader = () => {
  const location = useLocation();
  const currentPath = location.pathname;
  const navigate = useNavigate();

  const [modalVisible, setModalVisible] = useState(false);
  const [searchModal, setSearchModal] = useState(false);
  const [dropdownVisible, setDropdownVisible] = useState(false);

  const handleSegmentChange = (value) => {
    navigate(value);
  };

  const handleDropdownVisibleChange = (flag) => {
    setDropdownVisible(flag);
  };

  const handleSelectChange = (value) => {
    setDropdownVisible(false);
  };

  const isAuthPage = ["/login", "/register", "/"].includes(currentPath);

  const userMenu = (
    <Menu>
      <Menu.Item key="1">
        <Text>Плотоненко Юрий Анатольевич</Text>
      </Menu.Item>
      <Menu.Item key="2">
        <Select defaultValue="1 семестр - 2022-2023гг." style={{ width: '100%' }} onChange={handleSelectChange}>
          <Option value="1 семестр - 2022-2023гг.">1 семестр - 2022-2023гг.</Option>
        </Select>
      </Menu.Item>
    </Menu>
  );

  if (isAuthPage) {
    return null;
  }

  return (
    <Header className="custom-header" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', backgroundColor: '#00aeef' }}>
      <Space>
        <Dropdown
          overlay={userMenu}
          trigger={['click']}
          visible={dropdownVisible}
          onVisibleChange={handleDropdownVisibleChange}
        >
          <Avatar icon={<UserOutlined />} style={{ marginRight:"10px", cursor: 'pointer' }} />
        </Dropdown>


        <Button icon={<SearchOutlined />} onClick={() => setSearchModal(true)}>
          Поиск студента
        </Button>
        <SearchStudentButton visible={searchModal} onClose={() => setSearchModal(false)} />

        <Button icon={<DownloadOutlined />} style={{ backgroundColor: '#58c600' }} type="primary" onClick={() => setModalVisible(true)}>
          Экспорт данных
        </Button>
        <ExportData visible={modalVisible} onClose={() => setModalVisible(false)} />

        <Segmented
          options={[
            { label: <><FundViewOutlined /> Обзор группы</>, value: '/main' },
            { label: <><TrophyOutlined /> Топы студентов</>, value: '/tops_stud' },
            { label: <><TeamOutlined /> Топы команд</>, value: '/tops_team' },
            { label: <><FallOutlined /> Отстающие</>, value: '/least' },
            { label: <><BoxPlotOutlined /> Анализ КР</>, value: '/analys_kr' },
            { label: <><AppstoreOutlined /> Ваши группы</>, value: '/your_group' },
            { label: <><GlobalOutlined /> Ваши направления</>, value: '/your_vectorstudy' },
            { label: <><DotChartOutlined /> Диаграмма рассеяния</>, value: '/scater_plot' },
            { label: <><QuestionCircleOutlined /> Карта сайта</>, value: '/map_site' },
            { label: <><LogoutOutlined className="logout-icon" /> Выход</>, value: '/' },
          ]}
          onChange={handleSegmentChange}
          defaultValue={currentPath}
          className="custom-segmented"
          style={{ backgroundColor: '#00aeef', marginRight: 'auto' }}
        />
      </Space>
    </Header>
  );
};

export default CustomHeader;
