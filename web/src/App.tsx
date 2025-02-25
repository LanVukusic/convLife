import { LineChart } from "@mantine/charts";
import {
  Alert,
  Box,
  Button,
  Card,
  Center,
  Container,
  Flex,
  Group,
  lighten,
  LoadingOverlay,
  SegmentedControl,
  SimpleGrid,
  Stack,
  Text,
  Title,
} from "@mantine/core";
import { GameOfLifeVis } from "./components/GameOfLifeVis";
import { vgreen, vpurp, vyel } from "./main";
import { useGameOfLife } from "./components/UseGameOfLife";
import {
  IconX,
  IconQuestionMark,
  IconSparkles,
  IconBrandGithubFilled,
} from "@tabler/icons-react";
import { PredictionVis } from "./components/predictionVis";

const gridSize = 8;

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
    lastHint,
    isLoading,
    isError,
    lastPredictions,
  } = useGameOfLife(gridSize);
  return (
    <Stack w="100%">
      <Flex pos="relative">
        <SimpleGrid cols={2} pos="absolute" w="100%" h="100%" spacing={0}>
          <Box bg={vyel}></Box>
          <Box bg={vpurp}></Box>
        </SimpleGrid>
        <LoadingOverlay visible={isLoading} />

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
              {/* <Button
                component="a"
                target="_blank"
                href="https://docs.google.com/presentation/d/1ROGDIO5ggTeZ1F3k_y5aE4DJ_9712d0dIGgGy1fLBpw/preview"
              >
                Presentation
              </Button> */}
              <Button
                size="lg"
                variant="light"
                component="a"
                target="_blank"
                leftSection={<IconBrandGithubFilled />}
                href="https://github.com/LanVukusic/convLife"
              >
                Github
              </Button>
            </Group>
          </Stack>
        </Container>
      </Flex>

      <Center py="xl" pos="relative" w="100%">
        <Stack gap="xl">
          <Container>
            <Text size="xl" fw="bold">
              This is our contribution for the 2025{" "}
              <a href="https://dragonhack.si/">Dragonhack</a>!!
            </Text>
            <Text size="xl" fw="bold">
              In response to the task{" "}
              <i style={{ opacity: 0.7 }}>
                "make something cool and show it to us"
              </i>{" "}
              we've built an AI that plays game of life!
            </Text>
          </Container>
          <Container>
            <Stack py="xl">
              <Text>
                Using the convolutional network for state prediction we tried to
                understand what is difficult and what is simple for a model to
                learn and comprehend. Building on this knowledge, we constructed
                a deep-Q agent that plays the game of life and sustains the
                population with the least possible changes.
              </Text>
              <Text>
                We have successfully created an agent that can sustain a game
                alive for arbitrarily long time and pinpointed the problems and
                limitations that neural networks have regarding this task.
              </Text>
            </Stack>

            <Text size="sm" c="vpurple">
              * click on the grid to toggle values
            </Text>

            <Group w="100%" gap="xl" py="xl">
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
                    value: "ai",
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
          </Container>

          {isError && <Alert c="red">model error</Alert>}

          <Group align="stretch" py="xl">
            <Card
              shadow="xl"
              p="xs"
              bg={lighten(help == "ai" ? vgreen : vpurp, 0.1)}
              style={{
                boxShadow: "0px 0px 30px " + (help == "ai" ? vgreen : vpurp),
                transition: "0.5s",
              }}
            >
              <Center>
                {state && (
                  <GameOfLifeVis
                    grid={state}
                    onClick={toggle}
                    hint={lastHint}
                  />
                )}
                {lastPredictions && (
                  <PredictionVis
                    predictions={lastPredictions}
                    size={gridSize}
                  />
                )}
              </Center>
            </Card>

            <Stack justify="start">
              <LineChart
                style={{
                  margin: "0",
                  marginTop: "-4rem",
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
      </Center>

      <Box
        w="100%"
        pos="relative"
        bg={vpurp}
        c="white"
        px="0"
        py="xl"
        style={{ zIndex: -2 }}
        pt="3rem"
      >
        <Container>
          <Stack gap="lg">
            <Title py="xl">DeepQ learning</Title>
            <Text>
              To further test our findings we trained a deep-q agent to sustain
              a high-density population of pixels. The Game of Life environment
              was implemented as a PyTorch module. The state of the game is
              represented by a binary matrix where each cell can be either alive
              (1) or dead (0).
            </Text>
            <Text>
              The model uses convolutional layers to determine the number of
              neighbors for each cell, applying the standard Game of Life rules
              to transition to the next state. The DQN implementation involves
              an agent interacting with the Game of Life environment, learning
              to place cells in a manner that maximizes a reward signal. Our
              reward signal was the amount of alive cells.
            </Text>
            <Text>
              The neural network architecture used for the Q-function is a
              resnet like convolutional network with skip connections which
              predicts the Q values for all pixels. The training process
              involves episodes where the agent interacts with the environment,
              selecting actions based on an epsilon-greedy policy.
            </Text>
            <Text>
              The agent’s experience (state, action, next state, reward) is
              stored in a replay buffer, and the neural network is trained by
              sampling from this buffer. We use a policy network to predict the
              Q values of the current state and a target network to predict the
              future reward. The target network, which provides stable target
              values, is periodically updated with the policy network’s weights.
              Because the goal was to sustain the game of life as long as
              possible we used a two step training approach.
            </Text>
            <Text>
              First we trained the agent to sustain the game for 100 steps with
              16 batches. This allows the agent to understand the game enough to
              know that it should place a pixel near other alive pixels. Then we
              take the trained weights and train again with 1000 steps per
              episode, but a batch size of only 4. We skip the episode if all
              the pixels are dead.
            </Text>
          </Stack>
        </Container>
      </Box>
      <Box w="100%" pos="relative" bg={vyel} py="xl" c="grape" px="0">
        <Container>
          <Stack gap="lg">
            <Title py="xl">Results</Title>
            <Text c="black">
              We have progressively trained agent to perform less actions and
              sustain a bigger grid of cells. We found out that the agents can
              successfully maintain population with only one pixel per frame.
              Agent’s performance increases significantly as the training
              progresses and fully trained models can effectively sustain a
              large grid (tested with up to 32x32) with only 1 action per
              iteration. After training with the two step approach our model
              successfully managed to keep the cells for 1000 steps almost every
              time.
            </Text>
          </Stack>
        </Container>
      </Box>
    </Stack>
  );
};
