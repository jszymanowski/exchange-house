import { Button, Flex, Heading, Text } from "@still-forest/canopy";
import { API_URL } from "@/config";
import { useQuery } from "@tanstack/react-query";
import Dashboard from "@/components/Dashboard";
import { SquareArrowOutUpRight } from "lucide-react";
import { getAvailableDates } from "@/services/exchangeRateService";

export default function Home() {
  const { data } = useQuery({
    queryKey: ["available-dates"],
    queryFn: () => getAvailableDates(),
  });

  const asOfDate = data?.data?.at(-1);

  const formattedAsOfDate = asOfDate?.toDate()?.toLocaleDateString("en-GB", {
    year: "numeric",
    month: "long",
    day: "numeric",
  });

  return (
    <>
      <Flex justify="between" align="center">
        <Flex align="end" gap="2">
          <Heading level="1">Exchange House API</Heading>
          {asOfDate && (
            <Heading level="4" variant="muted" family="sans" weight="thin">
              as of {formattedAsOfDate}
            </Heading>
          )}
        </Flex>
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
    </>
  );
}
