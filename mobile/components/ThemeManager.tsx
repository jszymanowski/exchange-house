import AsyncStorage from "@react-native-async-storage/async-storage";
import type React from "react";
import { createContext, useEffect, useState } from "react";
import { Appearance } from "react-native";

export const THEME_OPTIONS = ["system", "light", "dark"] as const;
type ThemePreference = (typeof THEME_OPTIONS)[number];

interface ThemeContextType {
  themePreference: ThemePreference;
  setThemePreference: (preference: ThemePreference) => void;
}

export const ThemeContext = createContext<ThemeContextType | undefined>(undefined);
const THEME_PREFERENCE_KEY = "theme_preference";

export const ThemeProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [themePreference, setThemePreferenceState] = useState<ThemePreference>("system");

  // Load saved theme preference on mount
  useEffect(() => {
    const loadThemePreference = async () => {
      try {
        const savedPreference = await AsyncStorage.getItem(THEME_PREFERENCE_KEY);
        if (
          savedPreference &&
          (savedPreference === "system" || savedPreference === "light" || savedPreference === "dark")
        ) {
          applyThemePreference(savedPreference as ThemePreference);
        }
      } catch (error) {
        console.error("Failed to load theme preference:", error);
      }
    };

    loadThemePreference();
  }, []);

  // Apply theme preference by setting the color scheme override
  const applyThemePreference = (preference: ThemePreference) => {
    setThemePreferenceState(preference);

    // Only override if not using system preference
    if (preference !== "system") {
      Appearance.setColorScheme(preference);
    } else {
      // Reset to system preference
      Appearance.setColorScheme(null);
    }
  };

  // Save and apply theme preference
  const setThemePreference = async (preference: ThemePreference) => {
    try {
      await AsyncStorage.setItem(THEME_PREFERENCE_KEY, preference);
      applyThemePreference(preference);
    } catch (error) {
      console.error("Failed to save theme preference:", error);
    }
  };

  return <ThemeContext.Provider value={{ themePreference, setThemePreference }}>{children}</ThemeContext.Provider>;
};
