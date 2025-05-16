import AsyncStorage from "@react-native-async-storage/async-storage";
import { useCallback, useMemo, useState } from "react";
import { StorageContext } from "./StorageContext";

export const StorageProvider = ({ children }: { children: React.ReactNode }) => {
  const [listeners, setListeners] = useState<Record<string, Array<() => void>>>({});

  const getItem = useCallback(async (key: string) => {
    return await AsyncStorage.getItem(key);
  }, []);

  const setItem = useCallback(
    async (key: string, value: string) => {
      await AsyncStorage.setItem(key, value);
      // Notify listeners
      if (listeners[key]) {
        listeners[key].forEach((callback) => callback());
      }
    },
    [listeners],
  );

  const subscribe = useCallback((key: string, callback: () => void) => {
    setListeners((prev) => ({
      ...prev,
      [key]: [...(prev[key] || []), callback],
    }));

    // Return unsubscribe function
    return () => {
      setListeners((prev) => ({
        ...prev,
        [key]: prev[key].filter((cb) => cb !== callback),
      }));
    };
  }, []);

  const contextValue = useMemo(
    () => ({
      getItem,
      setItem,
      subscribe,
    }),
    [getItem, setItem, subscribe],
  );

  return <StorageContext.Provider value={contextValue}>{children}</StorageContext.Provider>;
};
