import { View } from "react-native";

interface ContainerProps {
  children: React.ReactNode;
  className?: string;
}

export const Container = ({ children, className }: ContainerProps) => {
  return <View className={`px-4 ${className}`}>{children}</View>;
};
