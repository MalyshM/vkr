import React, { useEffect, useRef ,useState} from 'react';
import { Bar } from 'react-chartjs-2';
import { Chart } from 'chart.js/auto';
import ChartDataLabels from 'chartjs-plugin-datalabels';
Chart.register(ChartDataLabels);
<script src="https://cdnjs.cloudflare.com/ajax/libs/chartjs-plugin-datalabels/2.2.0/chartjs-plugin-datalabels.min.js" integrity="sha512-JPcRR8yFa8mmCsfrw4TNte1ZvF1e3+1SdGMslZvmrzDYxS69J7J49vkFL8u6u8PlPJK+H3voElBtUCzaXj+6ig==" crossorigin="anonymous" referrerpolicy="no-referrer"></script>

const MatchTotalPointsTeams = ({ teamId1,teamId2}) => {
  const [totalPointData, setTotalPointData] = useState(null);
  const chartRef = useRef(null);

  useEffect(() => {
    if (chartRef.current) {
      // Уничтожаем чарт при размонтировании компонента
      return () => {
        if (chartRef.current) {
          const chartInstance = Chart.getChart(chartRef.current); // Получаем экземпляр чарта
          if (chartInstance) {
            chartInstance.destroy(); // Уничтожаем чарт
          }
        }
      };
    }
  }, []);

  

  // console.log('selectedTeam changed:', selectedTeam);
  console.log('team ID 1 in MatchTotalPointsTeams:', teamId1, 'team ID 2 in MatchTotalPointsTeams:', teamId2);
  
  useEffect(() => {
  const fetchtotalPointData = async () => {
    try {
        if (teamId1 !== null && teamId2 !== null) {
        const response = await fetch(`http://localhost:8090/api/total_points_stud_for_teams?id_team1=${teamId1}&id_team2=${teamId2}`);
        const result = await response.json();
        // Обновляем состояние с полученными данными /api/total_points_stud_for_teams
        setTotalPointData(result);
      }
    } catch (error) {
      console.error('Error fetching attendance data:', error);
    }
  };
  fetchtotalPointData(); 
},[teamId1,teamId2]);

if (!totalPointData) {
  return <div>Loading...</div>;
}

const colors = {
  [teamId2]: 'rgba(217,68,58, 0.5)', // Цвет для teamId1
  [teamId1]: 'rgba(177,185,253, 0.7)', // Цвет для teamId2
};

const data = {
    labels: totalPointData.map(item => `${item.id} (${item.team_name})`),
    datasets: [
      {
        label: 'Средний балл',
        data: totalPointData.map(item => item.total_points),
        backgroundColor: totalPointData.map(item => colors[item.team_id]),
        borderColor: 'rgb(0,174,239)',
        borderWidth: 0,
        

      },
    ],
  };

const options = {
  
  scales: {
    x: {
      ticks: {
        display: false,
      },
      type: 'category',
      position: 'bottom',
      title: {
        display: true,
        text: `Студенты групп ${totalPointData[0]?.team_name || ''} и ${totalPointData[1]?.team_name || ''}`,
        font: {
          size: 20, // Размер шрифта названия оси X
          fontColor: 'black',
          family: 'Trebuchet MS'
        },
      },
    },
    y: {
      type: 'linear', // изменение типа шкалы на категорию
      position: 'left',
      title: {
        display: true,
        text: 'Баллы',
        font: {
          size: 20, // Размер шрифта названия оси X
          fontColor: 'black',
          family: 'Trebuchet MS'
        },
      },
    },
  },
  plugins: {
    
    datalabels: {
      display: true,
        anchor: 'end',
        align: 'end',
        color: 'black',
        formatter: (value, context) => {
          const roundedValue = (value).toFixed(1);
          return `${roundedValue}`;
        },
      },

    title: {
      display: true,
      text: `Успеваемость групп ${totalPointData[0]?.team_name || ''} и ${totalPointData[1]?.team_name || ''}`,
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
  maintainAspectRatio: false,
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
      borderRadius: 5, 
    },
  },
  

  animation: {
    duration: 2000,
  },

};


  return <Bar ref={chartRef} data={data} options={options} />;
};

export default MatchTotalPointsTeams;
