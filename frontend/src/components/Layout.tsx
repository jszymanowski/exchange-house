import { Container } from "@still-forest/canopy";

export default function Layout({ children }: { children: React.ReactNode }) {
  return <Container className="mx-auto h-dvh">{children}</Container>;
}
