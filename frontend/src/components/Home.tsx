import { Heading, Text } from "@jszymanowski/breeze-primitives";
import { API_URL } from "@/config";
import Dashboard from "@/components/Dashboard";

export default function Home() {
  return (
    <div>
      <Heading level="1">Exchange House</Heading>
      <a href={`${API_URL}/docs`} target="_blank" rel="noopener noreferrer">
        <Text>Docs</Text>
      </a>
      <Dashboard defaultFromIsoCode="SGD" defaultToIsoCode="USD" />
    </div>
  );
}
