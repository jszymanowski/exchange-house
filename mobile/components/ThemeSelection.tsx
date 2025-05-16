import { Icon } from "@rneui/themed";
import { useState } from "react";
import { View } from "react-native";
import { THEME_OPTIONS } from "@/components/ThemeManager";
import { useThemePreference } from "@/hooks/useThemePreference";
import { VerticalButtonGroup } from "./VerticalButtonGroup";

export const ThemeSelection = () => {
  const { themePreference, setThemePreference } = useThemePreference();
  const [selectedIndex, setSelectedIndex] = useState<number>(THEME_OPTIONS.findIndex((v) => v === themePreference));

  const options = [
    {
      icon: ({ color }: { color: string }) => <Icon name="adjust" type="font-awesome" size={16} color={color} />,
      label: "Automatic",
    },
    {
      icon: ({ color }: { color: string }) => <Icon name="sun" type="feather" size={16} color={color} />,
      label: "Light",
    },
    {
      icon: ({ color }: { color: string }) => <Icon name="moon" type="feather" size={16} color={color} />,
      label: "Dark",
    },
  ];

  return (
    <View testID="theme-selection">
      <VerticalButtonGroup
        selectedIndex={selectedIndex}
        onPress={(index) => {
          setSelectedIndex(index);
          setThemePreference(THEME_OPTIONS[index]);
        }}
        options={options}
      />
    </View>
  );
};
