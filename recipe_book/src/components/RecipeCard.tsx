import { Card, CardBody, HStack, Heading, Image } from "@chakra-ui/react";
import { Recipe } from "../Hooks/useRecipes";
import CriticScore from "./CriticScore";

interface Props {
  recipe: Recipe;
}

const RecipeCard = ({ recipe }: Props) => {
  return (
    <Card maxW="sm" borderRadius={10} overflow="hidden">
      <Image src={recipe.thumbnail_url} />
      <CardBody>
        <Heading>{recipe.name}</Heading>
        <HStack spacing={124}>
          <CriticScore  scoring={(recipe.user_ratings.score * 10).toFixed(1)} />
        </HStack>
      </CardBody>
    </Card>
  );
};

export default RecipeCard;
