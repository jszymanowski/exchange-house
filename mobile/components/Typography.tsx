import { Text as BaseText, type TextProps as BaseTextProps, type StyleProp, type TextStyle } from "react-native";
import { useTheme } from "@/hooks/useThemePreference";

type TextProps = BaseTextProps & {
  family?: "sans" | "serif" | "monospace";
  style?: StyleProp<TextStyle>;
  className?: string;
  color?: "default" | "muted";
};

export const Text = ({ children, family, style, color, ...props }: TextProps) => {
  const { colors } = useTheme();

  const fontFamily = family
    ? family === "sans"
      ? "Inter"
      : family === "serif"
        ? "Georgia"
        : "monospace"
    : "sans-serif";

  const textColor = color === "muted" ? colors.textMuted : colors.text;

  return (
    <BaseText style={{ color: textColor, fontFamily, ...style }} {...props}>
      {children}
    </BaseText>
  );
};

type HeadingProps = TextProps & {
  level?: 1 | 2 | 3 | 4 | 5 | 6;
};

const HEADING_SIZES = {
  1: "text-4xl",
  2: "text-3xl",
  3: "text-2xl",
  4: "text-xl",
  5: "text-lg",
  6: "text-base",
};

export const Heading = ({ level = 3, family = "serif", children, className, ...props }: HeadingProps) => {
  const { colors } = useTheme();

  const fontClass = HEADING_SIZES[level];

  return (
    <Text family={family} className={`${fontClass} ${className}`} style={{ color: colors.text }} {...props}>
      {children}
    </Text>
  );
};

const EMOJI_SIZES = {
  small: "text-2xl",
  medium: "text-3xl",
  large: "text-4xl",
};

type EmojiIconProps = TextProps & {
  size?: "small" | "medium" | "large";
};

export const EmojiIcon = ({ size = "medium", children, ...props }: EmojiIconProps) => {
  const fontClass = EMOJI_SIZES[size];

  return (
    <Text family="monospace" className={fontClass} {...props}>
      {children}
    </Text>
  );
};
