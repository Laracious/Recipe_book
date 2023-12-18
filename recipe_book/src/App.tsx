import { Grid, GridItem, Show } from "@chakra-ui/react"
import NavBar from "./components/NavBar"
import RecipeGrid from "./components/RecipeGrid"


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
  </Grid>
    

  )

  
}

export default App