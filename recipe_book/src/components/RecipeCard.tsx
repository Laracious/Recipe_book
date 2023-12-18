import { Card, CardBody, Heading, Image } from "@chakra-ui/react"
import { Recipe } from "../Hooks/useRecipes"
import CriticScore from "./CriticScore"

interface Props {
    recipe: Recipe
}

const RecipeCard = ({  recipe } : Props) => {
  return (
    <Card maxW="sm" borderRadius={10} overflow="hidden">
        <Image src={recipe.thumbnail_url}/>
        <CardBody>
            <Heading>{recipe.name}</Heading>
            <CriticScore scoring={(recipe.user_ratings.score * 10).toFixed(1)}/>
        </CardBody>
    </Card>
  )
}

export default RecipeCard  