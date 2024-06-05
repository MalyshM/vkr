import React, { useState } from 'react';
import { Button, Modal, Input } from 'antd';
import { useNavigate } from 'react-router-dom';

const SearchStudentModal = ({ visible, onClose }) => {
  const [studentId, setStudentId] = useState('');
  const navigate = useNavigate();

  const handleSearch = () => {
    // Переход на страницу студента с указанным ID
    navigate(`/student/${studentId}`);
    // Закрываем модальное окно
    onClose();
  };

  return (
    <Modal
      title="Поиск студента"
      visible={visible}
      onCancel={onClose}
      footer={[
        <Button key="cancel" onClick={onClose}>
          Отмена
        </Button>,
        <Button key="search" type="primary" onClick={handleSearch}>
          Поиск
        </Button>,
      ]}
    >
      <Input placeholder="Введите ID студента" value={studentId} onChange={(e) => setStudentId(e.target.value)} />
    </Modal>
  );
};

export default SearchStudentModal;
