import { Grid, GridItem, Show } from "@chakra-ui/react";
import NavBar from "./components/NavBar";
import RecipeGrid from "./components/RecipeGrid";
import SignUp from "./components/SignUp";
import SignIn from "./components/SignIn";
import { Route, Routes } from "react-router-dom";
import { useState } from "react";

export interface RecipeQuery {
  onSearch: (searchText: string) => void;
}

function App() {
  const [recipeQuery, setRecipeQuery] = useState<RecipeQuery>(
    {} as RecipeQuery
  );
  return (
    <Routes>
      <Route path="/" element={}></Route>

      <Route path="/Sign-up" element={<SignUp />} />
      <Route path="/Sign-in" element={<SignIn />} />
    </Routes>

    //<<<<<<< HEAD
    // <div>
    //   <Grid
    //     templateColumns="repeat(5, 1fr)"
    //     gap={0}
    //     templateAreas={{
    //       base: `"nav " " main"`,
    //       lg: `"nav nav" "aside main"`,
    //     }}
    //   >
    //     <GridItem area="nav">
    //       <NavBar onSearch={(searchText) => setRecipeQuery({ ...recipeQuery, })}/>
    //       <Routes>
    //         <Route path="/Sign-up" element={<SignUp />} />
    //         <Route path="/Sign-in" element={<SignIn />} />
    //       </Routes>
    //     </GridItem>
    //     <Show above="lg">
    //       <GridItem area="aside" padding="10px" margin="100px 0 0 200px">
    //         Aside
    //       </GridItem>
    //     </Show>
    //     <GridItem area="main">
    //       <RecipeGrid />
    //     </GridItem>
    //   </Grid>
    // </div>
  );

  // <Grid
  //   templateAreas={{
  //     base: `"nav " " main"`,
  //     lg: `"nav nav" "aside main"`,
  //   }}
  // >
  //   <GridItem area="nav">
  //     <NavBar />
  //   </GridItem>
  //   <Show above="lg">
  //     <GridItem area="aside">Aside</GridItem>
  //   </Show>
  //   <GridItem area="main">
  //     <RecipeGrid />
  //   </GridItem>
  //   <Routes>
  //     <Route path="/Sign-up" element={<SignUp />} />
  //     <Route path="/Sign-in" element={<SignIn />} />
  //   </Routes>
  // </Grid>;

  //>>>>>>> 6acb0b2e2e708f4dee60172bf28ed2224f88798d
}

export default App;
