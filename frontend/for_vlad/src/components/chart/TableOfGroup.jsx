import React, { useState, useEffect } from 'react';
import { Table, Tooltip, Typography, Space, Button ,Row,Col} from 'antd';
import { QuestionCircleOutlined, UpOutlined, DownOutlined } from '@ant-design/icons';
import styled from 'styled-components';
import RequestCheckbox from '../ReportSystem/RequestCheckbox';
import { fetchWithTokenRefresh } from '../RefreshToken';

const { Text } = Typography;

const TableContainer = styled.div`
  background: white;
  padding: 16px;
  border-radius: 20px;
  border: 1px solid lavender;
  height: 34vh;
  overflow-y: auto;
`;
const HeaderContainer = styled.div`
  display: flex;
  align-items: center;
  margin-bottom: 16px;
`;

const TableOfGroup = ({ teamId, selectedLesson }) => {
  const [TableOfGroupData, setTableOfGroupData] = useState(null);
  const [sortColumn, setSortColumn] = useState({ key: '', ascending: true });
  const [requests, setRequests] = useState([]);

  useEffect(() => {
    const fetchTableOfGroup = async () => {
      try {
        if (teamId !== null) {
          const response = await fetchWithTokenRefresh(`http://moais-dashboard.ru:8082/api/attendance_num_for_stud_for_team_stat_table?id_team=${teamId}&name_of_lesson=${selectedLesson}`);
          const result = await response.json();
          setTableOfGroupData(result);
        }
      } catch (error) {
        console.error('Error fetching attendanceTotalPoints data:', error);
      }
    };
    fetchTableOfGroup();
  }, [teamId, selectedLesson]);

  const requestUrl = `http://moais-dashboard.ru:8082/api/attendance_num_for_stud_for_team_stat_table?id_team=${teamId}&name_of_lesson=${selectedLesson}`;

  const handleUpdateRequests = (updatedRequests) => {
    setRequests(updatedRequests);
  };

  const handleSort = (key) => {
    setSortColumn({ key, ascending: !sortColumn.ascending });
  };


  const sortedData = [...(TableOfGroupData || [])].sort((a, b) => {
    const aValue = a[sortColumn.key];
    const bValue = b[sortColumn.key];

    if (aValue < bValue) return sortColumn.ascending ? -1 : 1;
    if (aValue > bValue) return sortColumn.ascending ? 1 : -1;
    return 0;
  });

  const columns = [
    {
      title: '№',
      dataIndex: 'index',
      key: 'index',
      render: (_, __, index) => index + 1,
    },
    {
      title: 'ID',
      dataIndex: 'id',
      key: 'id',
    },
    {
      title: (
        <Space>
          Успеваемость
          <Button
            type="link"
            size="small"
            icon={sortColumn.key === 'Успеваемость' && sortColumn.ascending ? <UpOutlined /> : <DownOutlined />}
            onClick={() => handleSort('Успеваемость')}
          />
        </Space>
      ),
      dataIndex: 'Успеваемость',
      key: 'Успеваемость',
    },
    {
      title: (
        <Space>
          Посещение
          <Button
            type="link"
            size="small"
            icon={sortColumn.key === 'Посещаемость' && sortColumn.ascending ? <UpOutlined /> : <DownOutlined />}
            onClick={() => handleSort('Посещаемость')}
          />
        </Space>
      ),
      dataIndex: 'Посещаемость',
      key: 'Посещаемость',
    },
  ];

  const count = TableOfGroupData ? sortedData.length : 0;

  return (
    <TableContainer>
      <HeaderContainer>

        <Row>
          
          <Col span={24}>
          <Text strong style={{ fontSize: '22px', color: '#808080' }}>
            {selectedLesson ? `Название встречи: ${selectedLesson}` : 'Выберите встречу'}
          </Text>
          </Col >

          <Col span={24}>
          <Text type="danger" >
          {`Количество студентов пропустивших встречу: ${count}`}
          </Text>
          </Col>

        </Row>

      </HeaderContainer>

      <Table
        columns={columns}
        dataSource={sortedData}
        rowKey="id"
        pagination={false}
        scroll={{ y: 130 }}
        style={{ marginBottom: '10px' }}
      />

        <Tooltip title="Таблица отображающая отсутствующих студентов на выбранной учебной встрече">
          <QuestionCircleOutlined style={{ marginRight: 8 }} />
        </Tooltip>

        <RequestCheckbox
          requestUrl={requestUrl}
          requestName={`Студенты пропустившие встречу ${selectedLesson}`}
          onUpdateRequests={handleUpdateRequests}
          style={{ marginLeft: 'auto' }}
        />
      
    </TableContainer>
  );
};

export default TableOfGroup;
