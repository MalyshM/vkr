import React from 'react';
import { Button, Layout, Typography, Card } from 'antd';
import { Link } from 'react-router-dom';

const { Content } = Layout;
const { Title } = Typography;


const HomePage = () => {

    return (

      <Layout style={{ minHeight: '100vh', backgroundColor: '#00aeef' }}>
      <Content style={{ display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
        <Card
          style={{
            padding: '32px',
            borderWidth: '2px',
            borderRadius: '16px',
            boxShadow: '0 4px 8px rgba(0, 0, 0, 0.1)',
            textAlign: 'center',
            borderColor: '#1A1A1A',
            height: '300px',
            width: '500px',
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            justifyContent: 'center',
            backgroundColor: 'white'
          }}
        >
          <Title level={1} style={{ marginBottom: '24px', fontFamily: 'Trebuchet MS' }}>
            Добро пожаловать!
          </Title>

          <Link to='/login'>
          <Button
            type="primary"
            style={{ width: '200px', margin: '8px' }}
            size="large"
          >
            Войти
          </Button>
          </Link>

          <Link to="/register"> 
          <Button
            type="default"
            style={{ width: '200px', margin: '8px' }}
            size="large"
          >
            Создать аккаунт
          </Button>
          </Link>
          
        </Card>
      </Content>
    </Layout>
    
      );
    };
    
export default HomePage;
