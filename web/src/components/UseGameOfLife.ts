import { useCallback, useEffect, useState } from "react";
import { GameOfLife } from "./GameOfLifeEngine";
import { useModel } from "./ModelRunner";

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
  const [help, setHelp] = useState<"no" | "random" | "ai">("no");

  const { forward, isError, isLoading } = useModel("");

  useEffect(() => {
    const g = new GameOfLife(gridSize);
    setGame(g);
    setState(g.worldGrid);
  }, [gridSize]);

  const randomize = useCallback(() => {
    game?.randomizeGrid();
    setState(game?.worldGrid);
  }, [game]);

  const st = useCallback(() => {
    if (!game) {
      return;
    }

    // if(help == "ai"){
    //   const out = forward(game.worldGrid).
    // }

    game?.step();
    if (help == "random") {
      const x = Math.round(Math.random() * (gridSize - 1));
      const y = Math.round(Math.random() * (gridSize - 1));
      game.toggle(y, x);
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
  }, [game, gridSize, help, history]);

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
    }, 500);

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
  };
};
