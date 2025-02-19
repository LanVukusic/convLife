import { LineChart } from "@mantine/charts";
import {
  Box,
  Button,
  Card,
  Center,
  Container,
  Flex,
  Group,
  SegmentedControl,
  SimpleGrid,
  Stack,
  Text,
  Title,
} from "@mantine/core";
import { GameOfLifeVis } from "./components/GameOfLifeVis";
import { vgreen, vpurp, vyel } from "./main";
import { useGameOfLife } from "./components/UseGameOfLife";
import { IconX, IconQuestionMark, IconSparkles } from "@tabler/icons-react";

const gridSize = 16;

export const App = () => {
  const {
    state,
    randomize,
    step,
    setIsPlayling,
    isPlaying,
    history,
    toggle,
    help,
    setHelp,
    isLoading,
    isError,
  } = useGameOfLife(gridSize);
  return (
    <Stack>
      <Flex pos="relative">
        <SimpleGrid cols={2} pos="absolute" w="100%" h="100%" spacing={0}>
          <Box bg={vyel}></Box>
          <Box bg={vpurp}></Box>
        </SimpleGrid>

        <Container style={{ zIndex: 10 }} w="100%">
          <Stack justify="center" my="xl">
            <Title order={1} p="xl" bg="white" w="fit">
              ConvLife
            </Title>
            <Box
              style={{
                width: "",
              }}
            >
              <Title order={2} bg={vgreen} size="sm" p="lg" c="white">
                Neural network for persisting game of life state
              </Title>
            </Box>
            <Group>
              <Button
                component="a"
                target="_blank"
                href="https://docs.google.com/presentation/d/1ROGDIO5ggTeZ1F3k_y5aE4DJ_9712d0dIGgGy1fLBpw/preview"
              >
                Presentation
              </Button>
              <Button
                variant="light"
                component="a"
                target="_blank"
                href="https://docs.google.com/presentation/d/1ROGDIO5ggTeZ1F3k_y5aE4DJ_9712d0dIGgGy1fLBpw/preview"
              >
                Github
              </Button>
            </Group>
          </Stack>
        </Container>
      </Flex>
      <Box
        pos="relative"
        p="0"
        ml="-10%"
        style={{
          overflow: "hidden",
        }}
      >
        <Container py="12rem">
          <Stack gap="xl">
            <Text>
              Lorem ipsum dolor, sit amet consectetur adipisicing elit.
              Perspiciatis quis ratione vero, minus ullam repellat obcaecati
              soluta quia sunt harum!
            </Text>

            <Group w="100%" gap="xl" justify="center">
              <Button.Group>
                <Button variant="light" onClick={randomize}>
                  randomize
                </Button>
                <Button
                  variant="filled"
                  onClick={() => {
                    setIsPlayling(!isPlaying);
                  }}
                >
                  {isPlaying ? "Pause" : "Play"}
                </Button>
                <Button variant="light" onClick={step} disabled={isPlaying}>
                  step
                </Button>
              </Button.Group>
              <SegmentedControl
                // color="vpurple"
                value={help}
                //@ts-expect-error its fine
                onChange={setHelp}
                data={[
                  {
                    value: "no",
                    label: (
                      <Center style={{ gap: 10 }}>
                        <IconX size={16} />
                        <span>No help</span>
                      </Center>
                    ),
                  },
                  {
                    value: "random",
                    label: (
                      <Center style={{ gap: 10 }}>
                        <IconQuestionMark size={16} />
                        <span>Random placing</span>
                      </Center>
                    ),
                  },
                  {
                    value: "agent",
                    label: (
                      <Center style={{ gap: 10 }}>
                        <IconSparkles size={16} />
                        <span>AI Agent</span>
                      </Center>
                    ),
                  },
                ]}
              />
            </Group>

            <Group align="stretch" py="xl">
              <Card shadow="xl" p="0">
                {state && <GameOfLifeVis grid={state} onClick={toggle} />}
              </Card>

              <Stack justify="start" py="md">
                <LineChart
                  style={{
                    margin: "0",
                    padding: 0,
                    zIndex: -1,
                    position: "absolute",
                    left: 0,
                  }}
                  yAxisLabel={undefined}
                  w="100%"
                  h="600"
                  data={history}
                  dataKey="date"
                  yAxisProps={{
                    domain: [-5, gridSize * gridSize + 5],
                    tick: false,
                  }}
                  xAxisProps={{ tick: false }}
                  strokeWidth={8}
                  series={[
                    { name: "live", color: vyel },
                    { name: "dead", color: vpurp },
                  ]}
                />
              </Stack>
            </Group>
          </Stack>
        </Container>
      </Box>

      <Box h="12rem" w="100%" pos="relative" bg={vpurp}></Box>
    </Stack>
  );
};
