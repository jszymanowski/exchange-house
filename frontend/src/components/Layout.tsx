import { Box, Footer, Text } from "@still-forest/canopy";
import Header from "./Header";

export default function Layout({ children }: { children: React.ReactNode }) {
  return (
    <>
      <Header />
      <Box className="mx-auto h-dvh">{children}</Box>
      <Footer>
        <Text variant="muted" size="sm">
          © 2025 Still Forest LLC.
        </Text>
      </Footer>
    </>
  );
}
