import React, { useEffect, useState } from 'react';
import { Checkbox } from 'antd';
import ExportData from './ExportData';

const RequestCheckbox = ({ requestUrl , requestName, onUpdateRequests, onCheckboxChange, requestTeamName}) => {
  const [isChecked, setIsChecked] = useState(false);
  const [isModalVisible, setIsModalVisible] = useState(false);

useEffect(() => {
    const storedRequests = localStorage.getItem('selectedRequests');
    if (storedRequests) {
      const requestsArray = JSON.parse(storedRequests);
      if (requestsArray.some(req => req.url === requestUrl)) {
        setIsChecked(true);
      }
    }
    console.log('storedRequests',storedRequests)

  }, [requestUrl]);

const handleCheckboxChange = (e) => {
    const isChecked = e.target.checked;
    setIsChecked(isChecked);
    const storedRequests = JSON.parse(localStorage.getItem('selectedRequests')) || [];

    if (isChecked) {
      const newRequest = { url: requestUrl, name: requestName };
      localStorage.setItem('selectedRequests', JSON.stringify([...storedRequests, newRequest]));
      onUpdateRequests([...storedRequests, newRequest]);  
      

    } else {
      const updatedRequests = storedRequests.filter(req => req.url !== requestUrl);
      localStorage.setItem('selectedRequests', JSON.stringify(updatedRequests));
      onUpdateRequests(updatedRequests);
    }

  };

  const handleCloseModal = () => {
    setIsModalVisible(false);
  };

  return (
    <><Checkbox checked={isChecked} onChange={handleCheckboxChange}>
      {isChecked ? `Отчёт "${requestName}" сохранён` : `Сохранить отчёт по "${requestName}" ?`}
    </Checkbox>
    
    <ExportData
        visible={isModalVisible}
        onClose={handleCloseModal}
        requestName={requestName}
        requestTeamName={requestTeamName}
 />
        
        </>
  );
};

export default RequestCheckbox;
