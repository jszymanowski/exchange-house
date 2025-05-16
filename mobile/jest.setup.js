jest.mock("@react-native-async-storage/async-storage", () =>
  require("@react-native-async-storage/async-storage/jest/async-storage-mock"),
);

jest.mock("@expo/vector-icons", () => ({
  Ionicons: "Ionicons",
}));

jest.mock("expo-symbols", () => {
  return {
    SymbolView: "SymbolView",
  };
});

jest.mock("expo-font", () => ({
  isLoaded: jest.fn(() => true),
  loadAsync: jest.fn(() => Promise.resolve()),
  __esModule: true,
  Font: {
    isLoaded: jest.fn(() => true),
    loadAsync: jest.fn(() => Promise.resolve()),
  },
}));

jest.mock("@expo/vector-icons", () => {
  const { View } = require("react-native");
  return {
    FontAwesome: (props) => <View testID={props.testID || "FontAwesomeMock"} />,
    MaterialIcons: (props) => <View testID={props.testID || "MaterialIconsMock"} />,
    Ionicons: (props) => <View testID={props.testID || "IoniconsMock"} />,
  };
});

jest.mock("expo-modules-core", () => ({
  Platform: {
    OS: "web",
    select: jest.fn((obj) => obj.web || obj.default),
  },
}));
