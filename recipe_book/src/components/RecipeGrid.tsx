import { Text } from "@chakra-ui/react";
import useRecipes from "../Hooks/useRecipes";

const RecipeGrid = () => {
  const {recipes, error} = useRecipes();

  return (
    <>
      {error && <Text>{error}</Text>}
      <ul>
        {recipes.map((recipe) => (
          <li key={recipe.id}>{recipe.name}</li>
        ))}
      </ul>
    </>
  );
};

export default RecipeGrid;
