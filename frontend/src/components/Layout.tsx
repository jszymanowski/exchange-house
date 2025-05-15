import { Flex, Footer, Text } from "@still-forest/canopy";
import Header from "./Header";

export default function Layout({ children }: { children: React.ReactNode }) {
  return (
    <Flex direction="col" className="mx-auto h-full w-full max-w-screen-lg">
      <Header />
      <Flex.Item className="flex-1">{children}</Flex.Item>
      <Footer>
        <Text variant="muted" size="sm">
          © 2025 Still Forest LLC.
        </Text>
      </Footer>
    </Flex>
  );
}
