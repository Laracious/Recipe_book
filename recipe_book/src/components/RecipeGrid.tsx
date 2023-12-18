import { useEffect, useState } from "react";
import apiClient from "../Services/api-client";
import { Text } from "@chakra-ui/react";

interface Recipe {
  id: number;
  name: string;
}

interface FetchRecipesRespone {
  count: number;
  results: Recipe[];
}

const RecipeGrid = () => {
  const [recipes, setRecipes] = useState<Recipe[]>([]);
  const [error, setError] = useState("");

  useEffect(() => {
    
    apiClient
      .get<FetchRecipesRespone>("/list")
      .then((res) => setRecipes(res.data.results))
      .catch((err) => setError(err.message));
  }, []);

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
