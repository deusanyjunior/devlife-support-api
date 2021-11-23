import { useState } from "react";

export function useToggle(
  defaultValue: boolean = false,
): [boolean, () => void] {
  const [state, setState] = useState(defaultValue);

  function toggleState(): void {
    setState((prev) => !prev);
  }

  return [state, toggleState];
}
