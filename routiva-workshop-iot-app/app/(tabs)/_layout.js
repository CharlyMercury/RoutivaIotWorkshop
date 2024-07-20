import { Tabs } from "expo-router";
import { FormIcon, HomeIcon, InfoIcon } from "../../components/Icons";

export default function TabsLayout() {
  return (
    <Tabs
      screenOptions={{
        headerShown: false,
        tabBarStyle: { backgroundColor: "#000" },
        tabBarActiveTintColor: "cyan",
      }}
    >
      <Tabs.Screen
        name="index"
        options={{
          title: "Home",
          tabBarIcon: ({ color }) => <HomeIcon color={color} />,
        }}
      />
      <Tabs.Screen
        name="about"
        options={{
          title: "Información",
          tabBarIcon: ({ color }) => <InfoIcon color={color} />,
        }}
      />
      <Tabs.Screen
        name="form"
        options={{
          title: "Formulatio",
          tabBarIcon: ({ color }) => <FormIcon color={color} />,
        }}
      />
    </Tabs>
  );
}
