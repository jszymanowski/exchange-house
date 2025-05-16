import { Tabs } from "expo-router";
import { Platform } from "react-native";

import { HapticTab } from "@/components/HapticTab";
import { EmojiIcon } from "@/components/Typography";
import { IconSymbol } from "@/components/ui/IconSymbol";
import TabBarBackground from "@/components/ui/TabBarBackground";
import { Colors } from "@/constants/Colors";
import { CURRENCIES } from "@/data/currencies";
import { useCurrencySubscription } from "@/hooks/useCurrencySubscription";
import { useTheme } from "@/hooks/useThemePreference";

export default function TabLayout() {
  const { theme } = useTheme();
  const currencies = useCurrencySubscription();

  return (
    <Tabs
      screenOptions={{
        tabBarActiveTintColor: Colors[theme].tabBarForeground,
        headerShown: false,
        tabBarButton: HapticTab,
        tabBarBackground: TabBarBackground,
        tabBarStyle: Platform.select({
          ios: {
            // Use a transparent background on iOS to show the blur effect
            position: "absolute",
          },
          default: {},
        }),
      }}
    >
      <Tabs.Screen
        name="index"
        options={{
          href: null,
        }}
      />
      {currencies.map((code, i) => (
        <Tabs.Screen
          key={code}
          name={`currency${i + 1}`}
          options={{
            title: code,
            tabBarIcon: () => <EmojiIcon>{CURRENCIES[code]?.flag || "🌐"}</EmojiIcon>,
          }}
        />
      ))}
      <Tabs.Screen
        name="settings"
        options={{
          title: "Settings",
          tabBarIcon: ({ color }) => <IconSymbol size={20} name="gear" color={color} />,
        }}
      />
    </Tabs>
  );
}
