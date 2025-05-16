import { Stack } from "expo-router";
import { View } from "react-native";
import ErrorBoundary from "@/components/ErrorBoundary";
import { ThemeProvider } from "@/components/ThemeManager";
import { Heading } from "@/components/Typography";
import { IconSymbol } from "@/components/ui/IconSymbol.ios";
import { StorageProvider } from "@/hooks/StorageProvider";
import { useTheme } from "@/hooks/useThemePreference";

import "./global.css";

const App = () => {
  const { colors } = useTheme();

  return (
    <Stack
      screenOptions={{
        headerStyle: {
          backgroundColor: colors.headerBackground,
        },
        headerTitle: () => (
          <View className="flex flex-row items-center gap-2">
            <IconSymbol name="dollarsign.bank.building" size={24} weight="light" color={colors.headerForeground} />
            <Heading level={3} style={{ color: colors.headerForeground }}>
              Exchange House
            </Heading>
          </View>
        ),
      }}
    >
      <Stack.Screen name="(tabs)" />
    </Stack>
  );
};

export default function RootLayout() {
  return (
    <ErrorBoundary>
      <ThemeProvider>
        <StorageProvider>
          <App />
        </StorageProvider>
      </ThemeProvider>
    </ErrorBoundary>
  );
}
