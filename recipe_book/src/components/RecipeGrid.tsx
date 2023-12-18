import { SimpleGrid, Text } from "@chakra-ui/react";
import useRecipes from "../Hooks/useRecipes";
import RecipeCard from "./RecipeCard";

const RecipeGrid = () => {
  const { recipes, error } = useRecipes();

  return (
    <>
      {error && <Text>{error}</Text>}
      <SimpleGrid column={3} spacing={10}>
        {recipes.map((recipe) => (
          <RecipeCard key={recipe.id} recipe={recipe} />
        ))}
      </SimpleGrid>
    </>
  );
};

export default RecipeGrid;
