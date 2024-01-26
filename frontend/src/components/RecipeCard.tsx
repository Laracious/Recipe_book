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
import Video from "./Video";

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
      margin="10px"
      boxShadow="xl"
      bg={cardBgColor}
      color={textColor}
    >
      <Image
        height={200}
        src={recipe.image}
        alt={`Thumbnail for ${recipe.name}`}
      />
      <CardBody>
        <Heading fontSize="xl" color={textColor}>
          {recipe.name}
        </Heading>
        <HStack spacing={3} justify="space-between">
          <Description descripe={recipe.description} />
          <CriticScore scoring={parseFloat((recipe.user_rating.score * 10).toFixed(1))} />
          <Video watch={recipe.video} />
        </HStack>
      </CardBody>
    </Card>
  );
};

export default RecipeCard;
