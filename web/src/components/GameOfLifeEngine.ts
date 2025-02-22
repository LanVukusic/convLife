export class GameOfLife {
  worldGrid: boolean[][];
  gridSize: number;
  iteration: number;

  constructor(gridSize: number = 8) {
    // Initialize the board with random live (true) and dead (false) cells
    this.gridSize = gridSize;
    this.worldGrid = [[]];
    this.iteration = 0;
    this.randomizeGrid();
  }

  randomizeGrid() {
    this.worldGrid = new Array(this.gridSize)
      .fill(false)
      .map(() =>
        new Array(this.gridSize).fill(false).map(() => Math.random() > 0.85)
      );
  }

  step() {
    const newBoard = this.worldGrid.map((row, i) =>
      row.map((cell, j) => {
        const liveNeighbors = this.countLiveNeighbors(i, j);
        if (cell) {
          // Any live cell with 2 or 3 live neighbors lives on to the next generation
          return liveNeighbors === 2 || liveNeighbors === 3;
        } else {
          // Any dead cell with exactly 3 live neighbors becomes a live cell
          return liveNeighbors === 3;
        }
      })
    );

    this.worldGrid = newBoard;
    this.iteration++;
  }

  toggle(y: number, x: number) {
    this.worldGrid[y][x] = !this.worldGrid[y][x];
    return this.worldGrid;
  }

  private countLiveNeighbors(x: number, y: number): number {
    let count = 0;
    for (let i = -1; i <= 1; i++) {
      for (let j = -1; j <= 1; j++) {
        if (i === 0 && j === 0) continue; // Skip the current cell
        const newX = x + i;
        const newY = y + j;
        if (
          newX >= 0 &&
          newX < this.worldGrid.length &&
          newY >= 0 &&
          newY < this.worldGrid[0].length &&
          this.worldGrid[newX][newY]
        ) {
          count++;
        }
      }
    }
    return count;
  }
}
