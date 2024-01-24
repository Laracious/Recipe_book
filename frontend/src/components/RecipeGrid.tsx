import { Grid, SimpleGrid, Skeleton, Text } from "@chakra-ui/react";
import useRecipes from "../Hooks/useRecipes";
import RecipeCard from "./RecipeCard";
import CardSkeleton from "./CardSkeleton";

const RecipeGrid = () => {
  const { recipes, error, isLoading } = useRecipes();
  const skeletons = [1, 2, 3, 4, 5, 6];

  return (
    <div style={{ display: "flex", justifyContent: "center", alignItems: "center" }}>
      {error && <Text>{error}</Text>}
      <SimpleGrid
        templateColumns="repeat(3, 1fr)"
        padding="10px"
        margin="100px"
        gap={8}
      >
        {isLoading && skeletons.map(skeleton => <CardSkeleton key={skeleton}/>)}
        {recipes.map((recipe) => (
          <RecipeCard key={recipe.id} recipe={recipe} />
        ))}
      </SimpleGrid>
    </div>
  );
};

export default RecipeGrid;
