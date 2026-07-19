import type { ButtonHTMLAttributes } from "react";

export type PrimaryButtonProps = ButtonHTMLAttributes<HTMLButtonElement> & {
  pending?: boolean;
};

export function PrimaryButton({ pending = false, children, disabled, ...props }: PrimaryButtonProps) {
  return (
    <button {...props} disabled={disabled || pending} aria-busy={pending || undefined}>
      {pending ? "Loading" : children}
    </button>
  );
}
