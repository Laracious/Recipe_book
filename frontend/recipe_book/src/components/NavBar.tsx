import { HStack, Image, Text, } from "@chakra-ui/react";
import logo from "../assets/LOGO.png";
import ColorModeSwitch from "./colorModeSwitch";
import SearchInput from "./Searchinput";
import { Link } from "react-router-dom";

interface Props {
  onSearch: (searchText: string) => void;
}
const NavBar = ({ onSearch}: Props) => {
  return (
    <HStack  padding={5} >
      <HStack >
        <Image src={logo} boxSize="60px" alt="Recipe Book Logo" />
        <Text
          whiteSpace="nowrap"
          fontSize="3xl"
          fontWeight="bold"
          color="#a80863"
          textShadow="2px 2px 2px rgba(0, 0, 0, 0.5)"
          marginRight="50px"
          > Recipe Book</Text>
        <SearchInput onSearch={onSearch}/>
        <Link to="/sign-in" style={linkStyle}>Sign In</Link>
        <Link to="/sign-up" style={linkStyle}>Sign Up</Link>
        <ColorModeSwitch /> 
        </HStack>
      </HStack>
    
  );
};

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