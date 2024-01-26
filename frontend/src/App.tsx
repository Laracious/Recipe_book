import { Grid, GridItem, Show } from "@chakra-ui/react";
import SignUp from "./components/SignUp";
import SignIn from "./components/SignIn";
import { Route, Routes } from "react-router-dom";
import { useState } from "react";
import Home from "./components/home";
import "./App.css"
import Footer from "./components/Footer";
import { useMediaQuery } from 'react-responsive';

export interface RecipeQuery {
  onSearch: (searchText: string) => void;
} 

function App() {
  const isMobile = useMediaQuery({ query: '(max-width: 767px)' });
  const isTablet = useMediaQuery({ query: '(min-width: 768px) and (max-width: 1023px)' });
  const isDesktop = useMediaQuery({ query: '(min-width: 1024px)' });
  
  return (
    <div className="page-container">
      <div className="content-wrap">
        <Grid
          templateAreas={{
          base: `"nav " " main"`,
          lg: `"nav nav" "main"`,
         }}
          templateColumns="repeat(1, 1fr)"
          gap={0}
      
          >
        
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/Sign-up" element={<SignUp />} />
            <Route path="/Sign-in" element={<SignIn />} />
          </Routes>
        </Grid>
        <Footer />
      </div>
    </div>
  );
}

export default App;
