import React, { useEffect, useState } from 'react';
import { Checkbox } from 'antd';

const RequestCheckbox = ({ requestUrl , requestName, onUpdateRequests }) => {
  const [isChecked, setIsChecked] = useState(false);


useEffect(() => {
    const storedRequests = localStorage.getItem('selectedRequests');
    if (storedRequests) {
      const requestsArray = JSON.parse(storedRequests);
      if (requestsArray.some(req => req.url === requestUrl)) {
        setIsChecked(true);
      }
    }
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

  return (
    <Checkbox checked={isChecked} onChange={handleCheckboxChange}>
    {requestName}
  </Checkbox>
  );
};

export default RequestCheckbox;
