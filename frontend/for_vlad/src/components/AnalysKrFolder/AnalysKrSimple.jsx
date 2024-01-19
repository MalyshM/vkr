import React, { useEffect, useRef, useState } from 'react';
import { Chart } from 'chart.js/auto';
import { Text } from '@chakra-ui/react';
import { BoxPlotChart } from '@sgratzl/chartjs-chart-boxplot';

const AnalysKrSimple = ({ tokenUsers, type, kr }) => {
  const [AnalysKrSimpleData, setAnalysKrSimpleData] = useState(null);
  const chartRef = useRef(null);

  useEffect(() => {
    const fetchAnalysKrSimpleData = async () => {
      try {
        if (type !== null && kr !== null) {
          const response = await fetch(`http://localhost:8090/api/kr_analyse_simple?type=${type}&kr=${kr}&token=${tokenUsers}`);
          const result = await response.json();
          setAnalysKrSimpleData(result);
        }
      } catch (error) {
        console.error('AnalysKrSimpleData - Error fetching attendance data:', error);
      }
    };
    fetchAnalysKrSimpleData();
  }, [type, kr, tokenUsers]);

  useEffect(() => {
    if (AnalysKrSimpleData) {
      const labels = Object.keys(AnalysKrSimpleData);
      const data = Object.values(AnalysKrSimpleData);


      const boxplotData = {
        labels: labels,
        datasets: [
          {
            label: 'Boxplot',
            data: data,
            backgroundColor: 'rgba(0, 123, 255, 0.5)',
            borderColor: 'rgba(0, 123, 255, 1)',
            borderWidth: 1,
          },
        ],
      };

      const config = {
        type: 'boxplot',
        data: boxplotData,
        options: {
          plugins: {
            legend: {
              display: false,
            },
          },
        },
      };

      const ctx = chartRef.current.getContext('2d');
      // new Chart(ctx, config);
      new BoxPlotChart(ctx,config);
    }
  }, [AnalysKrSimpleData]);

  if (!AnalysKrSimpleData) {
    return <div>Loading...</div>;
  }

  return (
    <div>
      <canvas ref={chartRef} width="400" height="200"></canvas>
    </div>
  );
};

export default AnalysKrSimple;