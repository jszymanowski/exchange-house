import { useContext } from "react";
import { type ColorSchemeName, useColorScheme as nativeUseColorScheme } from "react-native";
import { ThemeContext } from "@/components/ThemeManager";
import { Colors } from "@/constants/Colors";
export const useThemePreference = () => {
  const context = useContext(ThemeContext);
  if (context === undefined) {
    throw new Error("useThemePreference must be used within a ThemeProvider");
  }
  return context;
};

export const useTheme = () => {
  const { themePreference } = useThemePreference();
  const systemColorScheme = nativeUseColorScheme();

  const effectiveColorScheme: ColorSchemeName = themePreference === "system" ? systemColorScheme : themePreference;

  const theme = effectiveColorScheme || "light";

  return {
    theme,
    themePreference,
    isSystem: themePreference === "system",
    isDark: theme === "dark",
    isLight: theme === "light",
    colors: Colors[theme],
  };
};
