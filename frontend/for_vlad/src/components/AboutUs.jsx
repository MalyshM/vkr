import React from 'react';
import { Layout, Typography, Row, Col, Avatar, Image } from 'antd';
import '.././thems/style.css';
import vlad from '../thems/photovlad.jpg'
import miha from '../thems/miha.jpg'

const { Content } = Layout;
const { Title } = Typography;

const AboutUs = () => {
  const data = [
    {
      name: <>Михаил Малыш - BackEnd </>,
      
      image: miha,
    },
    {
      name: <>Владислав Плахота - FrontEnd </>,
      image: vlad, 
    },
  ];
  
    return (
      <Layout>
        <Content style={{ padding: '50px' }}>

          <Row gutter={[16, 16]} justify="center">
            {data.map((person, index) => (
              <Col key={index} xs={24} sm={12} md={8} lg={6}>
                <Image 
                  src={person.image} 
                  alt={person.name} 
                  width={300} 
                  height={300}
                  style={{ borderRadius: '50%' }} 
                />
                <Title level={4} style={{ marginTop: '16px', marginLeft: "20px" }}>
                  {person.name}
                </Title>
              </Col>
            ))}
          </Row>

        </Content>
      </Layout>
    );
  };

export default AboutUs;