import { PrimaryButton } from "../components/PrimaryButton";

export function ComponentBoard() {
  return (
    <section aria-labelledby="button-states">
      <h2 id="button-states">Primary button states</h2>
      <PrimaryButton>Continue</PrimaryButton>
      <PrimaryButton pending>Continue</PrimaryButton>
      <PrimaryButton disabled>Continue</PrimaryButton>
    </section>
  );
}
