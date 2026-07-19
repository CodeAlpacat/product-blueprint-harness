import { PrimaryButton } from "../components/PrimaryButton";

export function DepthBoard() {
  return (
    <main>
      <section aria-labelledby="depth-one"><h1 id="depth-one">Home · Depth 1</h1><PrimaryButton>Open item</PrimaryButton></section>
      <section aria-labelledby="depth-two"><h2 id="depth-two">Detail · Depth 2</h2><PrimaryButton>Retry</PrimaryButton></section>
    </main>
  );
}
