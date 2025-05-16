import { render } from "@testing-library/react-native";
import ErrorBoundary from "@/components/ErrorBoundary";
import { ThemeProvider } from "@/components/ThemeManager";
import { StorageProvider } from "@/hooks/StorageProvider";

export const renderWithProviders = (component: React.ReactNode) => {
  return render(
    <ErrorBoundary>
      <ThemeProvider>
        <StorageProvider>{component}</StorageProvider>
      </ThemeProvider>
    </ErrorBoundary>,
  );
};
