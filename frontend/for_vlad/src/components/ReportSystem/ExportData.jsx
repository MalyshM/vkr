import React, { useState, useEffect } from 'react';
import { Modal, Button, Checkbox, List } from 'antd';
import { SendOutlined} from '@ant-design/icons';
const ExportData = ({ visible, onClose }) => {
  const [selectedRequests, setSelectedRequests] = useState([]);
  const [requests, setRequests] = useState([]);

  useEffect(() => {
    const storedRequests = JSON.parse(localStorage.getItem('selectedRequests'));
    if (storedRequests) {
      setRequests(storedRequests);
    }
  }, [visible]);

  useEffect(() => {
    const storedRequests = JSON.parse(localStorage.getItem('selectedRequests'));
    if (storedRequests) {
      setRequests(storedRequests);
    }
  }, [selectedRequests]);

  useEffect(() => {
    const interval = setInterval(() => {
      localStorage.removeItem('selectedRequests');
      setRequests([]);
    }, 1800000); // 30 минут в миллисекундах

    return () => clearInterval(interval); // Очищаем интервал при размонтировании
  }, []);


  const handleOk = async () => {
    const hrefsList = selectedRequests.map(req => req.url).join(',');
    const nameOfSheetList = selectedRequests.map((req, index) => req.name || `Sheet ${index + 1}`).join(',');
    const asCsv = true;

    console.log('Sending data:', {
      hrefs_list: hrefsList,
      name_of_sheet_list: nameOfSheetList,
      as_csv: asCsv,
    });

    const queryParams = new URLSearchParams({
      hrefs_list: hrefsList,
      name_of_sheet_list: nameOfSheetList,
      as_csv: asCsv.toString(),
    }).toString();

    const url = `http://moais-dashboard.ru:8082/api/reporting_system?${queryParams}`;

    try {
      const response = await fetch(url, {
        method: 'POST',
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(JSON.stringify(errorData));
      }

      const blob = await response.blob();
      const downloadUrl = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = downloadUrl;
      a.download = 'Данные_студентов.xlsx';
      document.body.appendChild(a);
      a.click();
      a.remove();

      console.log('File download initiated');
      onClose();
    } catch (error) {
      console.error('Error:', error);
    }
  };

  const handleCheckboxChange = (e, request) => {
    if (e.target.checked) {
      setSelectedRequests([...selectedRequests, request]);
    } else {
      setSelectedRequests(selectedRequests.filter(r => r.url !== request.url));
    }
  };

  return (
    <Modal
      title="Экспорт данных"
      visible={visible}
      onOk={handleOk}
      onCancel={onClose}
      okText="Получить" 
      cancelText="Отмена"
      
    >
      <List
        dataSource={requests}
        renderItem={request => (
          <List.Item>
            <Checkbox onChange={(e) => handleCheckboxChange(e, request)} checked={selectedRequests.some(r => r.url === request.url)}>
              {request.name || request.url}
            </Checkbox>
          </List.Item>
        )}
      />
    </Modal>
  );
};

export default ExportData;
