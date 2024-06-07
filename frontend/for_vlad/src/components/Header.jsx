import React, { useEffect, useState } from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import { Button, Layout, Menu, Dropdown, Typography, Space, Segmented } from 'antd';
import { QuestionOutlined } from '@ant-design/icons';

import ExportData from './ReportSystem/ExportData';

import '.././thems/style.css';

import { HomeOutlined, TrophyOutlined, TeamOutlined, MehOutlined, BoxPlotOutlined, GroupOutlined, AimOutlined, DotChartOutlined, LogoutOutlined, FileTextOutlined,SearchOutlined,QuestionCircleOutlined, FundViewOutlined, FallOutlined,DownloadOutlined, AppstoreOutlined, GlobalOutlined} from '@ant-design/icons';
import SearchStudentButton from './SearchStudentButton';

import { DownOutlined, SmileOutlined } from '@ant-design/icons';

const { Header } = Layout;
const { Text } = Typography;

const CustomHeader = () => {
  const location = useLocation();
  const currentPath = location.pathname;
  const navigate = useNavigate();

  const [modalVisible, setModalVisible] = useState(false);
  const [searchModal, setsearchModal] = useState(false);
  
  const handleSegmentChange = (value) => {
    navigate(value);
  };

  const isAuthPage = ["/login", "/register", "/"].includes(currentPath);

  if (isAuthPage) {
    return null;
  }

return (
  <Header style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', backgroundColor: '#00aeef' }}>
   
    <Space>
    <Button icon={<SearchOutlined />} onClick={() => setsearchModal(true)}>
          Поиск студента
        </Button>
        <SearchStudentButton visible={searchModal} onClose={() => setsearchModal(false)}/>

      <Button icon={<DownloadOutlined />} style={{ backgroundColor: '#58c600' }} type="primary" onClick={() => setModalVisible(true)}>
        Экспорт данных
      </Button>
      <ExportData visible={modalVisible} onClose={() => setModalVisible(false)} />

      {/* <SettingOutlined /> */}

      <Segmented
        options={[
          { label: <><FundViewOutlined /> Обзор группы</>, value: '/main' },
          { label: <><TrophyOutlined /> Топы студентов</>, value: '/tops_stud' },
          { label: <><TeamOutlined /> Топы команд</>, value: '/tops_team' },
          { label: <><FallOutlined /> Отстающие</>, value: '/least' },
          { label: <><BoxPlotOutlined /> Анализ КТ</>, value: '/analys_kr' },
          { label: <><AppstoreOutlined /> Ваши группы</>, value: '/your_group' },
          { label: <><GlobalOutlined /> Ваши направления</>, value: '/your_vectorstudy' },
          { label: <><DotChartOutlined /> Диаграмма рассеяния</>, value: '/scater_plot' },
          { label: <><QuestionCircleOutlined/> Карта сайта</>, value: '/map_site' },
          { label: <><LogoutOutlined className="logout-icon" /> Выход</>, value: '/' },
        ]}
        onChange={handleSegmentChange}
        defaultValue={currentPath}
        className="custom-segmented"
        style={{ backgroundColor: '#00aeef', marginRight: 'auto'  }}
      />
       

    </Space>

     

  </Header>
);
};

export default CustomHeader;
