import {
  Card,
  CardBody,
  HStack,
  Heading,
  Image,
} from "@chakra-ui/react";
import { Recipe } from "../Hooks/useRecipes";
import CriticScore from "./CriticScore";
import Description from "./description";
import { useColorMode } from "@chakra-ui/react";

interface Props {
  recipe: Recipe;
}

const RecipeCard = ({ recipe }: Props) => {
  const { colorMode } = useColorMode();

  const cardBgColor = colorMode === "dark" ? "#1a202c" : "#a80863";
  const textColor = colorMode === "dark" ? "white" : "black";

  return (
    <Card
      width="300px"
      maxW="sm"
      borderRadius={10}
      overflow="hidden"
      margin="30px"
      boxShadow="xl"
      bg={cardBgColor}
      color={textColor}
    >
      <Image
        height={200}
        src={recipe.thumbnail_url}
        alt={`Thumbnail for ${recipe.name}`}
      />
      <CardBody>
        <Heading fontSize="xl" color={textColor}>
          {recipe.name}
        </Heading>
        <HStack spacing={3} justify="space-between">
          <Description descripe={recipe.description} />
          <CriticScore scoring={parseFloat((recipe.user_ratings.score * 10).toFixed(1))} />
        </HStack>
      </CardBody>
    </Card>
  );
};

export default RecipeCard;
