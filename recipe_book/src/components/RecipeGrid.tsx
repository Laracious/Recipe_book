import { SimpleGrid, Text } from "@chakra-ui/react";
import useRecipes from "../Hooks/useRecipes";
import RecipeCard from "./RecipeCard";

const RecipeGrid = () => {
  const { recipes, error } = useRecipes();

  return (
    <>
      {error && <Text>{error}</Text>}
      <SimpleGrid column={ {sm: 1, md: 2, lg: 3, xl: 5 }} padding="10px" spacing={10}>
        {recipes.map((recipe) => (
          <RecipeCard key={recipe.id} recipe={recipe} />
        ))}
      </SimpleGrid>
    </>
  );
};

export default RecipeGrid;
