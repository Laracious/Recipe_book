import { GridItem, Show } from '@chakra-ui/react'
import NavBar from './NavBar'
import RecipeGrid from './RecipeGrid'

const Home = () => {

  return (
    <>
    <GridItem area="nav">
    <NavBar onSearch={function (searchText: string): void {
                  throw new Error('Function not implemented.')
              } }/>
    </GridItem>
     <Show above="lg">
     <GridItem area="aside" padding="10px" margin="100px 0 0 200px">
       Aside
     </GridItem>
   </Show>
   <GridItem area="main">
     <RecipeGrid />
   </GridItem>
 </>
  )
};

export default Home;