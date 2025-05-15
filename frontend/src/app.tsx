import { QueryClient, QueryClientProvider } from "@tanstack/react-query";

import Layout from "@/components/Layout";
import Dashboard from "./components/Dashboard";

const queryClient = new QueryClient();

export function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <Layout>
        <Dashboard defaultFromIsoCode="SGD" defaultToIsoCode="USD" />
      </Layout>
    </QueryClientProvider>
  );
}
