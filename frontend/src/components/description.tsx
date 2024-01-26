import React from "react";
import { Button, Tooltip } from "@chakra-ui/react";

interface Props {
  descripe: string;
}

const Description = ({ descripe }: Props) => {
  return (
    <Tooltip label={descripe} placement="top">
      <Button
        background="#075050"        
        variant="ghost"
        fontSize="12px"
        paddingX={1}
        height="15px"
        borderRadius="4px"
        _hover={{ bg: "transparent" }} 
      >
        Description
      </Button>
    </Tooltip>
  );
};

export default Description;
