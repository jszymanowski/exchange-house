import React from "react";
import { render, act } from "@testing-library/react-native";
import AsyncStorage from "@react-native-async-storage/async-storage";
import { StorageProvider } from "../../hooks/StorageProvider";
import { StorageContext } from "../../hooks/StorageContext";
import { Text } from "react-native";

// Mock AsyncStorage
jest.mock("@react-native-async-storage/async-storage", () => ({
  getItem: jest.fn(),
  setItem: jest.fn(),
}));

describe("StorageProvider", () => {
  beforeEach(() => {
    // Clear all mocks before each test
    jest.clearAllMocks();
  });

  it("should render children", () => {
    (AsyncStorage.setItem as jest.Mock).mockResolvedValue(undefined);
    const { getByText } = render(
      <StorageProvider>
        <TestComponent />
      </StorageProvider>
    );

    expect(getByText("Test Child")).toBeTruthy();
  });

  it("should get item from AsyncStorage", async () => {
    (AsyncStorage.setItem as jest.Mock).mockResolvedValue(undefined);
    const mockValue = "test-value";
    (AsyncStorage.getItem as jest.Mock).mockResolvedValue(mockValue);

    let storageContext: any;
    const { getByText } = render(
      <StorageProvider>
        <TestComponent onContext={(context) => (storageContext = context)} />
      </StorageProvider>
    );

    expect(getByText("Test Child")).toBeTruthy();

    const result = await storageContext.getItem("test-key");
    expect(result).toBe(mockValue);
    expect(AsyncStorage.getItem).toHaveBeenCalledWith("test-key");
  });

  it("should set item in AsyncStorage", async () => {
    (AsyncStorage.setItem as jest.Mock).mockResolvedValue(undefined);
    const mockValue = "test-value";

    let storageContext: any;
    const { getByText } = render(
      <StorageProvider>
        <TestComponent onContext={(context) => (storageContext = context)} />
      </StorageProvider>
    );

    expect(getByText("Test Child")).toBeTruthy();

    await storageContext.setItem("test-key", mockValue);
    expect(AsyncStorage.setItem).toHaveBeenCalledWith("test-key", mockValue);
  });

  it("should handle errors when getting item", async () => {
    (AsyncStorage.setItem as jest.Mock).mockResolvedValue(undefined);
    const mockError = new Error("Storage error");
    (AsyncStorage.getItem as jest.Mock).mockRejectedValue(mockError);

    let storageContext: any;
    const { getByText } = render(
      <StorageProvider>
        <TestComponent onContext={(context) => (storageContext = context)} />
      </StorageProvider>
    );

    expect(getByText("Test Child")).toBeTruthy();

    const result = await storageContext.getItem("test-key");
    expect(result).toBeNull();
  });

  it("should handle errors when setting item", async () => {
    const mockError = new Error("Storage error");
    (AsyncStorage.setItem as jest.Mock).mockRejectedValue(mockError);

    let storageContext: any;
    const { getByText } = render(
      <StorageProvider>
        <TestComponent onContext={(context) => (storageContext = context)} />
      </StorageProvider>
    );

    expect(getByText("Test Child")).toBeTruthy();

    await expect(storageContext.setItem("test-key", "value")).rejects.toThrow(
      "Storage error"
    );
  });

  it("should notify subscribers when item is set", async () => {
    (AsyncStorage.setItem as jest.Mock).mockResolvedValue(undefined);
    const mockCallback = jest.fn();
    let storageContext: any;
    const { getByText } = render(
      <StorageProvider>
        <TestComponent onContext={(context) => (storageContext = context)} />
      </StorageProvider>
    );

    expect(getByText("Test Child")).toBeTruthy();

    // Subscribe to changes
    const unsubscribe = storageContext.subscribe("test-key", mockCallback);
    // Wait for state update to flush
    await act(async () => {
      await Promise.resolve();
    });

    // Set an item
    await storageContext.setItem("test-key", "new-value");

    // Verify callback was called
    expect(mockCallback).toHaveBeenCalledTimes(1);

    // Unsubscribe
    unsubscribe();
    // Wait for state update to flush
    await act(async () => {
      await Promise.resolve();
    });

    // Set another item
    await storageContext.setItem("test-key", "another-value");

    // Verify callback was not called again
    expect(mockCallback).toHaveBeenCalledTimes(1);
  });

  it("should handle multiple subscribers for the same key", async () => {
    (AsyncStorage.setItem as jest.Mock).mockResolvedValue(undefined);
    const mockCallback1 = jest.fn();
    const mockCallback2 = jest.fn();
    let storageContext: any;
    const { getByText } = render(
      <StorageProvider>
        <TestComponent onContext={(context) => (storageContext = context)} />
      </StorageProvider>
    );

    expect(getByText("Test Child")).toBeTruthy();

    // Subscribe two callbacks
    storageContext.subscribe("test-key", mockCallback1);
    storageContext.subscribe("test-key", mockCallback2);
    // Wait for state update to flush
    await act(async () => {
      await Promise.resolve();
    });

    // Set an item
    await storageContext.setItem("test-key", "new-value");

    // Verify both callbacks were called
    expect(mockCallback1).toHaveBeenCalledTimes(1);
    expect(mockCallback2).toHaveBeenCalledTimes(1);
  });
});

// Test component to access the context
const TestComponent = ({
  onContext,
}: {
  onContext?: (context: any) => void;
}) => {
  const context = React.useContext(StorageContext);

  React.useEffect(() => {
    if (onContext) {
      onContext(context);
    }
  }, [context, onContext]);

  return <Text>Test Child</Text>;
};
