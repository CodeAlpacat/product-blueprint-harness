import { useState } from "react";
import { PrimaryButton } from "./components/PrimaryButton";

export function FlowPreview() {
  const [surface, setSurface] = useState<"home" | "detail">("home");
  return surface === "home" ? (
    <main data-surface="home"><h1>Home</h1><PrimaryButton onClick={() => setSurface("detail")}>Open item</PrimaryButton></main>
  ) : (
    <main data-surface="detail"><h1>Detail</h1><PrimaryButton>Retry</PrimaryButton></main>
  );
}
