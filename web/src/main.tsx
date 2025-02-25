import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import "@mantine/core/styles.css";
import { createTheme, MantineProvider } from "@mantine/core";
import { App } from "./App";

export const vpurp = "#440154";
export const vyel = "#fde725";
export const vgreen = "#29AF7F";

const theme = createTheme({
  primaryColor: "vpurple",
  primaryShade: 9,
  fontFamily: "mono",
  colors: {
    vpurple: [
      "#fbebff",
      "#f3d2fb",
      "#e89ff9",
      "#dd6bf7",
      "#d341f6",
      "#cd2af6",
      "#cb20f6",
      "#b317db",
      "#a010c4",
      "#8b02ab",
    ],
    vyello: [
      "#fffde0",
      "#fffacb",
      "#fef49a",
      "#feee64",
      "#fde937",
      "#fde61a",
      "#fde402",
      "#e1ca00",
      "#c8b400",
      "#ac9b00",
    ],
  },
});

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <MantineProvider theme={theme} forceColorScheme="light">
      <App />
    </MantineProvider>
  </StrictMode>
);
