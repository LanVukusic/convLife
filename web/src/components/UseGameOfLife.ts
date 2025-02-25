import { useCallback, useEffect, useState } from "react";
import { GameOfLife } from "./GameOfLifeEngine";
import { useModel } from "./ModelRunner";

const modelPath = "/model8.onnx";

interface History {
  iteration: number;
  live: number;
  dead: number;
}

export const useGameOfLife = (gridSize: number) => {
  const [game, setGame] = useState<GameOfLife>();
  const [state, setState] = useState<boolean[][]>();
  const [isPlaying, setIsPlayling] = useState(true);
  const [history, setHistory] = useState<History[]>([]);
  const [lastHint, setLastHint] = useState<
    { x: number; y: number } | undefined
  >();
  const [lastPredictions, setLstPredictions] = useState<Float32Array>();
  const [help, setHelp] = useState<"no" | "random" | "ai">("ai");

  const { forward, isError, isLoading } = useModel(modelPath);

  useEffect(() => {
    const g = new GameOfLife(gridSize);
    setGame(g);
    setState(g.worldGrid);
  }, [gridSize]);

  const randomize = useCallback(() => {
    game?.randomizeGrid();
    setState(game?.worldGrid);
  }, [game]);

  const st = useCallback(async () => {
    if (!game) {
      return;
    }

    game?.step();
    if (help == "no") {
      setLastHint(undefined);
      setLstPredictions(undefined);
    }
    if (help == "ai") {
      if (game.worldGrid) {
        const out = await forward(
          game.worldGrid.map((y) => y.map((x) => (x ? 1.0 : 0)))
        );

        if (out) {
          setLastHint({ x: out?.x, y: out?.y });
          setLstPredictions(out.predictions);
          game.toggle(out.y, out.x);
        }
      }
    }

    if (help == "random") {
      setLstPredictions(undefined);
      const x = Math.round(Math.random() * (gridSize - 1));
      const y = Math.round(Math.random() * (gridSize - 1));
      game.toggle(y, x);
      setLastHint({ x, y });
    }

    setState(game?.worldGrid);
    setHistory([
      {
        iteration: game?.iteration,
        dead: game.worldGrid.flat().filter((val) => !val).length,
        live: game.worldGrid.flat().filter((val) => val).length,
      },
      ...history.slice(0, 10),
    ]);
  }, [forward, game, gridSize, help, history]);

  const toggle = useCallback(
    (y: number, x: number) => {
      if (!game) {
        return;
      }
      setState(game.toggle(y, x).slice(0));
    },
    [game]
  );

  // useEffect(() => {
  //   console.log("state", state);
  // }, [state]);

  useEffect(() => {
    const timer = setInterval(() => {
      if (isPlaying) {
        st();
      }
    }, 100);

    return () => {
      clearInterval(timer);
    };
  }, [isPlaying, st]);

  return {
    state,
    randomize,
    step: st,
    setIsPlayling,
    isPlaying,
    history,
    toggle,
    help,
    setHelp,
    isError,
    isLoading,
    lastHint,
    lastPredictions,
  };
};
