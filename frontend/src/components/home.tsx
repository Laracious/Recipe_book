import { GridItem, Show } from '@chakra-ui/react'
import NavBar from './NavBar'
import RecipeGrid from './RecipeGrid'

const Home = () => {

  return (
    <>
    <GridItem area="nav" width="100%">
      <div>
        <NavBar onSearch={function (searchText: string): void {
                      throw new Error('Function not implemented.' )
              } }/>
      </div>
    </GridItem>
   <GridItem area="main">
     <RecipeGrid />
   </GridItem>
 </>
  )
}

export default Home;