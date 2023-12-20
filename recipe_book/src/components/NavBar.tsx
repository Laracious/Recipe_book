import { HStack, Image, Text } from "@chakra-ui/react";
import logo from "../assets/LOGO.png";
import ColorModeSwitch from "./colorModeSwitch";

const NavBar = () => {
  return (
    <HStack justifyContent="space-between" padding={5}>
      <HStack>
        <Image src={logo} boxSize="60px" alt="Recipe Book Logo" />
        <Text
          fontSize="3xl"
          fontWeight="bold"
          color="#a80863"
          textShadow="2px 2px 2px rgba(0, 0, 0, 0.5)"
        >
          Recipe Book
        </Text>
      </HStack>
      <ColorModeSwitch />
    </HStack>
  );
};

export default NavBar;