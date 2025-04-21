import type React from "react";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";

import { MOCK_CURRENCY_PAIRS } from "@tests/support/server";

const queryClient = new QueryClient();

type MockProviderProps = {
  children: React.ReactNode;
  queryKey: string[];
  mockData: any; // eslint-disable-line @typescript-eslint/no-explicit-any
};

export default function MockProvider({
  children,
  queryKey,
  mockData,
}: MockProviderProps) {
  queryClient.setQueryData(["currency-pairs"], {
    data: MOCK_CURRENCY_PAIRS,
  });
  queryClient.setQueryData(queryKey, {
    data: mockData,
  });

  return (
    <QueryClientProvider client={queryClient}>{children}</QueryClientProvider>
  );
}
