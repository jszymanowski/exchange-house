import { Ionicons } from "@expo/vector-icons";
import { useState } from "react";
import { FlatList, Modal, TextInput, TouchableOpacity, View } from "react-native";
import { Heading, Text } from "@/components/Typography";
import type { CurrencyCode } from "@/data/currencies";
import { useTheme } from "@/hooks/useThemePreference";
import type { Currency } from "@/models/Currency";

interface CurrencySelectionModalProps {
  selectedCurrency: CurrencyCode;
  currencies: Currency[];
  modalVisible: boolean;
  setModalVisible: (visible: boolean) => void;
  onCurrencyChange: (currency: CurrencyCode) => void;
}

export const CurrencySelectionModal = ({
  selectedCurrency,
  currencies,
  modalVisible,
  setModalVisible,
  onCurrencyChange,
}: CurrencySelectionModalProps) => {
  const { colors } = useTheme();
  const [searchText, setSearchText] = useState("");

  const filteredCurrencies = searchText
    ? currencies.filter(
        (c) =>
          c.code.toLowerCase().includes(searchText.toLowerCase()) ||
          c.name.toLowerCase().includes(searchText.toLowerCase()),
      )
    : currencies;
  return (
    <Modal
      animationType="slide"
      transparent={true}
      visible={modalVisible}
      onRequestClose={() => setModalVisible(false)}
    >
      <View className="flex flex-1 items-center justify-center">
        <View
          className="h-[80%] w-[90%] overflow-hidden rounded-lg border"
          style={{
            backgroundColor: colors.backgroundModal,
            borderColor: colors.border,
          }}
        >
          <View
            className="flex flex-row items-center justify-between border-b p-4"
            style={{
              backgroundColor: colors.backgroundModalHeader,
              borderColor: colors.border,
            }}
          >
            <Heading style={{ color: colors.text }}>Select Currency</Heading>
            <TouchableOpacity onPress={() => setModalVisible(false)}>
              <Ionicons name="close" size={24} style={{ color: colors.text }} />
            </TouchableOpacity>
          </View>

          <View
            className="flex flex-row items-center gap-4 border-b px-4 py-2"
            style={{
              backgroundColor: colors.backgroundModalHeader,
              borderColor: colors.border,
            }}
          >
            <Ionicons name="search" size={20} style={{ color: colors.textMuted }} />
            <TextInput
              className="flex-1 p-2"
              style={{ color: colors.text, fontSize: 16 }}
              placeholder="Search currencies..."
              value={searchText}
              onChangeText={setSearchText}
              autoCapitalize="none"
            />
            {searchText.length > 0 && (
              <TouchableOpacity onPress={() => setSearchText("")}>
                <Ionicons name="close-circle" size={18} style={{ color: colors.textMuted }} />
              </TouchableOpacity>
            )}
          </View>

          <FlatList
            data={filteredCurrencies}
            keyExtractor={(item) => item.code}
            renderItem={({ item }) => {
              const isSelected = selectedCurrency === item.code;
              return (
                <TouchableOpacity
                  className="flex flex-row items-center justify-between gap-4 border-b px-4 py-2"
                  style={{
                    borderColor: colors.border,
                    backgroundColor: isSelected ? colors.buttonSecondaryForeground : colors.backgroundModal,
                  }}
                  onPress={() => {
                    onCurrencyChange(item.code);
                    setModalVisible(false);
                    setSearchText("");
                  }}
                >
                  <Text className="text-2xl">{item.flag}</Text>
                  <View className="flex-1">
                    <Text
                      className="font-bold text-lg"
                      style={{
                        color: isSelected ? colors.textInverse : colors.text,
                      }}
                    >
                      {item.code}
                    </Text>
                    <Text className="text-base" style={{ color: colors.textMuted }}>
                      {item.name}
                    </Text>
                  </View>
                  {selectedCurrency === item.code && (
                    <Ionicons name="checkmark-sharp" size={24} color={colors.accent} />
                  )}
                </TouchableOpacity>
              );
            }}
          />
        </View>
      </View>
    </Modal>
  );
};
