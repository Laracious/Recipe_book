import { Flex, HStack, Image, Text } from "@chakra-ui/react";
import logo from "../assets/LOGO.png";
import ColorModeSwitch from "./colorModeSwitch";
import SearchInput from "./Searchinput";

interface Props {
  onSearch: (searchText: string) => void;
}

const NavBar = ({ onSearch}: Props) => {
  return (
    <HStack  padding={5}>
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
        
        <SearchInput onSearch={onSearch}/>
        <ColorModeSwitch />
        
      </HStack>
    </HStack>
  );
};

export default NavBar;