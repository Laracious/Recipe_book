import { HStack, Image, Text, } from "@chakra-ui/react";
import logo from "../assets/LOGO.png";
import ColorModeSwitch from "./colorModeSwitch";
import SearchInput from "./Searchinput";
import { Link } from "react-router-dom";

interface Props {
  onSearch: (searchText: string) => void;
}
<<<<<<< HEAD:frontend/recipe_book/src/components/NavBar.tsx
const NavBar = ({ onSearch}: Props) => {
  return (
    <HStack  padding={5} >
      <HStack >
        <Image src={logo} boxSize="60px" alt="Recipe Book Logo" />
=======

const NavBar = ({ onSearch }: Props) => {
  return (
    <HStack padding={5} bg="#2C3E50" boxShadow="md">
      <HStack>
        <Image src={logo} boxSize="60px" alt="Recipe Book Logo" />

>>>>>>> f6acfede9528ff1e2154abd1cd83fe58dcb034a8:frontend/src/components/NavBar.tsx
        <Text
          whiteSpace="nowrap"
          fontSize="3xl"
          fontWeight="bold"
          color="#a80863"
          textShadow="2px 2px 2px rgba(0, 0, 0, 0.5)"
<<<<<<< HEAD:frontend/recipe_book/src/components/NavBar.tsx
          marginRight="50px"
          > Recipe Book</Text>
        <SearchInput onSearch={onSearch}/>
        <Link to="/sign-in" style={linkStyle}>Sign In</Link>
        <Link to="/sign-up" style={linkStyle}>Sign Up</Link>
        <ColorModeSwitch /> 
        </HStack>
=======
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
>>>>>>> f6acfede9528ff1e2154abd1cd83fe58dcb034a8:frontend/src/components/NavBar.tsx
      </HStack>
    
  );
};

<<<<<<< HEAD:frontend/recipe_book/src/components/NavBar.tsx
const linkStyle = {
  textDecoration: "none", 
  marginLeft: "35px", 
  color: "#a80863",
  fontSize: "1.4em", 
  fontWeight: "bold", 
  transition: "color 0.3s ease", 
  ":hover": {
    color: "#000", 
  },
};

export default NavBar;
=======
export default NavBar;
>>>>>>> f6acfede9528ff1e2154abd1cd83fe58dcb034a8:frontend/src/components/NavBar.tsx
