import { Grid, GridItem, Show } from "@chakra-ui/react"
import NavBar from "./components/NavBar"
import RecipeGrid from "./components/RecipeGrid"
import SignUp from "./components/SignUp"
import SignIn from "./components/SignIn"
import { Routes, Route} from "react-router-dom"


function App() {
  
  return (

  <Grid templateAreas={{
    base: `"nav " " main"`,
    lg: `"nav nav" "aside main"`
  }}>
    <GridItem area="nav" >
      <NavBar />
       
        
        
    </GridItem>
    <Show above="lg">
    <GridItem area="aside" >Aside</GridItem>
    </Show>
    <GridItem area="main" >
      <RecipeGrid />
      </GridItem>
      <Routes>
        <Route path="/Sign-up" element={<SignUp />}/>
        <Route path="/Sign-in" element={<SignIn />}/>
      </Routes>
  </Grid>
    

  )

  
}

export default App
