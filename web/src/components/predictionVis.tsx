import { Box, Flex, lighten, SimpleGrid } from "@mantine/core";
import { vpurp } from "../main";
import { getViridisHex } from "../viridis";
import { useMemo } from "react";

export interface GameOfLifeProps {
  predictions: Float32Array;
  size: number;
}

export const PredictionVis = ({ predictions, size }: GameOfLifeProps) => {
  const arPred = useMemo(() => {
    return Array.from(predictions);
  }, [predictions]);
  const mx = Math.max(...arPred);

  return (
    <Flex>
      <SimpleGrid cols={size} spacing="0">
        {arPred.map((value, index) => {
          return (
            <Box
              key={index}
              bg={getViridisHex(value / mx)}
              style={{
                cursor: "pointer",
                border: "1px solid",
                borderColor: lighten(vpurp, 0.05),
                aspectRatio: "1",
                transition: "background-color 0.1s ease",
                width: 40,
              }}
            ></Box>
          );
        })}
      </SimpleGrid>
    </Flex>
  );
};
