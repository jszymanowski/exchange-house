import { View } from "react-native";
import { useTheme } from "@/hooks/useThemePreference";

interface ScreenWrapperProps {
  children: React.ReactNode;
}

export const ScreenWrapper = ({ children }: ScreenWrapperProps) => {
  const { colors } = useTheme();
  return (
    <View style={{ backgroundColor: colors.background }} className="h-full px-4">
      {children}
    </View>
  );
};
