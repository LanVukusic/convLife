import * as ort from "onnxruntime-web";
import { useEffect, useState } from "react";

export const useModel = (modelPath: string) => {
  const [isLoading, setIsLoading] = useState(true);
  const [isError, setIsError] = useState(false);
  const [session, setSession] = useState<ort.InferenceSession>();

  useEffect(() => {
    ort.InferenceSession.create(modelPath)
      .then((sess) => {
        setSession(sess);
      })
      .catch(() => {
        setIsError(true);
      })
      .finally(() => {
        setIsLoading(false);
      });

    return () => {};
  }, [modelPath]);

  const forward = (grid: number[][]) => {
    const data = Float32Array.from(grid.flat());
    const tensorA = new ort.Tensor("float32", data, [grid.length, grid.length]);
    return session?.run({ a: tensorA });
  };

  return {
    isLoading,
    isError,
    forward,
  };
};
