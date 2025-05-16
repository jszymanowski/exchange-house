import { createContext } from "react";

type StorageContextType = {
  getItem: (key: string) => Promise<string | null>;
  setItem: (key: string, value: string) => Promise<void>;
  subscribe: (key: string, callback: () => void) => () => void;
};

export const StorageContext = createContext<StorageContextType | null>(null);
