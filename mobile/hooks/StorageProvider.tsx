import AsyncStorage from "@react-native-async-storage/async-storage";
import { useCallback, useMemo, useState } from "react";
import { StorageContext } from "./StorageContext";

export const StorageProvider = ({ children }: { children: React.ReactNode }) => {
  const [listeners, setListeners] = useState<Record<string, Array<() => void>>>({});

  const getItem = useCallback(async (key: string) => {
    try {
      return await AsyncStorage.getItem(key);
    } catch (error) {
      console.error(`Error getting item with key "${key}":`, error);
      return null;
    }
  }, []);

  const setItem = useCallback(
    async (key: string, value: string) => {
      try {
        await AsyncStorage.setItem(key, value);
        // Notify listeners
        if (listeners[key]) {
          listeners[key].forEach((callback) => {
            try {
              callback();
            } catch (callbackError) {
              console.error(`Error in storage listener for key "${key}":`, callbackError);
            }
          });
        }
      } catch (error) {
        console.error(`Error setting item with key "${key}":`, error);
        throw error; // Re-throw to allow callers to handle the error
      }
    },
    [listeners],
  );

  const subscribe = useCallback((key: string, callback: () => void) => {
    setListeners((prev) => ({
      ...prev,
      [key]: prev[key] ? prev[key].filter((cb) => cb !== callback) : [],
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
