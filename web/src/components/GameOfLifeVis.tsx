import { Box, Flex, lighten, SimpleGrid } from "@mantine/core";
import { vpurp, vyel } from "../main";

export interface GameOfLifeProps {
  grid: boolean[][];
  onClick: (y: number, x: number) => void;
}

export const GameOfLifeVis = ({ grid, onClick }: GameOfLifeProps) => {
  const cols = grid[0]?.length ?? 0;

  return (
    <Flex>
      <SimpleGrid
        cols={cols}
        spacing="0"
        // style={{ maxWidth: "900px", margin: "0 auto" }}
      >
        {grid.flat().map((isAlive, index) => (
          <Box
            key={index}
            bg={isAlive ? vyel : vpurp}
            onClick={() => {
              onClick(Math.floor(index / cols), index % cols);
            }}
            style={{
              cursor: "pointer",
              border: "1px solid",
              borderColor: lighten(vpurp, 0.05),
              aspectRatio: "1",
              transition: "background-color 0.2s ease",
              width: 40,
            }}
          >
            {/* {Math.floor(index / cols) + " / " + (index % cols)} */}
          </Box>
        ))}
      </SimpleGrid>
    </Flex>
  );
};
