import { ButtonGroup } from "@rneui/themed";
import { View } from "react-native";
import { useTheme } from "@/hooks/useThemePreference";
import { Text } from "./Typography";

interface Option {
  icon: (props: { color: string }) => React.ReactNode;
  label: string;
  labelClassName?: string;
  description?: string;
}

interface VerticalButtonGroupProps {
  selectedIndex?: number;
  onPress: (index: number) => void;
  options?: Option[];
  extras?: React.ReactNode;
}

export const VerticalButtonGroup = ({ selectedIndex, onPress, options, extras }: VerticalButtonGroupProps) => {
  const { colors } = useTheme();

  if (!options || options.length === 0) {
    return null;
  }

  const buttons = options.map((option) => ({
    element: ({ isSelected }: { isSelected: boolean }) => {
      const color = isSelected ? colors.buttonForeground : colors.buttonSecondaryForeground;

      return (
        <View
          className="flex w-full flex-row items-center justify-between px-4 py-4"
          accessibilityRole="button"
          accessibilityState={{ selected: isSelected }}
          accessibilityLabel={option.label}
        >
          <View className="flex flex-row items-center gap-4">
            <option.icon color={color} />
            <Text
              className={`text-lg ${option.labelClassName}`}
              style={{
                color: color,
              }}
            >
              {option.label}
            </Text>
            {option.description && <Text style={{ color: colors.textMuted }}>{option.description}</Text>}
          </View>
          {extras}
        </View>
      );
    },
  }));

  return (
    <ButtonGroup
      vertical={true}
      buttons={buttons}
      buttonStyle={{
        backgroundColor: colors.buttonSecondaryBackground,
      }}
      buttonContainerStyle={{
        height: 60,
      }}
      selectedButtonStyle={{
        backgroundColor: colors.buttonBackground,
      }}
      containerStyle={{
        borderColor: colors.border,
        borderWidth: 1,
        borderRadius: 8,
        marginHorizontal: 0,
      }}
      innerBorderStyle={{
        color: colors.border,
      }}
      onPress={onPress}
      selectedIndex={selectedIndex}
    />
  );
};
