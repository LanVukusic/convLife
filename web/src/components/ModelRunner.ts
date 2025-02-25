import * as ort from "onnxruntime-web";
import { useEffect, useState } from "react";

export const useModel = (modelPath: string) => {
  const [isLoading, setIsLoading] = useState(true);
  const [isError, setIsError] = useState(false);
  const [session, setSession] = useState<ort.InferenceSession>();

  useEffect(() => {
    ort.InferenceSession.create(
      modelPath
      // {
      //   executionProviders: [],
      // }
    )
      .then((sess) => {
        setSession(sess);
      })
      .catch((reason: unknown) => {
        console.error({ reason });

        setIsError(true);
      })
      .finally(() => {
        setIsLoading(false);
      });

    return () => {};
  }, [modelPath]);

  const forward = async (grid: number[][]) => {
    const data = Float32Array.from(grid.flat());
    const tensorX = new ort.Tensor("float32", data, [
      1,
      1,
      grid.length,
      grid.length,
    ]);
    const out = await session?.run({ input: tensorX });
    if (!out) {
      return;
    }
    const outTensor = out.output;
    const outputData = outTensor.data; // Access the tensor's data as a Float32Array

    // Find the index of the maximum value in the output data
    let maxIndex = 0;
    let maxVal = outputData[0];
    for (let i = 1; i < outputData.length; i++) {
      if (outputData[i] > maxVal) {
        maxVal = outputData[i];
        maxIndex = i;
      }
    }

    // Convert the flat index to (x, y) coordinates
    const y = Math.floor(maxIndex / grid.length); // Row (height) index
    const x = maxIndex % grid.length; // Column (width) index

    const predictions = (await outTensor
      .reshape([grid.length, grid.length])
      .getData()) as Float32Array;

    return { x, y, predictions };
  };

  return {
    isLoading,
    isError,
    forward,
  };
};
