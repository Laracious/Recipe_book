import { HStack, Image } from "@chakra-ui/react"
import logo from '../assets/LOGO.png'
import ColorModeSwitch from "./colorModeSwitch"

const NavBar = () => {
  return (
    <HStack justifyContent='space-between' padding={10}>
        <Image src={logo} boxSize= '60px'/>
        <ColorModeSwitch />
    </HStack>
  )
}

export default NavBar