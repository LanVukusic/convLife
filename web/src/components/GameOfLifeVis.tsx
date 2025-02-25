import { Box, Flex, lighten, SimpleGrid } from "@mantine/core";
import { vgreen, vpurp, vyel } from "../main";

export interface GameOfLifeProps {
  grid: boolean[][];
  onClick: (y: number, x: number) => void;
  hint: { x: number; y: number } | undefined;
}

export const GameOfLifeVis = ({ grid, onClick, hint }: GameOfLifeProps) => {
  const cols = grid[0]?.length ?? 0;

  return (
    <Flex>
      <SimpleGrid cols={cols} spacing="0">
        {grid.flat().map((isAlive, index) => {
          const x = index % grid.length;
          const y = Math.floor(index / grid.length);
          return (
            <Box
              key={index}
              bg={
                hint && hint.x == x && hint.y == y
                  ? vgreen
                  : isAlive
                  ? vyel
                  : vpurp
              }
              onClick={() => {
                onClick(Math.floor(index / cols), index % cols);
              }}
              style={{
                cursor: "pointer",
                border: "1px solid",
                borderColor: lighten(vpurp, 0.05),
                aspectRatio: "1",
                transition: "background-color 0.1s ease",
                width: 40,
              }}
            >
              {/* {Math.floor(index / cols) + " / " + (index % cols)} */}
            </Box>
          );
        })}
      </SimpleGrid>
    </Flex>
  );
};
