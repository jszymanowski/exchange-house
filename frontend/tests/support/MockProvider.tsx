import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { MOCK_CURRENCY_PAIRS } from "@tests/support/server";
import type React from "react";
import { useState } from "react";

type MockProviderProps = {
  children: React.ReactNode;
  queryKey: (string | undefined)[];
  mockData: unknown;
};

export default function MockProvider({ children, queryKey, mockData }: MockProviderProps) {
  const [queryClient] = useState(() => new QueryClient());

  queryClient.setQueryData(["currency-pairs"], {
    data: MOCK_CURRENCY_PAIRS,
  });
  queryClient.setQueryData(queryKey, {
    data: mockData,
  });

  return <QueryClientProvider client={queryClient}>{children}</QueryClientProvider>;
}
