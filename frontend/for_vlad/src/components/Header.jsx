import React, { useEffect, useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { Button, Layout, Menu, Dropdown, Typography, Space } from 'antd';
import { QuestionOutlined } from '@ant-design/icons';
import ExportData from './ExportData';
import '.././thems/style.css';
import { FileTextOutlined } from '@ant-design/icons';

const { Header } = Layout;
const { Text } = Typography;

const CustomHeader = () => {
  const location = useLocation();
  const currentPath = location.pathname;
  const [currentDate, setCurrentDate] = useState(new Date());

  const [exportDataVisible, setExportDataVisible] = useState(false);

  const handleOpenExportDataModal = () => {
    setExportDataVisible(true);
  };

  // Функция для закрытия модального окна
  const handleCloseExportDataModal = () => {
    setExportDataVisible(false);
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

  const menu = (
    <Menu>
      <Menu.Item key="1">
        <Link to="/your_group">Ваши группы</Link>
      </Menu.Item>
      <Menu.Item key="2" disabled>
        <Link to="/match2team">Сравнение по группам</Link>
      </Menu.Item>
      <Menu.Item key="3">
        <Link to="/your_vectorstudy">Ваши направления</Link>
      </Menu.Item>
      <Menu.Item key="4" disabled>
        <Link to="/match2team_vectorstudy">Сравнение по направлениям</Link>
      </Menu.Item>
    </Menu>
  );

  const menuTops = (
    <Menu>
      <Menu.Item key="1">
        <Link to="/tops_stud">Ученики</Link>
      </Menu.Item>

      <Menu.Item key="2">
        <Link to="/tops_team">Группы</Link>
      </Menu.Item>
      
    </Menu>
  );

  return (
    <Header style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', backgroundColor: '#00aeef' }}>
      <Text strong style={{ color: 'white' }}>
        Данные актуальны на {formatDate(currentDate)}
      </Text>
      <Space>

      <Button icon={<FileTextOutlined />} style={{backgroundColor: '#58c622'}} className="nav-link" type="primary" onClick={handleOpenExportDataModal}>
        Экспорт данных
      </Button>

      <ExportData visible={exportDataVisible} onClose={handleCloseExportDataModal} />


        <Button type="link">
          <Link to="/main" style={{ color: 'white', textDecoration: 'none' }} className="nav-link">Главная</Link>
        </Button>
        
        <Dropdown overlay={menuTops} placement="bottomCenter">
          <Button type="link" style={{ color: 'white' }} className="nav-link">Топы</Button>
        </Dropdown>

        <Button type="link">
          <Link to="/analys_kr" style={{ color: 'white', textDecoration: 'none' }} className="nav-link">Анализ КР</Link>
        </Button>

        <Dropdown overlay={menu} placement="bottomCenter">
          <Button type="link" style={{ color: 'white' }} className="nav-link">Группы/Направления</Button>
        </Dropdown>

        <Button type="link">
          <Link to="/scater_plot" style={{ color: 'white', textDecoration: 'none' }} className="nav-link">Диаграмма рассеяния</Link>
        </Button>

        <Button type="link">
          <Link to="/" style={{ color: 'white', textDecoration: 'none' }} className="nav-link">Выход</Link>
        </Button>
        
      </Space>
    </Header>
  );
};


export default CustomHeader;
