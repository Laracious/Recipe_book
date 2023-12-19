import { SimpleGrid, Skeleton, Text } from "@chakra-ui/react";
import useRecipes from "../Hooks/useRecipes";
import RecipeCard from "./RecipeCard";
import CardSkeleton from "./CardSkeleton";

const RecipeGrid = () => {
  const { recipes, error, isLoading } = useRecipes();
  const skeletons = [1, 2, 3, 4, 5, 6];

  return (
    <>
      {error && <Text>{error}</Text>}
      <SimpleGrid
        column={{ sm: 1, md: 2, lg: 3, xl: 5 }}
        padding="10px"
        spacing={10}
      >
        {isLoading && skeletons.map(skeleton => <CardSkeleton key={skeleton}/>)}
        {recipes.map((recipe) => (
          <RecipeCard key={recipe.id} recipe={recipe} />
        ))}
      </SimpleGrid>
    </>
  );
};

export default RecipeGrid;
