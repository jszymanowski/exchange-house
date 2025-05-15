import { Container, Footer, Text } from "@still-forest/canopy";

export default function Layout({ children }: { children: React.ReactNode }) {
  return (
    <Container className="mx-auto h-dvh">
      {children}
      <Footer>
        <Text variant="muted" size="sm">
          © 2025 Still Forest LLC.
        </Text>
      </Footer>
    </Container>
  );
}
