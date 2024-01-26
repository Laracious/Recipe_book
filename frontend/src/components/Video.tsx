import { Link } from "react-router-dom";
import { Button } from "@chakra-ui/react";


interface Props {
  watch: string;
}

const Video = ({ watch }: Props) => {
  return (
    <Link to={watch}>
      <Button
        background="#075050"
        variant="ghost"
        fontSize="12px"
        paddingX={1}
        height="15px"
        borderRadius="4px"
        _hover={{ bg: "transparent" }}
      >
        Video
      </Button>
    </Link>
  );
};

export default Video;
