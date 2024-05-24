import React, { useState } from 'react';
import { Modal, Checkbox, Button } from 'antd';

const ExportData = ({ visible, onClose }) => {
  const [loadExcel, setLoadExcel] = useState(false);
  const [loadHTML, setLoadHTML] = useState(false);

  const handleLoadExcelChange = () => {
    setLoadExcel(!loadExcel);
  };

  const handleLoadHTMLChange = () => {
    setLoadHTML(!loadHTML);
  };

  const handleDownload = () => {
    // Обработка загрузки данных
    onClose(); // Закрыть модальное окно после загрузки
  };

  return (
    <Modal
      title="Экспорт данных"
      visible={visible}
      onCancel={onClose}
      footer={[
        
        <Button key="export" type="primary" onClick={handleDownload}>
          Загрузить
        </Button>,
      ]}
    >
      <Checkbox checked={loadExcel} onChange={handleLoadExcelChange}>
        Загрузить Excel
      </Checkbox>
      <Checkbox checked={loadHTML} onChange={handleLoadHTMLChange}>
        Загрузить HTML
      </Checkbox>
    </Modal>
  );
};

export default ExportData;
