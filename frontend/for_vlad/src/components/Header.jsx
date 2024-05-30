import React, { useEffect, useState } from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import { Button, Layout, Menu, Dropdown, Typography, Space, Segmented } from 'antd';
import { QuestionOutlined } from '@ant-design/icons';
import ExportData from './ExportData';
import '.././thems/style.css';
import { HomeOutlined, TrophyOutlined, TeamOutlined, MehOutlined, AreaChartOutlined, GroupOutlined, AimOutlined, DotChartOutlined, LogoutOutlined, FileTextOutlined } from '@ant-design/icons';

const { Header } = Layout;
const { Text } = Typography;

const CustomHeader = () => {
  const location = useLocation();
  const currentPath = location.pathname;
  const [currentDate, setCurrentDate] = useState(new Date());
  const navigate = useNavigate();

  const [exportDataVisible, setExportDataVisible] = useState(false);

  const handleOpenExportDataModal = () => {
    setExportDataVisible(true);
  };

  // Функция для закрытия модального окна
  const handleCloseExportDataModal = () => {
    setExportDataVisible(false);
  };

  const handleSegmentChange = (value) => {
    navigate(value);
  };

  useEffect(() => {
    // Обновляем текущую дату каждый час
    const intervalId = setInterval(() => {
      setCurrentDate(new Date());
    }, 3600000); // 1 час в миллисекундах

    // Очищаем интервал при размонтировании компонента
    return () => clearInterval(intervalId);
  }, []);

  const formatDate = (date) => {
    const options = { year: 'numeric', month: 'long', day: 'numeric' };
    return date.toLocaleDateString('ru-RU', options);
  };

  // Проверьте, является ли текущий путь страницей авторизации
  const isAuthPage = ["/login", "/register", "/"].includes(currentPath);

  // Если это страница авторизации, не отображайте хедер
  if (isAuthPage) {
    return null;
  }

return (
  <Header style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', backgroundColor: '#00aeef' }}>
    {/* <Text strong style={{ color: 'white' }}>
      Данные актуальны на {formatDate(currentDate)}
    </Text> */}
    <Space>
      

      <Segmented
        options={[
          { label: <><HomeOutlined /> Главная</>, value: '/main' },
          { label: <><TrophyOutlined /> Топы студентов</>, value: '/tops_stud' },
          { label: <><TeamOutlined /> Топы команд</>, value: '/tops_team' },
          { label: <><MehOutlined /> Отстающие</>, value: '/least' },
          { label: <><AreaChartOutlined /> Анализ КР</>, value: '/analys_kr' },
          { label: <><GroupOutlined /> Ваши группы</>, value: '/your_group' },
          { label: <><AimOutlined /> Ваши направления</>, value: '/your_vectorstudy' },
          { label: <><DotChartOutlined /> Диаграмма рассеяния</>, value: '/scater_plot' },
          { label: <><LogoutOutlined className="logout-icon" /> Выход</>, value: '/' },
        ]}
        onChange={handleSegmentChange}
        defaultValue={currentPath}
        className="custom-segmented"
        style={{ backgroundColor: '#00aeef' }}
      />

    </Space>
    
    <Button icon={<FileTextOutlined />} style={{ backgroundColor: '#58c622' }} className="nav-link" type="primary" onClick={handleOpenExportDataModal}>
        Экспорт данных
      </Button>

      <ExportData visible={exportDataVisible} onClose={handleCloseExportDataModal} />
  </Header>
);
};

export default CustomHeader;
