import { Heading, Text } from "@jszymanowski/breeze-primitives";
import {
  useQuery,
} from '@tanstack/react-query'

import ErrorOverlay from "@/components/ErrorOverlay"
import PageLoader from "@/components/PageLoader"
import { getAvailableCurrencyPairs } from "@/services/api";
import { API_URL } from "@/config";

export default function Home() {
  const { isPending, isError, error, data } = useQuery({ queryKey: ['currency-pairs'], queryFn: getAvailableCurrencyPairs })

  if (isPending || (!isError && !data)) return <PageLoader message="Loading exchange rates" />;
  if (isError) return <ErrorOverlay message={error?.message} />;

  const { data: currencyPairs } = data;

  return (
    <div>
      <Heading level="1">Exchange House</Heading>
      <a href={`${API_URL}/docs`} target="_blank" rel="noopener noreferrer">
        <Text>Docs</Text>
      </a>
      <ul>
        {currencyPairs.map((currencyPair) => (
          <li
            key={`${currencyPair.baseCurrencyCode}-${currencyPair.quoteCurrencyCode}`}
          >
            {currencyPair.baseCurrencyCode}
            {currencyPair.quoteCurrencyCode}
          </li>
        ))}
      </ul>
    </div>
  );
}
