import { HStack, Show, Switch, Text, useColorMode } from "@chakra-ui/react";
import React from "react";

const ColorModeSwitch = () => {
  const { toggleColorMode, colorMode } = useColorMode();

  return (

    <HStack  padding={5} position="absolute" top="0" right="0">
      <Show above="lg">
      <Switch
        colorScheme="green"
        isChecked={colorMode === "dark"}
        onChange={toggleColorMode}
        aria-label="Toggle Dark Mode"
      />
      
      <Text ml={2} fontWeight="bold">Dark Mode</Text>
      </Show>
    </HStack>
  );
};

export default ColorModeSwitch;
