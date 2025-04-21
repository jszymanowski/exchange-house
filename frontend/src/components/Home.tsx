import { Flex, Heading, Text } from "@jszymanowski/breeze-primitives";
import { API_URL } from "@/config";
import Dashboard from "@/components/Dashboard";
import { Button } from "@jszymanowski/breeze-forms";
import { SquareArrowOutUpRight } from "lucide-react";

export default function Home() {
  return (
    <div>
      <Flex justify="between" align="center">
        <Heading level="1">Exchange House</Heading>
        <Button
          variant="primary"
          onClick={() => {
            window.open(`${API_URL}/docs`, "_blank");
          }}
        >
          <Text variant="primary" size="md">
            API Docs{" "}
          </Text>
          <SquareArrowOutUpRight size={12} />
        </Button>
      </Flex>
      <Dashboard defaultFromIsoCode="SGD" defaultToIsoCode="USD" />
    </div>
  );
}
