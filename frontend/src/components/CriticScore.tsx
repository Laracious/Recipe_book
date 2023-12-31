import { Badge } from "@chakra-ui/react";

interface Props {
  scoring: number;
}

const CriticScore = ({ scoring }: Props) => {
  let color = scoring > 7.5 ? "green" : scoring > 5 ? "yellow" : "";
  return (
    <Badge fontSize="12p" colorScheme={color} paddingX={1} borderRadius="1px">
      {scoring}
    </Badge>
  );
};

export default CriticScore;