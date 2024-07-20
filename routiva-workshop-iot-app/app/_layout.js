import { Link, Stack } from "expo-router";
import { Pressable, View } from "react-native";
import { InfoIcon } from "../components/Icons";
import { Logo } from "../components/Logo";

export default function Layout() {
  return (
    <View className="flex-1">
      <Stack
        screenOptions={{
          headerStyle: { backgroundColor: "#448aff" },
          headerTintColor: "yellow",
          headerTitle: "",
          headerLeft: () => <Logo />,
        }}
      />
    </View>
  );
}
