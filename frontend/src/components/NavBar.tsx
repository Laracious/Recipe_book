import { Button, Flex, HStack, Image, Text } from "@chakra-ui/react";
import logo from "../assets/LOGO.png";
import ColorModeSwitch from "./colorModeSwitch";
import SearchInput from "./Searchinput";
import { Link } from "react-router-dom";

interface Props {
  onSearch: (searchText: string) => void;
}

const NavBar = ({ onSearch }: Props) => {
  return (
    <HStack padding={5} bg="#2C3E50" boxShadow="md">
      <HStack>
        <Image src={logo} boxSize="60px" alt="Recipe Book Logo" />

        <Text
          whiteSpace="nowrap"
          fontSize="3xl"
          fontWeight="bold"
          color="#a80863"
          textShadow="2px 2px 2px rgba(0, 0, 0, 0.5)"
        >
          Recipe Book
        </Text>

        <SearchInput onSearch={onSearch} />
        <Button
          as={Link}
          to="/sign-in"
          variant="link"
          color="#a80863"
          fontWeight="bold"
          borderWidth="2px"
          borderColor="#a80863"
          borderRadius="md"
          backgroundColor="orange"
          padding="0.3rem 0.5rem"
          _hover={{
            textDecoration: "underline",
            transform: "scale(1.05)",
            transition: "transform 0.3s",
          }}
        >
          Sign in
        </Button>
        <ColorModeSwitch />
      </HStack>
    </HStack>
  );
};

export default NavBar;
