import { Card, CardBody, Heading, Image } from "@chakra-ui/react"
import { Recipe } from "../Hooks/useRecipes"

interface Props {
    recipe: Recipe
}

const RecipeCard = ({  recipe } : Props) => {
  return (
    <Card maxW='sm' border={10} overflow="hidden">
        <Image src={recipe.thumbnail_url}/>
        <CardBody>
            <Heading>{recipe.name}</Heading>
        </CardBody>
    </Card>
  )
}

export default RecipeCard  