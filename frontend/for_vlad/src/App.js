import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import HomePage from './components/HomePage';
import LoginPage from './components/LoginPage';
import RegistrationPage from './components/RegistrationPage';
import MainPage from './components/MainPage';
import {AuthProvider} from './components/useAuth' ;

import {ChakraProvider } from '@chakra-ui/react'
import theme from './thems/theme'; 

import GeneralStudPage from './components/InfoAboutStudients/GeneralStudPage';
import MatchToTeamPage from './components/Match/MatchForGroup/MatchToTeamPage';

import Header from "./components/Header";
import MatchTwoTeamVectorStudy from "./components/VectorStudy/Match/MatchTwoTeamVectorStudy"
import YourGroup from './components/Match/Group/YourGroup';
import YourVectorStudy from './components/VectorStudy/AllUsers/YourVectorStudy';

import AnalysKr from './components/AnalysKrFolder/AnalysKr';
import { NumberItemsProvider } from './components/chart/NumberItemsContext';

import ScaterPlotPage from './components/Scatter_Plot/ScaterPlotPage';

import TopsPage from './components/Tops/TopsPage'; 

function App() {


  return (
    <ChakraProvider theme={theme}>
      <Router>
      <Header />
    <AuthProvider>
      <NumberItemsProvider>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<RegistrationPage />} />
        <Route path="/main" element={<MainPage />} />
        <Route path={"/main/:teamId/:teamName"} element={<MainPage />} />
        <Route path="/match2team" element={<MatchToTeamPage />} />
        <Route path={"/student/:studentId/:teamId/:teamName"} element={<GeneralStudPage />} />
        <Route path="/match2team_vectorstudy" element={<MatchTwoTeamVectorStudy/>} />
        <Route path="/your_group" element={<YourGroup/>} />
        <Route path="/your_vectorstudy" element={<YourVectorStudy/>} />
        <Route path="/analys_kr" element={<AnalysKr/>} />
        <Route path="/scater_plot" element={<ScaterPlotPage/>}/>
        <Route path='/tops' element={<TopsPage/>}/>

      </Routes>
      </NumberItemsProvider>
    </AuthProvider>
  </Router>
  </ChakraProvider>
  );
}
export default App;

