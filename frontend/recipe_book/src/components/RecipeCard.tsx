import { Card, CardBody,HStack, Heading, Image, Tooltip,} from "@chakra-ui/react";
import { Recipe } from "../Hooks/useRecipes";
import CriticScore from "./CriticScore";
import Description from "./description";

interface Props {
  recipe: Recipe;
}

const RecipeCard = ({ recipe }: Props) => {
  return (
    <Card
      width="300px"
      maxW="sm"
      borderRadius={10}
      overflow="hidden"
      margin="10px"
      boxShadow="xl"
      bg="#29a9ed"
    >
      <Image height={200} src={recipe.thumbnail_url} alt={recipe.name} />
      <CardBody>
        <Heading fontSize="xl" color="black">
          {recipe.name}
        </Heading>
        <HStack spacing={3} justify="space-between">
          <Description descripe={recipe.description} />
          <CriticScore
            scoring={parseFloat((recipe.user_ratings.score * 10).toFixed(1))}
          />
        </HStack>
      </CardBody>
    </Card>
  );
};

export default RecipeCard;
