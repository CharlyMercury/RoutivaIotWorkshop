import { Link, Stack } from "expo-router";
import { Pressable, View, Image } from "react-native";
import { InfoIcon } from "../components/Icons";
import { Logo } from "../components/Logo";
import logo from "../assets/routiva_logo.png";

export default function Layout() {
  return (
    <View className="flex-1">
      <Stack
        screenOptions={{
          headerStyle: { backgroundColor: "#448aee" },
          headerTintColor: "yellow",
          headerTitle: "",
          headerLeft: () => <Image className="h-12 w-40" source={logo} />,
        }}
      />
    </View>
  );
}
