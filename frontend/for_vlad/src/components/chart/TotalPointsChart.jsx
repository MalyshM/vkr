
import React, { useEffect, useState } from 'react';
import { Bar } from 'react-chartjs-2';
import { useNavigate  } from 'react-router-dom';

const TotalPointsChart = ({ teamId }) => {
  // const navigate = useNavigate ();
  const [chartData, setChartData] = useState(null);
  const navigate = useNavigate ();

  const handleChartClick = (_, elements) => {
    if (elements && elements.length > 0) {
      const clickedElement = elements[0];
      const dataIndex = clickedElement.index;
      const studentId = sortedData_total[dataIndex]?.id;
      navigate (`/student/${studentId}/${teamId}`);
    }
  };

  console.log('team ID in YoyalPoint (new realization):', teamId);

  useEffect(() => {
    const fetchTotalPointsData = async () => {
      try {
        if (teamId !== null) {
        const response = await fetch(`http://localhost:8090/api/total_points_per_stud_for_team?id_team=${teamId}`);
        const result = await response.json();
        setChartData(result);
        }
      } catch (error) {
        console.error('Error fetching TotalPoints data:', error);
      }
    };

    fetchTotalPointsData();
  }, [teamId]);

  if (!chartData) {
    return <div>Loading...</div>;
  }

  const sortedData_total = [...chartData].sort((a, b) => b.Успеваемость - a.Успеваемость);
  
  const sortedData_map_total= sortedData_total.map(item => parseFloat(item.Успеваемость.toFixed(3)));

  const data = {
    labels: sortedData_total.map(item => item.id),
    datasets: [
      {
        label: 'Успеваемость',
        data: sortedData_map_total,
        backgroundColor: 'rgba(75, 192, 192, 0.2)',
        borderColor: 'rgb(0,174,239)',
        borderWidth: 3,
      },
    ],
  };

  const options = {
    onClick: handleChartClick,
    scales: {
      x: {
        type: 'category',
        position: 'bottom',
        title: {
          display: true,
          text: 'Идентификатор студента',
          font: {
            size: 20, // Размер шрифта названия оси X
            fontColor: 'black',
            family: 'Trebuchet MS'},
        },
      },
      y: {
        type: 'linear',
        position: 'left',
        title: {
          display: true,
          text: 'Успеваемость (баллы)',
          font: {
            size: 20, // Размер шрифта названия оси X
            fontColor: 'black',
            family: 'Trebuchet MS'
        },
      },
    },
  },
    plugins: {
      title: {
        display: true,
        text: 'Успеваемость студентов выбранной подгруппы дисциплины ПиОА',
        font: {
          size: 22,
          fontColor: 'black',
          family: 'Trebuchet MS'
        },
      },
    
      legend: {
        display: false,
        position: 'top',
      },
    },
    layout: {
      padding: {
        left: 50,
        right: 50,
        top: 0,
        bottom: 0,
      },
    },
    elements: {
      bar: {
        barThickness: 400,
        borderRadius: 10,
      },
    },
  };

  return <Bar data={data} options={options} />;
};

export default TotalPointsChart;
