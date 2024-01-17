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
import MatchToTeamPage from './components/Match/MatchToTeamPage';

import Header from "./components/Header";
import MatchTwoTeamVectorStudy from "./components/Match/MatchTwoTeamVectorStudy"
// import TableOfGroup from './components/TableFolder/TableOfGroup'; 

function App() {


  return (
    <ChakraProvider theme={theme}>
      <Router>
      <Header />
    <AuthProvider>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<RegistrationPage />} />
        <Route path="/main" element={<MainPage />} />
        <Route path="/match2team" element={<MatchToTeamPage />} />
        <Route path={"/student/:studentId/:teamId/:teamName"} element={<GeneralStudPage />} />
        <Route path="/match2team_vectorstudy" element={<MatchTwoTeamVectorStudy/>} />

      </Routes>
    </AuthProvider>
  </Router>
  </ChakraProvider>
  );
}
export default App;

