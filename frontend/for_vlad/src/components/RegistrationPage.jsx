import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from './useAuth';

import { Button, Layout, Typography, Card, Form, Input, Radio, Space } from 'antd';
import { CloseOutlined } from '@ant-design/icons';

import { useToast } from '@chakra-ui/react';

import { fetchWithTokenRefresh } from './RefreshToken';

const RegistrationPage = () => {
  const { Header, Content, Footer } = Layout;
  const { Title } = Typography;

  const [FIO, setFIO] = useState('');
  const [role, setRole] = useState('');
  const [isAdmin, setIsAdmin] = useState(false);
  const [isCurator, setIsCurator] = useState(false);
  const [isTeacher, setIsTeacher] = useState(false);
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [email, setEmail] = useState('');
  const [responseMessage, setResponseMessage] = useState('');
  const navigate = useNavigate();
  const { setUserToken } = useAuth(); 
  const toast = useToast();

  const handleRoleChange = (e) => {
    const selectedRole = e.target.value;
    setRole(selectedRole);

    // Сбросить все состояния ролей
    setIsAdmin(false);
    setIsCurator(false);
    setIsTeacher(false);

    // Установить состояние для выбранной роли
    if (selectedRole === 'admin') {
      setIsAdmin(true);
    } else if (selectedRole === 'curator') {
      setIsCurator(true);
    } else if (selectedRole === 'teacher') {
      setIsTeacher(true);
    }
  };


  const register = async () => {
    if (!username || !password || !FIO || !email || !role) {
      toast({
        title: 'Ошибка',
        description: 'Пожалуйста, заполните все поля!',
        status: 'error',
        duration: 3000, // Продолжительность отображения в миллисекундах
        isClosable: true,
      });
      return;
    }
    try {
      const response = await fetch('http://moais-dashboard.ru:8082/api/registration_standard', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          FIO,
          isAdmin,
          isCurator,
          isTeacher,
          role,
          username,
          password,
          email,
        }),
      });

      const result = await response.json();

      if (response.ok) {
        setUserToken(result.access_token); 
        setResponseMessage(`Registration successful! Welcome, ${username}!, Access Token: ${result.access_token}`);
        navigate('/main');
      } else {
        setResponseMessage(`Registration failed: ${result.detail}`);
      }
    } catch (error) {
      console.error('Error during registration:', error);
      setResponseMessage('An error occurred during registration.');
    } 
  };

  return (
    <Layout style={{ minHeight: '100vh', backgroundColor: '#00aeef', display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
      <Card
        style={{
          width: '500px',
          borderWidth: '2px',
          borderRadius: '8px',
          padding: '24px',
          boxShadow: '0 4px 8px rgba(0, 0, 0, 0.1)',
          borderColor: '#1A1A1A',
          backgroundColor: 'white',
        }}
      >
        <Space style={{ display: 'flex', justifyContent: 'space-between', width: '100%' }}>
          <Title level={2}>Регистрация</Title>
          <Link to="/">
            <Button type="text" icon={<CloseOutlined />} />
          </Link>
        </Space>

        <Form layout="vertical">
          <Form.Item label="Роль:">
            <Radio.Group onChange={handleRoleChange} value={role}>
              <Radio value="teacher">Преподаватель</Radio>
              <Radio value="curator">Куратор</Radio>
            </Radio.Group>
          </Form.Item>

          <Form.Item label="ФИО:" required>
            <Input
              type="text"
              value={FIO}
              onChange={e => setFIO(e.target.value)}
              placeholder="Введите ФИО"
            />
          </Form.Item>

          <Form.Item label="Логин:" required>
            <Input
              type="text"
              value={username}
              onChange={e => setUsername(e.target.value)}
              placeholder="Введите логин"
              autoComplete="off"
            />
          </Form.Item>

          <Form.Item label="Пароль:" required>
            <Input
              type="password"
              value={password}
              onChange={e => setPassword(e.target.value)}
              placeholder="Введите пароль"
              autoComplete="off"
            />
          </Form.Item>

          <Form.Item label="Адрес электронной почты:" required>
            <Input
              type="email"
              value={email}
              onChange={e => setEmail(e.target.value)}
              placeholder="Введите электронную почту"
              autoComplete="off"
            />
          </Form.Item>

          <Button type="primary" style={{ width: '100%' }} onClick={register}>
            Подтвердить
          </Button>
        </Form>
      </Card>
    </Layout>
  );
};

export default RegistrationPage;
